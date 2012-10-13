from django.contrib import admin

from albums.models import *

# Main reusable Admin class for only viewing
class ViewAdmin(admin.ModelAdmin):

    """
    Custom made change_form template just for viewing purposes
    You need to copy this from /django/contrib/admin/templates/admin/change_form.html
    And then put that in your template folder that is specified in the 
    settings.TEMPLATE_DIR
    """
    #change_form_template = 'view_form.html'

    # Remove the delete Admin Action for this Model
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        #Return nothing to make sure user can't update any data
        pass

    def get_readonly_fields(self, request, obj=None):
        return tuple(obj._meta.get_all_field_names())

class ArtistAliasInline(admin.TabularInline):
    model = ArtistAlias
    extra = 0

class ArtistAdmin(admin.ModelAdmin):
    inlines = [ArtistAliasInline, ]

admin.site.register(GroupArtist, ArtistAdmin)
admin.site.register(PersonArtist, ArtistAdmin)

class ArtistAlbumAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'artist', )

admin.site.register(ArtistAlbum, ArtistAlbumAdmin)

admin.site.register(CompilationAlbum)

class AlbumReleaseDownloadSourceInline(admin.StackedInline):
    model = AlbumReleaseDownloadSource
    extra = 1

class AlbumReleaseAdmin(admin.ModelAdmin):
    inlines = [AlbumReleaseDownloadSourceInline, ]
    list_display = ('album', 'get_artist', 'uploaded_on', 'uploader', 
                    'get_available_download_sources', 'published' )
    def get_artist(self, obj):
        try:
            artistAlbum = ArtistAlbum.objects.get(pk=obj.album.pk)
            return u'%s' % artistAlbum.artist
        except:
            return ''
    get_artist.short_description = 'Artista'
    def get_available_download_sources(self, obj):
        return ', '.join(sorted([dls.__unicode__() for dls in 
                                 obj.download_sources.filter(enabled=True)]))
    get_available_download_sources.short_description = 'Fuentes de descarga disponibles'
    
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
    

class AlbumPlaybackLogEntryAdmin(ViewAdmin):
    list_display = ('date_and_time', 'user', 'album_release', 
                    'album_release_dl_source', 'output_message' )
    ordering = ('-date_and_time', )

admin.site.register(AlbumPlaybackLogEntry, AlbumPlaybackLogEntryAdmin)
