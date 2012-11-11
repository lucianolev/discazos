import urllib

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.urlencode(kwargs)

def paginate(request, objects, range):
    paginator = Paginator(objects, range)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        objects_with_pagination = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects_with_pagination = paginator.page(paginator.num_pages)
    return objects_with_pagination