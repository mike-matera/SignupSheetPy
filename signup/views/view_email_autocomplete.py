from __future__ import print_function 

from django.contrib.auth.models import User

from django import forms
from django.http import HttpResponse
from django.core.cache import cache

import json 

class SignupFormUser(forms.Form):
    comment = forms.CharField(label='Comment', required=False)
    def clean(self):
        super().clean()

class SignupFormCoordinator(forms.Form):
    comment = forms.CharField(label='Comment', required=False)
    def clean(self):
        super().clean()

class XXSignupFormCoordinator(forms.Form):

    #def gen_choices():
    #    users = cache_fill()            
    #    return [ user['id'] for user in users ] 
    
    comment = forms.CharField(label='Comment', required=False)
    #email = autocomplete.Select2ListChoiceField(
    #            required=False,
    #            choice_list=gen_choices,
    #            widget=autocomplete.ListSelect2(
    #                url='email-autocomplete', 
    #                attrs={'data-html': True},
    #                ),
    #            )
