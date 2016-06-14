from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django import forms
from django.forms import ModelForm
from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from models import Source, Role, Coordinator, Job
from parser.StaffSheetLexer import StaffSheetLexer
from parser.StaffSheetListener import StaffSheetListener
from parser.StaffSheetParser import StaffSheetParser
from django.db.utils import IntegrityError

from schema import build, build_all, ReportedException

from django.core.cache import cache

class SkipperForm(ModelForm):
    class Meta:
        model = Source
        fields = ['title', 'text']
        
    def clean(self):
        super(ModelForm, self).clean()
        try: 
            build(sourcetext=self.cleaned_data.get('text'), test_parse=True) 
        except ReportedException as e :
            raise ValidationError(
                _('Error: %(value)s'),
                params={'value': e.message},
            )

class BulkSourceForm(forms.Form):
    text = forms.CharField(label='text', widget=forms.Textarea({'cols': '80', 'rows': '40'}))
    def clean(self):
        super(BulkSourceForm, self).clean()
        try: 
            build_all(self.cleaned_data.get('text'), test_parse=True) 
        except ReportedException as e :
            raise ValidationError(
                _('Error: %(value)s'),
                params={'value': e.message},
            )

@user_passes_test(lambda u: u.is_superuser)
def source_list(request, template_name='source/source_list.html'):
    sources = Source.objects.order_by('title')
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
        
        # Now build it.
        build(sourceobj=source)

        # Make sure cached pages update
        cache.clear()                
        return redirect('source_list')
    return render(request, template_name, {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def source_update(request, pk, template_name='source/source_form.html'):    
    source = Source.objects.get(title=pk)
    if source == None :
        raise Http404("Source does not exist")

    form = SkipperForm(request.POST or None, instance=source)
    if form.is_valid():
        
        try: 
            with transaction.atomic() :
                # There is no update, sources must be deleted and remade.
                # on_delete=CASCADE is emulated, but it works when my objects don't suck. 
                source.delete()

                # Create a new one 
                source = form.save(commit=False)
                source.title = pk
                source.owner = request.user.username
                source.save()
        
                # Now build it.
                build(sourceobj=source)
        except IntegrityError as e:
            print "Transaction error:", e
        
        cache.clear()                
        return redirect('source_list')
    return render(request, template_name, {'form':form})

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
                    build_all(form.cleaned_data['text'])
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
