import csv, codecs, io
from operator import imod

from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.db import transaction
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from django.db.models import Sum
from django.core.cache import cache

from signup.models import Coordinator, Job, Role, Volunteer, Global
from signup.access import is_coordinator, is_coordinator_of, can_signup, can_delete, is_ea, is_ld, EA_THRESHOLD, LD_THRESHOLD, global_signup_enable

from signup.views.badge import badgeFor
import signup.views.source

def index(request):
    
    navdata = filterNavData(request.user)
    
    if len(navdata) == 0 : 
        if request.user.is_superuser :
            return redirect(signup.views.source.source_all)    
        else:
            if request.user.is_authenticated:
                return render(request, "underconstruction.html")
            else:
                return redirect('/accounts/login')
    
    return redirect('jobs', navdata[0]['role'].source.pk)
        
def getNavData() :
    # Test if there's nav information cached. 
    navdata = cache.get('navdata')
    if navdata != None :
        return navdata 
    
    # Otherwise fetch navigation information 
    roles = Role.objects.all().order_by('source')
    navdata = []
    for role in roles : 
        ent = {}
        ent['role'] = role;
        
        jobcount = Job.objects.filter(source__exact=role.source.pk).aggregate(Sum('needs'))['needs__sum']
        # Make sure zero count-jobs don't cause a crash
        if jobcount is None : 
            jobcount = 0
            
        personcount = Volunteer.objects.filter(source__exact=role.source.pk).count()
        ent['needed'] = jobcount - personcount
        ent['jobs'] = jobcount
        ent['status'] = role.status
        ent.update(badgeFor(role, jobcount, personcount))
        navdata.append(ent)
    
    navdata.sort(reverse=True, key=lambda role: role['needed'])
    cache.set('navdata', navdata, 60)
    return navdata

def filterNavData(user) :
    navdata = getNavData()
    rval = []
    for role in navdata : 
        if role['status'] == Role.ACTIVE :
            rval.append(role)
        else :
            if is_coordinator_of(user, role['role'].source) :
                rval.append(role)
    return rval
            
@login_required
def jobs(request, title):

    navdata = filterNavData(request.user)

    found = False
    for job in navdata : 
        if job['role'].source.title == title :
            found = True 
            break; 
    
    if not found : 
        return redirect('/')
    
    # Next and previous roles. 
    current_job_index = 0
    for i, item in enumerate(navdata) : 
        if item['role'].source.pk == title :
            current_job_index = i
            break

    next_job = navdata[(current_job_index + 1) % len(navdata)]['role'] 
    prev_job = navdata[(current_job_index - 1) % len(navdata)]['role'] 
    
        
    # Fetch the role information 
    roles = Role.objects.filter(source__exact=title)
    if len(roles) == 0 :
        # bogus role 
        return index(request)
    
    role = roles[0]
    coordinators = Coordinator.objects.filter(source__exact=title)
    for c in coordinators : 
        # Fill images... 
        if c.url == "" : 
            c.url = settings.COORDINATOR_DEFAULT_IMG
        elif c.url[0:4] != "http" :
            c.url = settings.COORDINATOR_STATIC_IMG_URL + c.url

    total_staff = 0;
    needed_staff = 0;

    # Now find the people that are signed up
    jobstaff = []
    for job in Job.objects.filter(source__exact=title).order_by('start') :
        entry = {}
        entry['job'] = job
        entry['volunteers'] = []
        for volunteer in Volunteer.objects.filter(source__exact=job.source.pk, title__exact=job.title, start__exact=job.start).select_related('user') :
            vol = {}
            vol['volunteer'] = volunteer
            if can_delete(request.user, volunteer) :
                vol['can_delete'] = volunteer.id
            else:
                vol['can_delete'] = None
                                            
            entry['volunteers'].append(vol)
                    
        # create "empty" volunteers so that rendering shows holes...
        needed = job.needs - len(entry['volunteers'])
        for _ in range(needed) :
            vol = {}
            vol['volunteer'] = None
            vol['can_delete'] = None 
            entry['volunteers'].append(vol)
        
        # Determine if the user is able to signup
        entry['needed'] = needed
        if needed > 0 :
            entry['can_signup'] = can_signup(request.user, role, job)
        else:
            entry['can_signup'] = False
            
        jobstaff.append(entry)
        total_staff += job.needs
        needed_staff += needed 
    
    # Fill enablement and status data 
    status = {}
    status['enable'] = global_signup_enable()
    status['color'] = 'black'
    status['text'] = 'This is the status'
    if status['enable'] == Global.COORDINATOR_ONLY :
        status['color'] = 'red'
        status['text'] = '''The staff sheet is not yet enabled for general signups.
                If you're a coordinator you will be able to fill your protected jobs.
                Otherwise please wait for an announcement indicating the general availability of the staff sheet.'''
    elif status['enable'] == Global.AVAILABLE : 
        if role.status == Role.DISABLED : 
            status['color'] = 'red'
            status['text'] = '''Signups for this job have been temporarily disabled until essential jobs are filled.'''
        else : 
            if needed_staff > 0 :
                status['text'] = "There are " + str(total_staff) + " jobs and " + str(needed_staff) + " left to fill."
            else :
                status['text'] = "All " + str(total_staff) + " available shifts are taken!"
    elif status['enable'] == Global.CLOSED :
        status['color'] = 'red'
        status['text'] = 'Signups are closed. See you next year!'

    template_values = {
        'navdata': navdata,
        'role': role,
        'coordinators' : coordinators,
        'jobs' : jobstaff,
        'user' : request.user,
        'total' : total_staff, 
        'needed' : needed_staff,
        'status' : status,
        'coordinator_of' : is_coordinator_of(request.user, role.source),
        'next' : next_job,
        'prev' : prev_job,
    }
    return render(request, 'signup/jobpage.html', context=template_values)

@login_required
def signup_view(request, pk):

    do_coordinator = False
    job = Job.objects.get(pk=pk)
    if job == None :
        raise Http404("Job does not exist")

    # TODO: Check perimssions 
    try: 
        with transaction.atomic() :
            signup_user = request.user

            #if do_coordinator : 
            #    # Check if the form has another user's email in it. 
            #    other_user = form.cleaned_data.get('email', None) 
            #    if other_user is not None and other_user != u'': 
            #        for user in User.objects.filter(email__exact=other_user) :
            #            signup_user = user
            #            break
                
            # Create a Volunteer with form data 
            # We need the natural key from the job... this way 
            # if the job changes in a non-meaningful way this volunteer
            # continues to be valid. 
            v = Volunteer(
                            user = signup_user,
                            comment = "fucky fuck fuck",
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
        
    return HttpResponse('You got it', status=200)
    
    
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


DAYFORMAT = "%A"
TIMEFORMAT = "%I:%M %p"
DAYTIMEFORMAT = DAYFORMAT + " " + TIMEFORMAT
            
@user_passes_test(lambda u: is_coordinator(u))
def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="StaffSheet.csv"'
    #writer = UnicodeWriter(response)
    writer = csv.writer(response, dialect='excel')
    writer.writerow(["Role", "Protected", "EA/LD", "Job", "Start Day", "Start Time", "End Day", "End Time", "Volunteer Name", "Email", "Comment"])
    total = 0
    taken = 0;
    
    for j in Job.objects.order_by('source_id', 'start') :
        cnt = 0
        if j.protected : 
            prot = "Yes"
        else:
            prot = "";
        
        eald=""    
        if is_ea(j) :
            eald = "Early Arrival"
        
        if is_ld(j) :
            eald = "Late Departure"

        for v in Volunteer.objects.filter(source__exact=j.source.pk, title__exact=j.title, start__exact=j.start).select_related('user') :
            writer.writerow([j.source.pk, prot, eald, j.title, j.start.strftime(DAYFORMAT), j.start.strftime(TIMEFORMAT), j.end.strftime(DAYFORMAT), j.end.strftime(TIMEFORMAT), v.user.first_name + " " + v.user.last_name,  v.user.email, v.comment])
            cnt += 1
            
        for _ in range(j.needs - cnt) :
            writer.writerow([j.source.pk, prot, eald, j.title, j.start.strftime(DAYFORMAT), j.start.strftime(TIMEFORMAT), j.end.strftime(DAYFORMAT), j.end.strftime(TIMEFORMAT), '', '', '', ''])

        total += j.needs
        taken += cnt


    writer.writerow([])
    writer.writerow(['Total staff', str(total)])
    writer.writerow(['Jobs unfilled', str(total-taken)])
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
        
    for j in Job.objects.filter(Q(start__lte = EA_THRESHOLD) | Q(end__gt = LD_THRESHOLD)).order_by('source_id', 'start') :
        cnt = 0

        if is_ea(j) :
            eald = "Early Arrival"
        
        if is_ld(j) :
            eald = "Late Departure"
            
        for v in Volunteer.objects.filter(source__exact=j.source, title__exact=j.title, start__exact=j.start) :                
            writer.writerow([eald, j.source.pk, j.title, j.start.strftime(DAYTIMEFORMAT), j.end.strftime(DAYTIMEFORMAT), v.name])
            cnt += 1
            
        for _ in range(j.needs - cnt) :
            writer.writerow([eald, j.source.pk, j.title, j.start.strftime(DAYTIMEFORMAT), j.end.strftime(DAYTIMEFORMAT), ""])

        if is_ea(j) :
            ea_total += j.needs
            ea_filled += cnt
        
        if is_ld(j) :
            ld_total += j.needs
            ld_filled += cnt

    writer.writerow([])
    writer.writerow(['Total Early Arrivals', str(ea_total)])
    writer.writerow(['Taken Early Arrivals', str(ea_filled)])
    writer.writerow(['Total Late Departures', str(ld_total)])
    writer.writerow(['Taken Late Departures', str(ld_filled)])
    
    return response
