from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django import forms
from django.forms import ModelForm
from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from models import Source, Role, Coordinator, Job, Global, global_signup_enable
from parser.StaffSheetLexer import StaffSheetLexer
from parser.StaffSheetListener import StaffSheetListener
from parser.StaffSheetParser import StaffSheetParser
from django.db.utils import IntegrityError

from schema import build, build_all, ReportedException

from django.core.cache import cache
from signup.models import set_global_signup_enable

from access import is_coordinator, is_coordinator_of

class SkipperForm(forms.Form):
    title = forms.CharField(label='title')
    text = forms.CharField(label='text', widget=forms.Textarea({'cols': '80', 'rows': '30'}))
    
    def clean(self):
        super(SkipperForm, self).clean()
        try: 
            build(user=None, sourcetext=self.cleaned_data.get('text'), test_parse=True) 
        except ReportedException as e :
            raise ValidationError(
                _('Error: %(value)s'),
                params={'value': e.message},
            )

class BulkSourceForm(forms.Form):
    text = forms.CharField(label='text', widget=forms.Textarea({'cols': '80', 'rows': '30'}))
    def clean(self):
        super(BulkSourceForm, self).clean()
        try: 
            build_all(self.cleaned_data.get('text'), test_parse=True) 
        except ReportedException as e :
            raise ValidationError(
                _('Error: %(value)s'),
                params={'value': e.message},
            )

class SourceLockForm(forms.Form):
    lock = forms.IntegerField(label='Global Signup Enable', widget=forms.RadioSelect(choices=Global.CHOICES))
    
@user_passes_test(lambda u: is_coordinator(u))
def source_list(request, template_name='source/source_list.html'):
    data = {}
    data['object_list'] = []
    data['signup_enable'] = global_signup_enable()    
    for s in Source.objects.order_by('title') :
        if is_coordinator_of(request.user, s) :
            data['object_list'].append(s)

    return render(request, template_name, data)

@user_passes_test(lambda u: is_coordinator(u))
def source_create(request, template_name='source/source_form.html'):
    if request.method == 'POST' :
        form = SkipperForm(request.POST)
        if form.is_valid():
            source = Source()
            source.text = form.cleaned_data['text']
            source.title = form.cleaned_data['title']
            source.owner = request.user.username
            source.save()
        
            # Now build it.
            build(user=request.user.username, sourceobj=source)

            # Make sure cached pages update
            cache.clear()                
            return redirect('source_list')
        else:
            return render(request, template_name, {'form':form})            
    else:
        default = '''
coordinator "Name" "Email" "Url"

description {
}
    ''' 
        form = SkipperForm( {'text': default, 'title': 'New Role'} )    
        return render(request, template_name, {'form':form})

@user_passes_test(lambda u: is_coordinator(u))
def source_update(request, pk, template_name='source/source_form.html'):    
    source = Source.objects.get(title=pk)
    if source == None :
        raise Http404("Source does not exist")

    if request.method=='POST':
        form = SkipperForm(request.POST)
        if form.is_valid():
        
            try: 
                with transaction.atomic() :
                    # There is no update, sources must be deleted and remade.
                    # on_delete=CASCADE is emulated, but it works when my objects don't suck. 
                    source.delete()

                    # Create a new one 
                    source = Source()
                    source.title = pk
                    source.text = form.cleaned_data['text']
                    source.owner = request.user.username
                    source.save()
        
                    # Now build it.
                    build(user=request.user.username, sourceobj=source)
            except IntegrityError as e:
                print "Transaction error:", e
        
            cache.clear()                
            return redirect('source_list')
        else:
            return render(request, template_name, {'title': pk, 'form':form})

    else:
        form = SkipperForm({'text': source.text, 'title': source.title})
        return render(request, template_name, {'title': pk, 'form':form})

@user_passes_test(lambda u: u.is_superuser)
def source_delete(request, pk, template_name='source/confirm_delete.html'):
    source = Source.objects.get(title=pk)
    if source == None :
        raise Http404("Source does not exist")

    if request.method=='POST':
        source.delete()
        cache.clear()                
        return redirect('source_list')
    
    return render(request, template_name, {'object':source})


@user_passes_test(lambda u: u.is_superuser)
def source_all(request, template_name='source/source_bulkedit.html'):
    
    if request.method=='POST':
        form = BulkSourceForm(request.POST)
        if form.is_valid():
            try: 
                with transaction.atomic() :
                    # Remake ALL source ojbects based on top source.
                    Source.objects.all().delete()
        
                    # Now build it.
                    build_all(form.cleaned_data['text'], request.user.username)
            except IntegrityError as e:
                print "Transaction error:", e

            cache.clear()                
            return redirect('source_list')
        else:
            return render(request, template_name, {'form':form})
    else:
        ## Fetch and unify the source 
        sources = Source.objects.order_by('title')
        text = ""
        for source in sources : 
            text += 'role "' + source.title + "\" (\n" + source.text + "\n)\n\n"
        
        form = BulkSourceForm({'text': text})
        return render(request, template_name, {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def source_lock(request, template_name='source/source_lockform.html') :

    if request.method == 'POST' :
        form = SourceLockForm(request.POST)
        if form.is_valid() : 
            set_global_signup_enable(form.cleaned_data['lock'])            
            return redirect('source_list')
        else:
            return render(request, template_name, {'form': form})
    else:
        form = SourceLockForm({'lock': global_signup_enable()})
        return render(request, template_name, {'form': form})
