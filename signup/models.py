from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.db.models.fields import (
    TextField, CharField, EmailField, URLField, DateTimeField, IntegerField, BooleanField
)
from datetime import datetime


# Create your models here.
class Source(models.Model):
    '''This is the source code used to generate the staff sheet'''
    title = CharField("Coordinator Role Name", max_length=64, primary_key=True)
    text = TextField(default='''
coordinator "Name" "" ""

description {
}
    ''');
    version = DateTimeField("Changed On", auto_now_add=True)
    owner = CharField("Changed By", 
        max_length=64
    )

class Role(models.Model):
    '''The parsed Role'''
    source = models.OneToOneField(
        Source,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    description = TextField()

# XXX: Fix me Coordinator and Job should have Source as their FK
class Coordinator(models.Model):
    '''A coordinator in one role.''' 
    source = ForeignKey(Source, on_delete=models.CASCADE)
    name = CharField(max_length=64)
    email = EmailField()
    url = URLField()

class Job(models.Model):
    '''An individual job''' 
    source = ForeignKey(Source, on_delete=models.CASCADE)
    title = CharField(max_length=64)
    start = DateTimeField() 
    end = DateTimeField()
    description = TextField()
    needs = IntegerField()
    protected = BooleanField()
    
class Volunteer(models.Model):
    '''
    A volunteer in a role
    
    The volunteer must be able to join with Job, but it cannot use a public key.
    Recompiling the Role source will delete Coordinators and Jobs, but should not
    delete the people who have already signed up. Instead they should be joined 
    with the natural key of Job which is (role, title, start). This is a shitty
    join, if it's too slow I can probably figure out how to use hashes as the PK
    for Volunteer and Job
    '''
    user = ForeignKey(User)
    
    # The natural key of Job 
    source = CharField(max_length=64)
    title = CharField(max_length=64)
    start = DateTimeField()
    
    # Not used in the join, just so that overlaps can be detected
    end = DateTimeField(default=datetime.now)
    # --- 
    
    name = CharField(max_length=64)
    comment = TextField()
    