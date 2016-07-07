from models import Source, Coordinator, Global, global_signup_enable
from argparse import ArgumentError
from datetime import datetime 

EA_THRESHOLD = datetime.strptime('07/29/2016 13:00:00 UTC', '%m/%d/%Y %H:%M:%S %Z')
LD_THRESHOLD = datetime.strptime('07/31/2016 16:00:00 UTC', '%m/%d/%Y %H:%M:%S %Z')

# Test if the job or volunteer model is an early arrival job.
def is_ea(job):
    return job.start <= EA_THRESHOLD

# Test if the job or volunteer model is a late departure job.
# This works because the fields in Job and Volunteer are similarly named.
def is_ld(job):
    return job.end >= LD_THRESHOLD

# Test if the user has any form of administrative privileges
# This is true for
#   - Super users 
#   - People with staff access  
#   - People who's email address is listed in a coordinator role.
#
def is_coordinator(user):
    if user.is_anonymous() :
        return False;
    
    return user.is_superuser or user.is_staff \
        or Coordinator.objects.filter(email__exact=user.email).count() > 0 

# Test if the user is the coordinator of a particular role. 
# This is used to restrict coordinator access to only the roles for 
# which they are responsible. This tests true for: 
#   - Super users
#   - People with staff access 
#   - Coordinators who's email address is listed in the role given
#
def is_coordinator_of(user, source):
    if user.is_anonymous() :
        return False;

    return user.is_superuser or user.is_staff \
        or Coordinator.objects.filter(email__exact=user.email, source__exact=source.pk).count() > 0

# Test if a user is able to signup for a job, taking into account the 
# global singup enable. The following conditions must be met:
#
# - Singups are always barred if there are no slots left. This function DOES NOT
#   check if the job is full. That's the responsibility of the caller.
# - Superusers are always able to signup for an available job (this is for testing) 
#
# If GSE is in the COORDINATOR_ONLY state: 
#   - A coordinator can singup if:
#         the job is protected or is early arrival or is late departure
#
# If GSE is in the AVAILABLE state: 
#   - If the job is protected a coordinator can signup
#   - Otherwise, anyone can. 
#
def can_signup(user, job):
    if user.is_anonymous() :
        return False;

    if user.is_superuser :
        return True
    
    gse = global_signup_enable()
    if gse == Global.COORDINATOR_ONLY :
        if (job.protected or is_ea(job) or is_ld(job)) and is_coordinator(user) :
            return True
        else:
            return False
    else:
        if job.protected :
            if is_coordinator_of(user, job.source) :
                return True
            else:
                return False
        else:
            return True
    
    # Never get here  
    raise ArgumentError("Failed to fully decode permissions in can_signup()")

# Test if the user can delete the specified volunteer signup. 
# The following conditions must be met: 
# 
# - The superuser can delete anything
# - A coordinator can delete a job for the role that they are the coordinator for
# - A user can delete their own signups. 
#
def can_delete(user, volunteer):
    if user.is_anonymous() :
        return False;

    if user.is_superuser :
        return True
    
    return (volunteer.user == user) or is_coordinator_of(user, Source.objects.get(pk=volunteer.source))
