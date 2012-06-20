# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Artist'
        db.create_table('albums_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('official_site', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('youtube_profile', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('wikipedia', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('albums', ['Artist'])

        # Adding model 'PersonArtist'
        db.create_table('albums_personartist', (
            ('artist_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.Artist'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('albums', ['PersonArtist'])

        # Adding model 'GroupArtist'
        db.create_table('albums_groupartist', (
            ('artist_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.Artist'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('albums', ['GroupArtist'])

        # Adding M2M table for field members on 'GroupArtist'
        db.create_table('albums_groupartist_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groupartist', models.ForeignKey(orm['albums.groupartist'], null=False)),
            ('personartist', models.ForeignKey(orm['albums.personartist'], null=False))
        ))
        db.create_unique('albums_groupartist_members', ['groupartist_id', 'personartist_id'])

        # Adding model 'ArtistAlias'
        db.create_table('albums_artistalias', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='aliases', to=orm['albums.Artist'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('albums', ['ArtistAlias'])

        # Adding model 'Song'
        db.create_table('albums_song', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('albums', ['Song'])

        # Adding M2M table for field composers on 'Song'
        db.create_table('albums_song_composers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('song', models.ForeignKey(orm['albums.song'], null=False)),
            ('personartist', models.ForeignKey(orm['albums.personartist'], null=False))
        ))
        db.create_unique('albums_song_composers', ['song_id', 'personartist_id'])

        # Adding model 'Album'
        db.create_table('albums_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('wikipedia', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('recording_type', self.gf('django.db.models.fields.CharField')(default='ST', max_length=2)),
        ))
        db.send_create_signal('albums', ['Album'])

        # Adding model 'ArtistAlbum'
        db.create_table('albums_artistalbum', (
            ('album_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.Album'], unique=True, primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='albums', to=orm['albums.Artist'])),
        ))
        db.send_create_signal('albums', ['ArtistAlbum'])

        # Adding model 'CompilationAlbum'
        db.create_table('albums_compilationalbum', (
            ('album_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.Album'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('albums', ['CompilationAlbum'])

        # Adding M2M table for field artists on 'CompilationAlbum'
        db.create_table('albums_compilationalbum_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('compilationalbum', models.ForeignKey(orm['albums.compilationalbum'], null=False)),
            ('artist', models.ForeignKey(orm['albums.artist'], null=False))
        ))
        db.create_unique('albums_compilationalbum_artists', ['compilationalbum_id', 'artist_id'])

        # Adding model 'AlbumRating'
        db.create_table('albums_albumrating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['albums.Album'])),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['auth.User'])),
        ))
        db.send_create_signal('albums', ['AlbumRating'])

        # Adding model 'AlbumRelease'
        db.create_table('albums_albumrelease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('release_date', self.gf('django.db.models.fields.DateField')()),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(related_name='uploadings', to=orm['auth.User'])),
            ('stream_quality', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('albums', ['AlbumRelease'])

        # Adding model 'ArtistAlbumRelease'
        db.create_table('albums_artistalbumrelease', (
            ('albumrelease_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.AlbumRelease'], unique=True)),
            ('artistalbum_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.ArtistAlbum'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('albums', ['ArtistAlbumRelease'])

        # Adding model 'CompilationAlbumRelease'
        db.create_table('albums_compilationalbumrelease', (
            ('albumrelease_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.AlbumRelease'], unique=True)),
            ('compilationalbum_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.CompilationAlbum'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('albums', ['CompilationAlbumRelease'])

        # Adding model 'AlbumReleaseDownloadSource'
        db.create_table('albums_albumreleasedownloadsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album_release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='download_sources', to=orm['albums.AlbumRelease'])),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('download_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('albums', ['AlbumReleaseDownloadSource'])

        # Adding model 'Disc'
        db.create_table('albums_disc', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album_release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='discs', to=orm['albums.AlbumRelease'])),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('albums', ['Disc'])

        # Adding model 'DiscTrack'
        db.create_table('albums_disctrack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('disc', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tracks', to=orm['albums.Disc'])),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recordings', to=orm['albums.Artist'])),
            ('song', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recordings', to=orm['albums.Song'])),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('albums', ['DiscTrack'])

        # Adding M2M table for field invited_artists on 'DiscTrack'
        db.create_table('albums_disctrack_invited_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('disctrack', models.ForeignKey(orm['albums.disctrack'], null=False)),
            ('artist', models.ForeignKey(orm['albums.artist'], null=False))
        ))
        db.create_unique('albums_disctrack_invited_artists', ['disctrack_id', 'artist_id'])


    def backwards(self, orm):
        
        # Deleting model 'Artist'
        db.delete_table('albums_artist')

        # Deleting model 'PersonArtist'
        db.delete_table('albums_personartist')

        # Deleting model 'GroupArtist'
        db.delete_table('albums_groupartist')

        # Removing M2M table for field members on 'GroupArtist'
        db.delete_table('albums_groupartist_members')

        # Deleting model 'ArtistAlias'
        db.delete_table('albums_artistalias')

        # Deleting model 'Song'
        db.delete_table('albums_song')

        # Removing M2M table for field composers on 'Song'
        db.delete_table('albums_song_composers')

        # Deleting model 'Album'
        db.delete_table('albums_album')

        # Deleting model 'ArtistAlbum'
        db.delete_table('albums_artistalbum')

        # Deleting model 'CompilationAlbum'
        db.delete_table('albums_compilationalbum')

        # Removing M2M table for field artists on 'CompilationAlbum'
        db.delete_table('albums_compilationalbum_artists')

        # Deleting model 'AlbumRating'
        db.delete_table('albums_albumrating')

        # Deleting model 'AlbumRelease'
        db.delete_table('albums_albumrelease')

        # Deleting model 'ArtistAlbumRelease'
        db.delete_table('albums_artistalbumrelease')

        # Deleting model 'CompilationAlbumRelease'
        db.delete_table('albums_compilationalbumrelease')

        # Deleting model 'AlbumReleaseDownloadSource'
        db.delete_table('albums_albumreleasedownloadsource')

        # Deleting model 'Disc'
        db.delete_table('albums_disc')

        # Deleting model 'DiscTrack'
        db.delete_table('albums_disctrack')

        # Removing M2M table for field invited_artists on 'DiscTrack'
        db.delete_table('albums_disctrack_invited_artists')


    models = {
        'albums.album': {
            'Meta': {'object_name': 'Album'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recording_type': ('django.db.models.fields.CharField', [], {'default': "'ST'", 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'wikipedia': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'albums.albumrating': {
            'Meta': {'object_name': 'AlbumRating'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['albums.Album']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'albums.albumrelease': {
            'Meta': {'object_name': 'AlbumRelease'},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {}),
            'stream_quality': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uploadings'", 'to': "orm['auth.User']"})
        },
        'albums.albumreleasedownloadsource': {
            'Meta': {'object_name': 'AlbumReleaseDownloadSource'},
            'album_release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'download_sources'", 'to': "orm['albums.AlbumRelease']"}),
            'download_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'albums.artist': {
            'Meta': {'object_name': 'Artist'},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'official_site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'wikipedia': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'youtube_profile': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'albums.artistalbum': {
            'Meta': {'object_name': 'ArtistAlbum', '_ormbases': ['albums.Album']},
            'album_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.Album']", 'unique': 'True', 'primary_key': 'True'}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'albums'", 'to': "orm['albums.Artist']"})
        },
        'albums.artistalbumrelease': {
            'Meta': {'object_name': 'ArtistAlbumRelease', '_ormbases': ['albums.ArtistAlbum', 'albums.AlbumRelease']},
            'albumrelease_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.AlbumRelease']", 'unique': 'True'}),
            'artistalbum_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.ArtistAlbum']", 'unique': 'True', 'primary_key': 'True'})
        },
        'albums.artistalias': {
            'Meta': {'object_name': 'ArtistAlias'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aliases'", 'to': "orm['albums.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'albums.compilationalbum': {
            'Meta': {'object_name': 'CompilationAlbum', '_ormbases': ['albums.Album']},
            'album_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.Album']", 'unique': 'True', 'primary_key': 'True'}),
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'compilation_albums'", 'symmetrical': 'False', 'to': "orm['albums.Artist']"})
        },
        'albums.compilationalbumrelease': {
            'Meta': {'object_name': 'CompilationAlbumRelease', '_ormbases': ['albums.CompilationAlbum', 'albums.AlbumRelease']},
            'albumrelease_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.AlbumRelease']", 'unique': 'True'}),
            'compilationalbum_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.CompilationAlbum']", 'unique': 'True', 'primary_key': 'True'})
        },
        'albums.disc': {
            'Meta': {'object_name': 'Disc'},
            'album_release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discs'", 'to': "orm['albums.AlbumRelease']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'albums.disctrack': {
            'Meta': {'object_name': 'DiscTrack'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recordings'", 'to': "orm['albums.Artist']"}),
            'disc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracks'", 'to': "orm['albums.Disc']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'invited_recordings'", 'blank': 'True', 'to': "orm['albums.Artist']"}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recordings'", 'to': "orm['albums.Song']"})
        },
        'albums.groupartist': {
            'Meta': {'object_name': 'GroupArtist', '_ormbases': ['albums.Artist']},
            'artist_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.Artist']", 'unique': 'True', 'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': "orm['albums.PersonArtist']"})
        },
        'albums.personartist': {
            'Meta': {'object_name': 'PersonArtist', '_ormbases': ['albums.Artist']},
            'artist_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.Artist']", 'unique': 'True', 'primary_key': 'True'})
        },
        'albums.song': {
            'Meta': {'object_name': 'Song'},
            'composers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'composed_songs'", 'blank': 'True', 'to': "orm['albums.PersonArtist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['albums']
