
from django.contrib.auth.forms import AuthenticationForm

#
# Override the built-in authentication form to fix the bug 
# that Jane reported: Her email address is longer than 30 characters 
#

class JanesForm(AuthenticationForm):
    
    def clean_username(self):
        return self.cleaned_data['username'][0:30]
    