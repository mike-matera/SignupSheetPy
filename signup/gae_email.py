from google.appengine.api import mail
from google.appengine.api import app_identity
from django.core.mail.backends.base import BaseEmailBackend

class GAEEmailBackend (BaseEmailBackend):
    
    def send_messages(self, email_messages):
        for message in email_messages : 
            print "Sending message to:", message.to
            mail.send_mail(sender='{}@appspot.gserviceaccount.com'.format(app_identity.get_application_id()), 
                           to=message.to, 
                           subject=message.subject, 
                           body=message.body
                           )
        