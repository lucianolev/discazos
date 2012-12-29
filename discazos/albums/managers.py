from django.db import models

class ArtistAlbumManager(models.Manager):
    
    def published(self):
        return self.filter(releases__published=True)

class AlbumReleaseDownloadSourceManager(models.Manager):
    
    def successful_loads(self):
        return self.filter(playback_log_entries__loading_status__contains='LOADING_')
    
    def enabled_by_priority(self):
        enabled_globally = self.all().filter(service__enabled=True)
        enabled_specific = enabled_globally.filter(enabled=True)
        by_priority = sorted(enabled_specific, key=lambda ards: ards.service.priority)
        return by_priority