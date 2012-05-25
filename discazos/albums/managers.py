from django.db import models
import time

class DiscTrackManager(models.Manager):
    use_for_related_fields = True
    
    def for_playlist(self):
        tracks = []
        added_offset = 0
        for track in self.all():
            track_item = {'number': track.number, 'song': track.song.name,
                          'length': track.length }
            track_item['length_f'] = time.strftime('%M:%S', 
                                                   time.gmtime(track.length))
            track_item['offset'] = added_offset
            added_offset += track.length
            tracks.append(track_item)
        return tracks