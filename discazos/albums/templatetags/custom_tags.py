import math

from django import template

register = template.Library()

@register.filter()
def format_secs(ms):
    s = int(ms) / 1000
    mins = math.floor(s / 60)
    secs = math.floor(s - (mins * 60)) 
    return "%d:%02d" % (mins, secs)