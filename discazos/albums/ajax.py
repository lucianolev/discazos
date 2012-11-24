from django.conf import settings
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Q

from dajaxice.decorators import dajaxice_register
from sorl.thumbnail import get_thumbnail

from discazos.utils.view_helpers import url_with_querystring

from models import AlbumReleaseDownloadSource, AlbumPlaybackLogEntry, ArtistAlbum

def global_album_search(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        albums = ArtistAlbum.objects.published()
        matched_albums = albums.filter(Q(title__icontains=query) | 
                                       Q(artist__name__icontains=query))
        results_limit = settings.ALBUM_SEARCH_RESULTS_LIMIT
        matched_albums_limited = matched_albums[:results_limit]
        results_list = [{ 'type': 'album',
                          'url': reverse("album_view", args=(album.pk, )),
                          'title': album.title, 
                          'artist': album.artist.name,
                          'cover_url': get_thumbnail(album.main_release.cover, '64x64').url
                        } for album in matched_albums_limited]
        if matched_albums.count() > results_limit:
            results_list.append({ 'type': 'more-link', 
                                  'url': url_with_querystring(reverse("albums_list"), 
                                                              q=query) 
                                })
    return HttpResponse(simplejson.dumps(results_list), 
                        mimetype="application/json")

@dajaxice_register
def add_log_album_playback(request, album_release_dl_source_id):
    album_release_dl_source = get_object_or_404(AlbumReleaseDownloadSource, 
                                                pk=album_release_dl_source_id)
    aple = AlbumPlaybackLogEntry(user=request.user, 
                                 album_release=album_release_dl_source.album_release,
                                 album_release_dl_source=album_release_dl_source)
    aple.save()
    return simplejson.dumps({'apleId': aple.pk})

@dajaxice_register
def update_log_album_playback(request, aple_id, loading_status, extra_debug_info=None):
    aple = get_object_or_404(AlbumPlaybackLogEntry, pk=aple_id)
    aple.loading_status = loading_status
    if extra_debug_info:
        aple.extra_debug_info = extra_debug_info
    aple.save()
    return None