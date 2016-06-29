import textwrap

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.http import Http404
from django.db import transaction
from django.db.utils import IntegrityError

from models import Coordinator, Job, Role, Source, Volunteer
from django.shortcuts import render, redirect

from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


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
    jobs = Job.objects.filter(source__exact=source[0]).order_by('start')
    
    # Now find the people that are signed up
    jobstaff = []
    for job in jobs :
        entry = {}
        entry['job'] = job
        entry['volunteers'] = []
        for volunteer in Volunteer.objects.filter(source__exact=job.source.pk, title__exact=job.title, start__exact=job.start) :
            vol = {}
            vol['volunteer'] = volunteer
            if request.user == volunteer.user or request.user.is_staff :
                vol['can_delete'] = volunteer.id
            else:
                vol['can_delete'] = None
                
            entry['volunteers'].append(vol)
                    
        # create "empty" volunteers so that rendering shows holes...
        needed = job.needs - len(entry['volunteers'])
        for x in xrange(0, needed) :
            vol = {}
            vol['volunteer'] = None
            vol['can_delete'] = None 
            entry['volunteers'].append(vol)
        
        # Determine if the user is able to signup
        entry['can_signup'] = False
        if needed > 0 and request.user.is_authenticated() :
            if job.protected :
                if request.user.is_staff :
                    entry['can_signup'] = True
            else:
                    entry['can_signup'] = True
                
        jobstaff.append(entry)
    
    template_values = {
        'sources': sources,
        'source': source[0],
        'role': role,
        'coordinators' : coordinators,
        'jobs' : jobstaff,
        'next' : title,
        'user' : request.user,
    }
    return render_to_response('signup/jobpage.html', context=template_values)

@login_required
def signup(request, pk, template_name='signup/signup.html'):
    job = Job.objects.get(pk=pk)
    if job == None :
        raise Http404("Job does not exist")

    # Check perimssions 
    #if job.protected and not request.user.is_staff :
    #    raise HttpResponseForbidden
    
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
