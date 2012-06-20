# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'CompilationAlbumRelease'
        db.delete_table('albums_compilationalbumrelease')

        # Deleting model 'ArtistAlbumRelease'
        db.delete_table('albums_artistalbumrelease')

        # Adding field 'AlbumRelease.album'
        db.add_column('albums_albumrelease', 'album', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='releases', to=orm['albums.ArtistAlbum']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'CompilationAlbumRelease'
        db.create_table('albums_compilationalbumrelease', (
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='releases', to=orm['albums.CompilationAlbum'])),
            ('albumrelease_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.AlbumRelease'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('albums', ['CompilationAlbumRelease'])

        # Adding model 'ArtistAlbumRelease'
        db.create_table('albums_artistalbumrelease', (
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='releases', to=orm['albums.ArtistAlbum'])),
            ('albumrelease_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['albums.AlbumRelease'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('albums', ['ArtistAlbumRelease'])

        # Deleting field 'AlbumRelease.album'
        db.delete_column('albums_albumrelease', 'album_id')


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
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['albums.ArtistAlbum']"}),
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
