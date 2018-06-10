from __future__ import print_function 

from dal import autocomplete

from django.contrib.auth.models import User

from django import forms
from django.http import HttpResponse
from django.core.cache import cache

import json 

class EmailAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return User.objects.none()
    
        qs = User.objects.all()

        if self.q:
            qs = qs.filter(email__icontains=self.q)

        return qs

class UserAutocomplete(autocomplete.Select2ListView):

    # Override to fix a bug
    def get(self, request, *args, **kwargs):
        """"Return option list json response."""
        results = self.get_list()
        create_option = []
        if self.q:
            if hasattr(self, 'create'):
                create_option = [{
                        'id':self.q, 
                        'text':'Create "%s"' % self.q, 
                        'create_id':True}]
        return HttpResponse(json.dumps({
            'results' : results + create_option
            }), content_type = 'application/json')

            
    def get_list(self):
        if not self.request.user.is_authenticated():
            return []

        if self.q is None or self.q == '' : 
            return [] 
            
        users = cache.get('users_lookup')
        if users is None :
            users = []
            qs = User.objects.all()
            for user in qs : 
                users.append(dict(id = user.email, text = user.first_name + ' ' + user.last_name + ' (' + user.email + ')'))
            users.sort(key=lambda x : x['text'].lower())
            cache.set('users_lookup', users, 600)
            
        return [user for user in users if self.q.lower() in user['text'].lower() ]


class SignupFormUser(forms.Form):
    comment = forms.CharField(label='Comment', required=False)
    def clean(self):
        super(SignupFormUser, self).clean()

class SignupFormCoordinator(forms.Form):

    def gen_choices():
        print ('Generating choices...')
        return [user.email for user in User.objects.all()]
    
    comment = forms.CharField(label='Comment', required=False)
    email = autocomplete.Select2ListChoiceField(
                required=False,
                choice_list=gen_choices,
                widget=autocomplete.ListSelect2(
                    url='email-autocomplete', 
                    attrs={'data-html': True},
                    ),
                )
