from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from dajaxice.decorators import dajaxice_register

from models import AlbumReleaseDownloadSource, AlbumPlaybackLogEntry

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