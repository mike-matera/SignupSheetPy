from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4.error.Errors import ParseCancellationException, InputMismatchException
from django.contrib.auth.decorators import user_passes_test
from django.forms import ModelForm
from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from models import Source
from parser.StaffSheetLexer import StaffSheetLexer
from parser.StaffSheetParser import StaffSheetParser

from parser.StaffSheetListener import StaffSheetListener
from parser.StaffSheetLexer import StaffSheetLexer
from google.appengine.ext.admin import NoneType
from datetime import datetime
from datetime import timedelta
import re
from models import *
from _mysql import IntegrityError

class SchemaBuilder(StaffSheetListener) :
    
    epoch = datetime.strptime('06/29/2016', '%m/%d/%Y')
    
    def __init__(self):
        self.rows = []
        self.stack = []
        self.context = []
    
    def enterRolefragment(self, ctx): 
        self.context.append(ctx.sourceobj);
            
    def exitRolefragment(self, ctx):
        role = Role()
        role.source = self.context.pop()
        role.description = self.stack.pop()
        role.save() 
        # Now that the role exists, we can create the other rows
        # which have FK constraints 
        for row in self.rows :
            row.save()

        self.rows = []

    def exitCoordinator(self, ctx):
        coord = Coordinator()
        coord.source = self.context[-1]
        coord.name = self.__strToken(ctx.QUOTE(0))
        coord.email = self.__strToken(ctx.QUOTE(1))
        coord.url = self.__strToken(ctx.QUOTE(2))
        self.rows.append(coord)

    def exitDescription(self, ctx):
        self.stack.append(self.__strToken(ctx.QUOTE()))
        
    def exitJob(self, ctx):
        for slot in self.stack.pop() :
            job = Job()
            job.source = self.context[-1]
            job.title = self.__strToken(ctx.QUOTE(0))
            job.description = self.__strToken(ctx.QUOTE(1))
            job.start = slot['begin']
            job.end = slot['end']
            job.needs = 1            
            if ctx.needs() != None :
                job.needs = self.__intToken(ctx.needs().NUMBER())
            job.protected = False
            if ctx.getChild(0).getText() == 'protected' :
                job.protected = True
            self.rows.append(job)
                           
    def exitTimespec(self, ctx):
        times = [self.__timespecToken(x) for x in ctx.getTokens(StaffSheetLexer.TIME)]
        numbers = [int(x.getText()) for x in ctx.getTokens(StaffSheetLexer.NUMBER)]
        duration = self.stack.pop()
        slots = []
        if len(times) == 1 and len(numbers) == 1 : 
            # This is a count job
            for i in xrange(0, numbers[0]) :
                slot = {}
                slot['begin'] = times[0] + (duration * i)
                slot['end'] = slot['begin'] + duration
                slots.append(slot)
        elif len(times) == 2 :
            # This is an until job
            cursor = times[0]
            until = times[1]
            while cursor < until : 
                slot = {}
                slot['begin'] = times[0] + duration
                slot['end'] = slot['begin'] + duration
                slots.append(slot)
                cursor += duration 
        else:         
            slot = {}
            slot['begin'] = times[0]
            slot['end'] = slot['begin'] + duration
            slots.append(slot)

        self.stack.append(slots)

    def exitDuration(self, ctx):
        value = float(ctx.getToken(StaffSheetLexer.NUMBER, 0).getText())
        magnitude = ctx.getChild(2).getText()
        if magnitude[0:4] == 'hour' :
            self.stack.append(timedelta(hours=value))
        else:
            self.stack.append(timedelta(minutes=value))
        
    def __strToken(self, token) :
        if token is None:
            return ""
        
        s = token.getText();
        # Stip quotes 
        s = s[1:-1]
        # Trim 
        s = s.strip()
        return s
    
    def __intToken(self, token) :
        return int(token.getText())

    def __floatToken(self, token) :
        return float(token.getText())

    def __timespecToken(self, token):
        # Stip the junk @[ and ] off 
        spec = token.getText()
        spec = spec[2:-1]
        (day, time) = spec.split()
        d = 0
        h = 0
        m = 0
        if day[1:] == 'riday' :
            d = 0
        elif day[1:] == 'aturday' :
            d = 1
        elif day[1:] == 'unday' :
            d = 2
        elif day[1:] == 'onday' :
            d = 3
        elif day[1:] == 'uesday' :
            d = 4
        elif day[1:] == 'ednesday' :
            d = 5
        elif day[1:] == 'ursday' :
            d = 6
        else :
            raise ValueError("This date is fucked: " + spec)

        if time[1:] == 'idnight' :
            h = 0
        elif time[1:] == 'oon' :
            h = 12
        else :  
            regex = re.compile("(\d+):(\d+)\s*(am|pm)")
            matcher = regex.search(time)
            h = int(matcher.group(1))
            if matcher.group(3) == 'pm' :
                h += 12
            m = int(matcher.group(2))
        
        time = self.epoch + timedelta(days=d, minutes=m, hours=h)
        return time            

class ReportedException(ParseCancellationException) :
    def __init__(self, s, l) :
        self.symbol = s
        self.line = l 
        self.message = "Parse error on line " + str(self.line) + "."
        if s is not None :
            self.message = self.message + " Something went wrong around \"" + self.symbol.text + "\""
        
    def __str__(self):
        return "message " + self.message
        
class ValidateErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ReportedException(offendingSymbol, line)

class ValidationErrorStrategy(DefaultErrorStrategy):
    def recover(self, recognizer, e):        
        context = recognizer._ctx
        raise ReportedException(context.start, context.start.line)

    def recoverInline(self, recognizer):
        self.recover(recognizer, InputMismatchException(recognizer))

    def sync(self, recognizer):
        pass

def test_parse(sourcestring):
    text = InputStream(sourcestring)
    lexer = StaffSheetLexer(text)
    stream = CommonTokenStream(lexer)
    parser = StaffSheetParser(stream)
    
    strat = ValidationErrorStrategy()
    parser._errHandler = strat
    
    errs = ValidateErrorListener()
    parser.addErrorListener(errs)
    lexer.addErrorListener(errs)
    
    parser.rolefragment("testparse")

def build(source):
    text = InputStream(source.source)
    lexer = StaffSheetLexer(text)
    stream = CommonTokenStream(lexer)
    parser = StaffSheetParser(stream)
    tree = parser.rolefragment(source)
    builder = SchemaBuilder()
    ParseTreeWalker.DEFAULT.walk(builder, tree)

class SkipperForm(ModelForm):
    class Meta:
        model = Source
        fields = ['title', 'source']
        
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
        
        # Now build it.
        build(source)
                
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
                build(source)
        except IntegrityError as e:
            print "Transaction error:", e
        
        return redirect('source_list')
    return render(request, template_name, {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def source_delete(request, pk, template_name='source/confirm_delete.html'):
    source = Source.objects.get(title=pk)
    if source == None :
        raise Http404("Source does not exist")

    if request.method=='POST':
        source.delete()
        return redirect('source_list')
    
    return render(request, template_name, {'object':source})
