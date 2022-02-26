"""
Views for our new React front-end
"""

import json 

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404

from signup.views.views import filterNavData, index

from signup.models import Coordinator, Job, Role, Volunteer, Global
from signup.access import is_coordinator, is_coordinator_of, can_signup, can_delete, is_ea, is_ld, EA_THRESHOLD, LD_THRESHOLD, global_signup_enable


@login_required
def react_jobs(request, title):
        
    # Fetch the role information 
    roles = Role.objects.filter(source__exact=title)
    if len(roles) == 0:
        raise Http404("That role was not found.")
    
    coordinators = []
    jobstaff = []
    role = {
        'title': title, 
        'status': roles[0].status,
        'contact': roles[0].contact,
        'description': roles[0].description,
        'coordinators': coordinators,
        'staff': jobstaff,
        'is_coordinator': is_coordinator_of(request.user, roles[0].source),
        'is_user': request.user.username,
    }
    for c in Coordinator.objects.filter(source__exact=title):
        if c.url == "" : 
            c.url = settings.COORDINATOR_DEFAULT_IMG
        elif c.url[0:4] != "http" :
            c.url = settings.COORDINATOR_STATIC_IMG_URL + c.url
        coordinators.append({
            'name': c.name,
            'email': c.email,
            'img': c.url,
        })

    for job in Job.objects.filter(source__exact=title).order_by('start'):
        entry = {
            'title': job.title,
            'start': job.start.strftime("%A %H:%M"), 
            'end': job.end.strftime("%A %H:%M"),
            'description': job.description,
            'needs': job.needs,
            'protected': job.protected,
        }
        entry['volunteers'] = []
        for vol in Volunteer.objects.filter(source__exact=job.source.pk, title__exact=job.title, start__exact=job.start).select_related('user'):
            entry['volunteers'].append({
                'username': vol.user.username,
                'first_name': vol.user.first_name,
                'last_name': vol.user.last_name,
                'comment': vol.comment,
            })
                 
        jobstaff.append(entry)
    

    context = {
        'data': json.dumps(role),
    }
    return render(request, 'react/jobpage.html', context={'data': role})