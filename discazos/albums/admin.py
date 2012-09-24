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

class ArtistAlbumAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'artist', )

admin.site.register(ArtistAlbum, ArtistAlbumAdmin)

admin.site.register(CompilationAlbum)

class AlbumReleaseDownloadSourceInline(admin.StackedInline):
    model = AlbumReleaseDownloadSource
    extra = 1

class AlbumReleaseAdmin(admin.ModelAdmin):
    inlines = [AlbumReleaseDownloadSourceInline, ]
    list_display = ('album', 'get_artist', 'main_release', 'uploaded_on', )
    def get_artist(self, obj):
        try:
            artistAlbum = ArtistAlbum.objects.get(pk=obj.album.pk)
            return u'%s' % artistAlbum.artist
        except:
            return ''
    get_artist.short_description = 'Artist'
    
    ordering = ('album', )

admin.site.register(AlbumRelease, AlbumReleaseAdmin)

class DiscTrackInline(admin.TabularInline):
    model = DiscTrack
    extra = 0
    
class DiscAdmin(admin.ModelAdmin):
    inlines = [DiscTrackInline, ]
    list_display = ('album_release', '__unicode__', )
    list_display_links = ('__unicode__', )
    ordering = ('album_release', )

admin.site.register(Disc, DiscAdmin)

class FileHostingServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled', 'priority', )
    list_editable = ('priority', )

    class Media:
        js = (
              'js/jquery.min.js',
              'js/jquery-ui.min.js',
              'js/admin-list-reorder.js',
        )

admin.site.register(FileHostingService, FileHostingServiceAdmin)
    
