
from django.contrib.auth.decorators import user_passes_test
from signup.access import is_coordinator
from django.contrib.auth.models import User
from django.http import JsonResponse

@user_passes_test(lambda u: is_coordinator(u))
def email_suggest(request):
    users = User.objects.all()
    return JsonResponse({
        'items': list(map(lambda u: u.email, users))
    })
