from django.http import HttpResponseRedirect

from google.appengine.ext import ndb
from parser.StaffSheetLexer import StaffSheetLexer
from parser.StaffSheetParser import StaffSheetParser
from django.shortcuts import render_to_response
from models import Coordinator, Role, Job, Source
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

import os

from django.shortcuts import render
from django.http import HttpResponse
import textwrap


def default(request):
    source = Source.objects.order_by('title')
    if len(source) == 0 :
        response_text = textwrap.dedent('''
          <html>
          <head>
          <title>Be the Ball</title>
          </head>
          <body>
          <p>A flute with no hole is not a flute.</p>
          <p>A doughnut without a hole is a danish.</p>
          </body>
        </html>''')
        return HttpResponse(response_text)    

    coordinators = Coordinator.objects.filter(source__exact=source[0])
    jobs = Job.objects.filter(source__exact=source[0])
    template_values = {
        'source': source[0],
        'coordinators' : coordinators,
        'jobs' : jobs
    }
    return render_to_response('signup/jobpage.html', context=template_values)
