from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from dajaxice.decorators import dajaxice_register

from models import AlbumReleaseDownloadSource, AlbumPlaybackLogEntry

@dajaxice_register
def log_album_playback(request, album_release_dl_source_id, output_message):
    album_release_dl_source = get_object_or_404(AlbumReleaseDownloadSource, 
                                                pk=album_release_dl_source_id)
    aple = AlbumPlaybackLogEntry(user=request.user, 
                                 album_release=album_release_dl_source.album_release,
                                 output_message=output_message,
                                 album_release_dl_source=album_release_dl_source)
    aple.save()
    return None