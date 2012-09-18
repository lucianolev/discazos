from django.db import models
from django.contrib.auth.models import User

from django_countries import CountryField

from albums.managers import DiscTrackManager

'''
An artist. 
It's not used directly but through group/person artist
'''
class Artist(models.Model):
    class Meta:
        ordering = ['name', ]

    name = models.CharField(max_length=255)
    country = CountryField(blank=True, null=True)
    #official_site = models.URLField(blank=True)
    #youtube_profile = models.URLField(blank=True)
    wikipedia = models.URLField(blank=True)
    
    def __unicode__(self):
        return self.name

#The person and group artist distinction make sense for
#a richer music library information 
class PersonArtist(Artist):
    class Meta:
        verbose_name = 'Artist (Person)'
        verbose_name_plural = 'Artists (People)'

class GroupArtist(Artist):
    class Meta:
        verbose_name = 'Artist (Group)'
        verbose_name_plural = 'Artists (Groups)'
    
    members = models.ManyToManyField(PersonArtist, related_name='groups', blank=True)
    past_members = models.ManyToManyField(PersonArtist, related_name='past_groups', blank=True)

#Many artist have multiple known names so this make sense
#for smart searches
class ArtistAlias(models.Model):
    class Meta:
        verbose_name = 'Alias'
        verbose_name_plural = 'Aliases'
    
    artist = models.ForeignKey(Artist, related_name='aliases')
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

'''
A song.
This represents a song in the sense of a composition created by someone
'''
class Song(models.Model):
    class Meta:
        verbose_name = 'Song'
        verbose_name_plural = 'Songs'
        ordering = ['name', ]
    
    name = models.CharField(max_length=255)
    #composers = models.ManyToManyField(PersonArtist, related_name='composed_songs', blank=True)
    #performers = models.ManyToManyField(PersonArtist, related_name='performed_songs', blank=True)
    
    def __unicode__(self):
        return self.name

'''
An album.
This represent an album as composition performed by one or more artist
An album can have many releases along history which may vary
depending on the country.
It's not used directly but through artist and compilation album.
'''
class Album(models.Model):
    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'
        ordering = ['title', ]

    RECORDING_TYPES = (
        ('ST', 'Studio'),
        ('LV', 'Live')
    )
    
    title = models.CharField(max_length=255)
    wikipedia = models.URLField(blank=True)
    recording_type = models.CharField(choices=RECORDING_TYPES, max_length=2, default='ST')
    #status? Official, bootleg
    
    @classmethod
    def create(cls, session_data):
        newAlbum = cls(**session_data)
        newAlbum.save()
        return newAlbum
    
    def main_release(self):
        return self.releases.filter(main_release=True)[0]
    
    def __unicode__(self):
        return self.title

#A typical album performed by a single artist
class ArtistAlbum(Album):
    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'
    
    artist = models.ForeignKey(Artist, related_name='albums')

#A compilation album which includes tracks of various artists
class CompilationAlbum(Album):
    class Meta:
        verbose_name = 'Compilation Album'
        verbose_name_plural = 'Compilation Albums'

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
        verbose_name = 'Album Release'
        verbose_name_plural = 'Album Releases'

    QUALITY_TYPES = (
        ('SQ', 'SQ'),
        ('HQ', 'HQ'),
    )

    album = models.ForeignKey(Album, related_name='releases')
    release_date = models.DateField(blank=True)
    country = CountryField(blank=True, null=True)
    cover = models.ImageField(upload_to='uploads/covers/')
    main_release = models.BooleanField()
    
    uploaded_on = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, related_name='uploadings')
    stream_quality = models.CharField(choices=QUALITY_TYPES, 
                                      max_length=2, default='SQ', blank=True)
    audiofile_size = models.BigIntegerField() #In bytes

    @classmethod
    def create_main_release(cls, session_data, user, album, audiofile_size):
        albumReleaseData = session_data
        albumReleaseData.update({'album': album, 
                                 'main_release': True,
                                 'uploader': user,
                                 'audiofile_size': audiofile_size,
                                 })
        newAlbumRelease = cls(**albumReleaseData)
        newAlbumRelease.save()
        return newAlbumRelease

    def __unicode__(self):
        return u"%s" % self.album + " (" + self.get_country_display() + u" %s" % self.release_date + ")"
    
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
                track_item = {'number': track.number, 'song': track.song.name,
                              'length': track.length }
                track_item['length_f'] = time.strftime('%M:%S', 
                                                       time.gmtime(track.length))
                track_item['offset'] = added_offset
                added_offset += track.length
                tracks.append(track_item)
            discs_playlist.append({ 'disc': disc, 'tracks_playlist': tracks })
        return discs_playlist

#A download source for an album release
class AlbumReleaseDownloadSource(models.Model):
    class Meta:
        verbose_name = 'Download Source'
        verbose_name_plural = 'Download Sources'
    
    PROVIDERS = (
        ('MF', 'Mediafire'),
        ('BF', 'BayFiles'),
    )
    
    album_release = models.ForeignKey(AlbumRelease, related_name='download_sources')
    provider = models.CharField(choices=PROVIDERS, max_length=2)
    download_link = models.URLField()

    @classmethod
    def create_mediafire(cls, session_data, album_release):
        sourceData = session_data
        sourceData.update({'album_release': album_release, 
                           'provider': 'MF'})
        newDownloadSource = cls(**sourceData)
        newDownloadSource.save()
        return newDownloadSource

    def __unicode__(self):
        return self.provider

'''
An album release disc.
'''
class Disc(models.Model):
    class Meta:
        verbose_name = 'Disc'
        verbose_name_plural = 'Discs'
        ordering = ['number', ]
    
    album_release = models.ForeignKey(AlbumRelease, related_name='discs')
    number = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=255, blank=True)

    @classmethod
    def create_with_release(cls, session_data, album_release):
        discData = session_data
        discData.update({'album_release': album_release })
        newDisc = cls(**discData)
        newDisc.save()
        return newDisc

    def __unicode__(self):
        disc_name = "CD " + "%s" % self.number
        if (self.title):
            disc_name += " - " + "%s" % self.title
        return disc_name

class DiscTrack(models.Model):
    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'
        ordering = ['number', ]
    
    disc = models.ForeignKey(Disc, related_name='tracks')
    number = models.PositiveSmallIntegerField(default=1)
    artist = models.ForeignKey(Artist, related_name='recordings')
    song = models.ForeignKey(Song, related_name='recordings')
    length = models.PositiveIntegerField() #In seconds
    
    @classmethod
    def create_from_assistant(cls, session_data, disc):
        trackData = session_data
        artist = Artist.objects.get(name=session_data['artist'])
        song, created = Song.objects.get_or_create(name=session_data['song'])
        trackData.update({'disc': disc, 
                          'artist': artist, 
                          'song': song})
        newTrack = cls(**trackData)
        newTrack.save()
        return newTrack
    
    def __unicode__(self):
        return "%s" % self.song
