import urllib

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.urlencode(kwargs)

def paginate(request, objects, range):
    paginator = Paginator(objects, range)

    page = request.GET.get('page')
    try:
        objects_with_pagination = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects_with_pagination = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects_with_pagination = paginator.page(paginator.num_pages)
    return objects_with_pagination