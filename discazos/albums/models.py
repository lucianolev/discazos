# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.formats import date_format

from django_countries import CountryField

from managers import *

'''
An artist. 
It's not used directly but through group/person artist
'''
class Artist(models.Model):
    class Meta:
        verbose_name = u'Artista'
        verbose_name_plural = u'Artistas'
        ordering = ['name', ]

    name = models.CharField(u'nombre', max_length=255)
    country = CountryField(u'país', blank=True, null=True)
    image = models.ImageField(u'imagen del artista', upload_to='uploads/artists', 
                              blank=True, null=True)
    #official_site = models.URLField(blank=True)
    #youtube_profile = models.URLField(blank=True)
    #wikipedia = models.URLField(u'wikipedia', blank=True)
    
    def __unicode__(self):
        return u"%s" % self.name

#The person and group artist distinction make sense for
#a richer music library information 
class PersonArtist(Artist):
    class Meta:
        verbose_name = u'Artista (Persona)'
        verbose_name_plural = u'Artistas (Personas)'

class GroupArtist(Artist):
    class Meta:
        verbose_name = u'Artista (Grupo)'
        verbose_name_plural = u'Artistas (Grupos)'
    
    members = models.ManyToManyField(PersonArtist, verbose_name=u'miembros', 
                                     related_name='groups', blank=True)
    past_members = models.ManyToManyField(PersonArtist, verbose_name=u'miembros anteriores', 
                                          related_name='past_groups', blank=True)

#Many artist have multiple known names so this make sense
#for smart searches
class ArtistAlias(models.Model):
    class Meta:
        verbose_name = u'Alias'
        verbose_name_plural = u'Alias'
    
    artist = models.ForeignKey(Artist, verbose_name=u'artista', related_name='aliases')
    name = models.CharField(u'nombre', max_length=255)
    
    def __unicode__(self):
        return u"%s" % self.name

'''
An album.
This represent an album as composition performed by one or more artist
An album can have many releases along history which may vary
depending on the country.
It's not used directly but through artist and compilation album.
'''
class Album(models.Model):
    class Meta:
        verbose_name = u'Álbum'
        verbose_name_plural = u'Álbumes'
        ordering = ['title', ]

    RECORDING_TYPES = (
        ('ST', 'Estudio'),
        ('LV', 'En vivo')
    )
    
    title = models.CharField(u'título', max_length=255)
    #wikipedia = models.URLField(u'wikipedia', blank=True)
    recording_type = models.CharField(u'tipo de grabación', choices=RECORDING_TYPES, max_length=2, default='ST')
    #status? Official, bootleg
    
    @classmethod
    def create(cls, session_data):
        newAlbum = cls(**session_data)
        newAlbum.save()
        return newAlbum
    
    @property
    def main_release(self):
        return self.releases.filter(main_release=True)[0]
    
    def __unicode__(self):
        return  u"%s" % self.title

#A typical album performed by a single artist
class ArtistAlbum(Album):
    class Meta:
        verbose_name = u'Álbum'
        verbose_name_plural = u'Álbumes'
    
    artist = models.ForeignKey(Artist, verbose_name=u'artista', related_name='albums')
    
    objects = ArtistAlbumManager()

#A compilation album which includes tracks of various artists
class CompilationAlbum(Album):
    class Meta:
        verbose_name = u'Álbum Compilado'
        verbose_name_plural = u'Álbumes Compilados'

#User ratings of an album
#class AlbumRating(models.Model):
#    album = models.ForeignKey(Album, related_name='ratings')
#    value = models.PositiveSmallIntegerField() #1 to 5
#    comment = models.TextField(blank=True)
#    user = models.ForeignKey(User, related_name='ratings')
#    
#    def __unicode__(self):
#        return self.value

'''
An album release. A.K.A a Discazo.
Represents a concrete release of an album.
'''
class AlbumRelease(models.Model):
    class Meta:
        verbose_name = 'Álbum (Edición)'
        verbose_name_plural = 'Álbumes (Ediciones)'

    QUALITY_TYPES = (
        ('SQ', 'SQ'),
        ('HQ', 'HQ'),
    )

    album = models.ForeignKey(Album, verbose_name=u'álbum', 
                              related_name='releases')
    release_year = models.IntegerField(u'año de lanzamiento', max_length=4)
    cover = models.ImageField(u'tapa', upload_to='uploads/covers/')
    main_release = models.BooleanField(u'¿Edición principal?')
    release_extra_info = models.CharField(u'información extra de la edición', max_length=255, 
                                    blank=True)
    
    uploaded_on = models.DateTimeField(u'subido el', auto_now_add=True)
    uploader = models.ForeignKey(User, verbose_name=u'subido por', 
                                 related_name='uploadings')
    stream_quality = models.CharField(u'calidad de audio', choices=QUALITY_TYPES, 
                                      max_length=2, default='SQ', blank=True)
    audiofile_size = models.BigIntegerField(u'peso del archivo de audio') #In bytes
    
    published = models.BooleanField(u'publicado', default=True)

    @classmethod
    def create_main_release(cls, session_data, user, album, audiofile_size):
        albumReleaseData = session_data
        albumReleaseData.update({'album': album, 
                                 'main_release': True,
                                 'uploader': user,
                                 'audiofile_size': audiofile_size,
                                 'published': True,
                                 })
        newAlbumRelease = cls(**albumReleaseData)
        newAlbumRelease.save()
        return newAlbumRelease

    def __unicode__(self):
        album_name = u"%s" % self.album + " (" + u"%s" % self.release_year
        if self.release_extra_info:
            album_name += " - " + u"%s" % self.release_info
        album_name += ")"
        return album_name
    
    def length(self):
        length = 0
        for disc in self.discs.all():
            for track in disc.tracks.all():
                length += track.length
        return length
    
    def playlist(self):
        import time
        discs_playlist = []
        added_offset = 0
        for disc in self.discs.all():
            tracks = []
            for track in disc.tracks.all():
                track_item = {'number': track.number, 'song': track.song_name,
                              'length': track.length }
                track_item['offset'] = added_offset
                added_offset += track.length
                tracks.append(track_item)
            discs_playlist.append({ 'disc': disc, 'tracks_playlist': tracks })
        return discs_playlist
    
    def has_sources(self):
        return self.download_sources.filter(enabled=True).exists()

#A download source for an album release
class AlbumReleaseDownloadSource(models.Model):
    class Meta:
        verbose_name = u'Fuente de descarga'
        verbose_name_plural = 'Fuentes de descarga'
    
    album_release = models.ForeignKey(AlbumRelease, verbose_name=u'álbum (edición)', 
                                      related_name='download_sources')
    service = models.ForeignKey('FileHostingService', verbose_name=u'servicio')
    download_link = models.URLField(u'link de descarga')
    enabled = models.BooleanField(u'Disponible', default=True)

    def last_successful_load(self):
        successful_loads = self.playback_log_entries.filter(loading_status__contains='LOADING_')
        latest_datetime = successful_loads.latest('date_and_time').date_and_time
        return u"%s" % date_format(latest_datetime, 'DATETIME_FORMAT')

    @classmethod
    def create(cls, session_data, album_release):
        sourceData = session_data
        sourceData.update({'album_release': album_release})
        newDownloadSource = cls(**sourceData)
        newDownloadSource.save()
        return newDownloadSource

    def __unicode__(self):
        return u"%s" % self.service
    
    objects = AlbumReleaseDownloadSourceManager()

'''
An album release disc.
'''
class Disc(models.Model):
    class Meta:
        verbose_name = u'Disco'
        verbose_name_plural = u'Discos'
        ordering = ['number', ]
    
    album_release = models.ForeignKey(AlbumRelease, verbose_name=u'álbum (edición)', 
                                      related_name='discs')
    number = models.PositiveSmallIntegerField(u'número', default=1)
    title = models.CharField(u'título del disco (si tiene)', max_length=255, blank=True)

    @classmethod
    def create_with_release(cls, session_data, album_release):
        discData = session_data
        discData.update({'album_release': album_release })
        newDisc = cls(**discData)
        newDisc.save()
        return newDisc

    def __unicode__(self):
        disc_name = "CD " + u"%s" % self.number
        if (self.title):
            disc_name += " - " + u"%s" % self.title
        return disc_name

class DiscTrack(models.Model):
    class Meta:
        verbose_name = u'Pista de disco'
        verbose_name_plural = u'Pistas de discos'
        ordering = ['number', ]
    
    disc = models.ForeignKey(Disc, verbose_name=u'disco', 
                             related_name='tracks')
    number = models.PositiveSmallIntegerField(u'número', default=1)
    artist = models.ForeignKey(Artist, verbose_name=u'artista', 
                               related_name='recordings')
    song_name = models.CharField(u'canción', max_length=255)
    length = models.PositiveIntegerField(u'duración (ms)')
    
    @classmethod
    def create_from_assistant(cls, session_data, disc):
        trackData = session_data
        artist = Artist.objects.get(name=session_data['artist'])
        trackData.update({'disc': disc, 
                          'artist': artist})
        newTrack = cls(**trackData)
        newTrack.save()
        return newTrack
    
    def __unicode__(self):
        return u"%s" % self.song_name

class FileHostingService(models.Model):
    class Meta:
        verbose_name = u'Servicio de alojamiento de archivos'
        verbose_name_plural = u'Servicios de alojamiento de archivos'
        ordering = ['priority', ]
        
    
    name = models.CharField(u'nombre', max_length=100)
    priority = models.IntegerField(u'prioridad')
    enabled = models.BooleanField(u'Habilitado?', default=True)

    def __unicode__(self):
        return u"%s" % self.name

class AlbumPlaybackLogEntry(models.Model):
    class Meta:
        verbose_name = u'Entrada del log de reproducciones'
        verbose_name_plural = u'Log de reproducciones'

    LOADING_STATUSES = (
        # In Discazos Loader
        ('DOWNLOAD_SOURCE_OPENED', 'ERROR: (1) Halted after choosing FH. Probably FH-CS not loaded correctly.'),
        ('DL_FETCH_INIT', 'ERROR: (2) Halted after download link fetching started (FH-CS succesfully loaded).'),
        ('WAITING_IN_EFFECT', 'INFO: (3) Waiting time in effect.'),
        ('CAPTCHA', 'WARN: (3) Stopped at Captcha.'),
        ('DL_NOT_AVAILABLE', 'WARN: (3) Download link not available.'),
        ('COUNTDOWN_INIT', 'WARN: (3.1) Halted after succesfully countdown start, before it ended.'),
        ('COUNTDOWN_END', 'ERROR: (3.2) Halted on afterCountdown callback, before the link could be fetched.'),
        ('UNHANDLED_ERROR', 'ERROR: (3.X) Unhandled situation after link fetching started.'),
        # In Discazos Player
        ('DL_LOAD_TIMEOUT', 'ERROR: (4) Download link load timeout.'),
        ('DL_GET_FAIL', 'ERROR: (4) Download link GET fail.'),
        ('DL_BAD_FILE', 'ERROR: (4) Bad file fetched (less than 50KB). Possible redirect.'),
        ('LOADING_INIT', 'INFO: (4) Loading initialized but not finished loading.'),
        ('LOADING_INTERRUPTED', 'WARN: (5) Loading suddenly interrupted.'),
        ('LOADING_SIZE_MISMATCH', 'WARN: (5) Loading finished, but loaded bytes does not match audio file size.'),
        ('LOADING_FINISHED_OK', 'OK: (5) Loading finished successfully.'),
    )
    
    date_and_time = models.DateTimeField(u'fecha y hora', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=u'usuario')
    album_release = models.ForeignKey(AlbumRelease, verbose_name='album (edición)', 
                                      related_name='playback_log_entries')
    album_release_dl_source = models.ForeignKey(AlbumReleaseDownloadSource, 
                                                verbose_name=u'fuente de descarga',
                                                related_name='playback_log_entries')
    loading_status = models.CharField(u'estado de la carga',
                                      choices=LOADING_STATUSES, max_length=50,
                                      default='DOWNLOAD_SOURCE_OPENED')
    extra_debug_info = models.CharField(u'información extra para debug', 
                                        max_length=255, blank=True)
    latest_update = models.DateTimeField(u'última act.', auto_now=True)

    def __unicode__(self):
        return u"%s - %s" % (self.date_and_time, self.user)
