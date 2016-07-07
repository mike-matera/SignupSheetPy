import textwrap
import csv
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.http import Http404
from django.db import transaction
from django.db.utils import IntegrityError

from models import Coordinator, Job, Role, Source, Volunteer, global_signup_enable
from django.shortcuts import render, redirect

from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings

from access import is_coordinator, can_signup, can_delete

class SignupForm(forms.Form):
    name = forms.CharField(label='Name')
    comment = forms.CharField(label='Comment', required=False)
    def clean(self):
        super(SignupForm, self).clean()

@cache_page(3600)
def default(request):
    source = Source.objects.order_by('title')
    if len(source) == 0 :
        response_text = textwrap.dedent('''
          <html>
          <head>
          <title>Be the Ball</title>
          </head>
          <body>
          <p>A flute with no hole is not a flute.</p>
          <p>A doughnut without a hole is a danish.</p>
          </body>
        </html>''')
        return HttpResponse(response_text)    
    return redirect('jobs', source[0].title)

def jobs(request, title):
    # Fetch navigation information 
    sources = Source.objects.all()
    
    # Fetch the role information 
    source = Source.objects.filter(title__exact=title)
    role = Role.objects.filter(source__exact=source[0])[0]
    coordinators = Coordinator.objects.filter(source__exact=source[0])
    for c in coordinators : 
        # Fill images... 
        if c.url == "" : 
            c.url = settings.COORDINATOR_DEFAULT_IMG
        elif c.url[0:4] != "http" :
            c.url = settings.COORDINATOR_STATIC_IMG_URL + c.url
            
    total_staff = 0;
    needed_staff = 0;
    
    enabled = global_signup_enable()
    
    # Now find the people that are signed up
    jobstaff = []
    for job in Job.objects.filter(source__exact=source[0]).order_by('start') :
        entry = {}
        entry['job'] = job
        entry['volunteers'] = []
        for volunteer in Volunteer.objects.filter(source__exact=job.source.pk, title__exact=job.title, start__exact=job.start) :
            vol = {}
            vol['volunteer'] = volunteer
            if can_delete(request.user, volunteer) :
                vol['can_delete'] = volunteer.id
            else:
                vol['can_delete'] = None
                                            
            entry['volunteers'].append(vol)
                    
        # create "empty" volunteers so that rendering shows holes...
        needed = job.needs - len(entry['volunteers'])
        for _ in xrange(0, needed) :
            vol = {}
            vol['volunteer'] = None
            vol['can_delete'] = None 
            entry['volunteers'].append(vol)
        
        # Determine if the user is able to signup
        if needed > 0 :
            entry['can_signup'] = can_signup(request.user, job)
        else:
            entry['can_signup'] = False
            
        jobstaff.append(entry)
        total_staff += job.needs
        needed_staff += needed 
        
    template_values = {
        'sources': sources,
        'source': source[0],
        'role': role,
        'coordinators' : coordinators,
        'jobs' : jobstaff,
        'next' : title,
        'user' : request.user,
        'total' : total_staff, 
        'needed' : needed_staff,
        'enabled' : enabled,
    }
    return render_to_response('signup/jobpage.html', context=template_values)

@login_required
def signup(request, pk, template_name='signup/signup.html'):
    job = Job.objects.get(pk=pk)
    if job == None :
        raise Http404("Job does not exist")

    # TODO: Check perimssions 
    
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid() :         
            try: 
                with transaction.atomic() :
                    # Create a Volunteer with form data 
                    # We need the natural key from the job... this way 
                    # if the job changes in a non-meaningful way this volunteer
                    # continues to be valid. 
                    v = Volunteer(
                                  user = request.user,
                                  name = form.cleaned_data['name'],
                                  comment = form.cleaned_data['comment'],
                                  source = job.source.pk,
                                  title = job.title, 
                                  start = job.start,
                                  end = job.end,
                                  )

                    # NB: This feature requires discussion: Doing this will make it 
                    # impossible for people to sign up their friends for shifts.
                    #
                    # Before we commit this to the database let's check to see if the 
                    # user is already signed up for a shift at this time...
                    #shifts = Volunteer.objects.filter(user__exact=request.user)
                    #for s in shifts : 
                    #    if s.start == v.start \
                    #        or ( v.start < s.start and s.end < v.end ) \
                    #        or ( v.start > s.start and v.start < s.end ) :
                    #        raise ValueError("Overlap!")

                    # Now add the row, so the count query works...
                    v.save()
                    
                    # Now check if there are too many volunteers. This has to 
                    # be done atomically. If we're overbooked, rollback. 
                    volcount = Volunteer.objects.filter(source__exact=job.source.pk, title__exact=job.title, start__exact=job.start).count()
                    if volcount > job.needs :
                        raise IntegrityError("fuck! nabbed!")                         
                    
                    
            except IntegrityError:
                return HttpResponse('Oh no! This signup was nabbed!', status=450)

            except ValueError:
                return HttpResponse('Wait a second!', status=451)
                
            cache.clear()
            return redirect('jobs', job.source.pk)

        else:
            return render(request, template_name, {'form':form, 'ret':job.source.pk, 'job':job})
            
    else:
        ## Pre-fill the form with the user's name (They don't have to use it.)
        form = SignupForm({'name': request.user.first_name + " " + request.user.last_name})
        return render(request, template_name, {'form':form, 'ret':job.source.pk, 'job':job})

@login_required
def delete(request, pk, template_name='signup/confirmdelete.html'):
    volunteer = Volunteer.objects.get(pk=pk)
    if volunteer == None :
        raise Http404("Volunteer does not exist")

    # Check perimssions 
    #if request.user.pk != volunteer.pk and not request.user.is_staff :
    #    raise HttpResponseForbidden

    if request.method=='POST':
        volunteer.delete()
        cache.clear()
        return redirect('jobs', volunteer.source)
    
    return render(request, template_name, {'object':volunteer, 'ret':volunteer.source})

@user_passes_test(lambda u: is_coordinator(u))
def email_list(request, role, template_name='misc/email_list.html'):
    data = {}        
    data['role'] = role;
    temp = {}
    for v in Volunteer.objects.filter(source__exact=role) :
        person = User.objects.get(pk=v.user.pk)
        temp[person.email] = person.first_name + " " + person.last_name

    data['volunteers'] = []
    for email,name in temp.items() :
        data['volunteers'].append('"' + name + '" <' + email + ">")
            
    return render(request, template_name, {'data':data} )


EA_THRESHOLD = datetime.strptime('07/29/2016 13:00:00 UTC', '%m/%d/%Y %H:%M:%S %Z')
LD_THRESHOLD = datetime.strptime('07/31/2016 16:00:00 UTC', '%m/%d/%Y %H:%M:%S %Z')
TIMEFORMAT = "%A %I:%M %p"

def is_ea(starttime):
    return starttime <= EA_THRESHOLD

def is_ld(endtime):
    return endtime >= LD_THRESHOLD

@user_passes_test(lambda u: is_coordinator(u))
def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="StaffSheet.csv"'
    writer = csv.writer(response)
    writer.writerow(["Role", "Protected", "EA/LD", "Job", "Start Time", "End Time", "Person"])
    total = 0
    taken = 0;
    
    for j in Job.objects.order_by('source_id') :
        cnt = 0
        if j.protected : 
            prot = "Yes"
        else:
            prot = "";
        
        eald=""    
        if is_ea(j.start) :
            eald = "Early Arrival"
        
        if is_ld(j.end) :
            eald = "Late Departure"

        for v in Volunteer.objects.filter(source__exact=j.source.pk, title__exact=j.title, start__exact=j.start) :                
            writer.writerow([j.source.pk, prot, eald, j.title, j.start.strftime(TIMEFORMAT), j.end.strftime(TIMEFORMAT), v.name])
            cnt += 1
            
        for _ in xrange(0, j.needs - cnt) :
            writer.writerow([j.source.pk, prot, eald, j.title, j.start.strftime(TIMEFORMAT), j.end.strftime(TIMEFORMAT), ""])

        total += j.needs
        taken += cnt


    writer.writerow([])
    writer.writerow(['Total staff', total])
    writer.writerow(['Jobs unfilled', total-taken])
    return response

@user_passes_test(lambda u: is_coordinator(u))
def eald_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="EA_LD.csv"'
    writer = csv.writer(response)
    writer.writerow(["Early/Late", "Role", "Job", "Start Time", "End Time", "Person"])
    
    ea_total = 0 
    ea_filled = 0 
    ld_total = 0 
    ld_filled = 0 
        
    for j in Job.objects.filter(Q(start__lte = EA_THRESHOLD) | Q(end__gte = LD_THRESHOLD)).order_by('source_id', 'start') :
        cnt = 0

        if is_ea(j.start) :
            eald = "Early Arrival"
        
        if is_ld(j.end) :
            eald = "Late Departure"
            
        for v in Volunteer.objects.filter(source__exact=j.source, title__exact=j.title, start__exact=j.start) :                
            writer.writerow([eald, j.source.pk, j.title, j.start, j.end, v.name])
            cnt += 1
            
        for _ in xrange(0, j.needs - cnt) :
            writer.writerow([eald, j.source.pk, j.title, j.start, j.end, ""])

        if is_ea(j.start) :
            ea_total += j.needs
            ea_filled += cnt
        
        if is_ld(j.end) :
            ld_total += j.needs
            ld_filled += cnt

    writer.writerow([])
    writer.writerow(['Total Early Arrivals', ea_total])
    writer.writerow(['Taken Early Arrivals', ea_filled])
    writer.writerow(['Total Late Departures', ld_total])
    writer.writerow(['Taken Late Departures', ld_filled])
    
    return response
