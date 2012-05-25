from django.contrib import admin

from albums.models import *

class ArtistAliasInline(admin.TabularInline):
    model = ArtistAlias
    extra = 0

class ArtistAdmin(admin.ModelAdmin):
    inlines = [ArtistAliasInline, ]

admin.site.register(GroupArtist, ArtistAdmin)
admin.site.register(PersonArtist, ArtistAdmin)

admin.site.register(Song)
admin.site.register(ArtistAlbum)
admin.site.register(CompilationAlbum)

class AlbumReleaseDownloadSourceInline(admin.StackedInline):
    model = AlbumReleaseDownloadSource
    extra = 1

class AlbumReleaseAdmin(admin.ModelAdmin):
    inlines = [AlbumReleaseDownloadSourceInline, ]

admin.site.register(AlbumRelease, AlbumReleaseAdmin)

class DiscTrackInline(admin.TabularInline):
    model = DiscTrack
    extra = 0
    
class DiscAdmin(admin.ModelAdmin):
    inlines = [DiscTrackInline, ]
    list_display = ('__unicode__', 'album_release')

admin.site.register(Disc, DiscAdmin)
