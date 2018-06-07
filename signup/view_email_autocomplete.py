from __future__ import print_function 

from dal import autocomplete

from django.contrib.auth.models import User

from django import forms

class EmailAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return User.objects.none()
    
        qs = User.objects.all()

        if self.q:
            qs = qs.filter(email__icontains=self.q)

        return qs

class SignupFormUser(forms.Form):
    comment = forms.CharField(label='Comment', required=False)
    def clean(self):
        super(SignupFormUser, self).clean()

class SignupFormCoordinator(forms.Form):
    comment = forms.CharField(label='Comment', required=False)
    email = forms.ModelChoiceField(
                required=False,
                queryset=User.objects.all(),
                widget=autocomplete.ModelSelect2(url='email-autocomplete'))

    
