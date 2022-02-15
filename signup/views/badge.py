from signup.models import Coordinator, Job, Role, Volunteer, Global

def badgeFor(role, jobcount, personcount) :
    ent = {}
    needed = jobcount - personcount
    
    if role.status == Role.WORKING :
        ent['pic'] = 'OrangeConstruction.png'
        ent['alt'] = 'Under construction.'
    elif role.status == Role.DISABLED :
        ent['pic'] = 'GrayDoNotEnter.png'
        ent['alt'] = 'Temporarily disabled.'
    elif jobcount == personcount : 
        ent['pic'] = 'GreenCheck.png'
        ent['alt'] = 'All jobs filled'
    elif jobcount == personcount + 1:
        ent['alt'] = str(needed) + ' needed'
        ent['pic'] = 'GreenCircle.png'  
    else :
        if jobcount == 0:
            percent = 0
        else:
            percent = personcount / float(jobcount)
                        
        ent['alt'] = str(needed) + ' needed'
        if percent < 0.25 :
            ent['pic'] = 'RedExclam.png'
        elif percent < 0.9 :
            ent['pic'] = 'YellowCircle.png'
        else :
            ent['pic'] = 'GreenCircle.png'  
    
    return ent
