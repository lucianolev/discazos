import math

from django import template

register = template.Library()

@register.filter()
def format_secs(s):
    mins = math.floor(int(s) / 60);
    secs = math.floor(int(s) - (mins * 60)); 
    return "%d:%02d" % (mins, secs);