from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import TextField, DateTimeField, CharField
from django.db.models import ForeignKey
from django.contrib.auth.models import User
from django.forms import HiddenInput

# Create your models here.
class Source(models.Model):
    '''This is the source code used to generate the staff sheet'''
    role = CharField("Coordinator Role Name", max_length=32, primary_key=True)
    source = TextField()
    version = DateTimeField("Changed On", auto_now_add=True)
    owner = CharField("Changed By", 
        max_length=32
    )
