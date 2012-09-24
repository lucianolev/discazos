from django.db import models

class AlbumReleaseDownloadSourceManager(models.Manager):
    def enabled_by_priority(self):
        enabled_globally = self.all().filter(service__enabled=True)
        enabled_specific = enabled_globally.filter(enabled=True)
        by_priority = sorted(enabled_specific, key=lambda ards: ards.service.priority)
        return by_priority