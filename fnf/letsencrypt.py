from django.http import HttpResponse

def challenge(request, challenge):    
    response = HttpResponse(content_type='text/plain')
    responses = {
                'fucker': 'sucker',
                'Tc-qmLkx2jjrbYrvMwl3kZO1JEhVWLveTcF9WnOPNhA': 'Tc-qmLkx2jjrbYrvMwl3kZO1JEhVWLveTcF9WnOPNhA.AUhfaXJZOjhHN5mhMeY5tm0AKAn6F01vOJL5C72z4h8'
            }
    response.write(responses.get(challenge, ''))
    return response
