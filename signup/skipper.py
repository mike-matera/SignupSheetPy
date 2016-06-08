from django.http import HttpResponseRedirect

from google.appengine.ext import ndb
from parser.StaffSheetLexer import StaffSheetLexer
from parser.StaffSheetParser import StaffSheetParser
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from django.shortcuts import render, redirect
from django.forms import ModelForm

from models import Source
from django.http import Http404

from django.contrib.auth.decorators import user_passes_test
from django.core import validators
from django.forms import TextInput, ValidationError
from django.utils.translation import gettext_lazy as _

import os
from webapp2 import Request

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from parser.util import test_parse, ReportedException
from django.db.models.fields import TextField, CharField
from django.core import validators
    
class SkipperForm(ModelForm):
    class Meta:
        model = Source
        fields = ['role', 'source']
        
    def clean(self):
        super(ModelForm, self).clean()
        try: 
            test_parse(self.cleaned_data.get('source')) 
        except ReportedException as e :
            raise ValidationError(
                _('Error: %(value)s'),
                params={'value': e.message},
            )

@user_passes_test(lambda u: u.is_superuser)
def source_list(request, template_name='source/source_list.html'):
    sources = Source.objects.all()
    data = {}
    data['object_list'] = sources
    return render(request, template_name, data)

@user_passes_test(lambda u: u.is_superuser)
def source_create(request, template_name='source/source_form.html'):
    form = SkipperForm(request.POST or None)
    if form.is_valid():
        source = form.save(commit=False)
        source.owner = request.user.username
        source.save()
        return redirect('source_list')
    return render(request, template_name, {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def source_update(request, pk, template_name='source/source_form.html'):    
    source = Source.objects.get(role=pk)
    if source == None :
        raise Http404("Source does not exist")

    form = SkipperForm(request.POST or None, instance=source)
    if form.is_valid():
        source = form.save(commit=False)
        source.owner = request.user.username
        source.save()
        return redirect('source_list')
    return render(request, template_name, {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def source_delete(request, pk, template_name='source/confirm_delete.html'):
    source = Source.objects.get(role=pk)
    if source == None :
        raise Http404("Source does not exist")

    if request.method=='POST':
        if "submit" in request.POST['submit'] :
            source.delete()
        return redirect('source_list')
    
    return render(request, template_name, {'object':source})
