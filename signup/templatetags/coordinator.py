from django import template
from signup.access import is_coordinator

register = template.Library()

@register.simple_tag(takes_context=True)
def is_coord(context):
    return is_coordinator(context['user'])
