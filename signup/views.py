from django.shortcuts import render
from django.http import HttpResponse
import textwrap

# Create your views here.
def hello(request):
    response_text = textwrap.dedent('''\
        <html>
        <head>
            <title>Greetings to the world</title>
        </head>
        <body>
            <h1>Greetings to the world</h1>
            <p>Hello, world!</p>
        </body>
        </html>
    ''')
    return HttpResponse(response_text)