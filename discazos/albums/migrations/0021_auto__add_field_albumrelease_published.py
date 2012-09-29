# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AlbumRelease.published'
        db.add_column('albums_albumrelease', 'published', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'AlbumRelease.published'
        db.delete_column('albums_albumrelease', 'published')


    models = {
        'albums.album': {
            'Meta': {'ordering': "['title']", 'object_name': 'Album'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recording_type': ('django.db.models.fields.CharField', [], {'default': "'ST'", 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'albums.albumrelease': {
            'Meta': {'object_name': 'AlbumRelease'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['albums.Album']"}),
            'audiofile_size': ('django.db.models.fields.BigIntegerField', [], {}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_release': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'release_extra_info': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'release_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'stream_quality': ('django.db.models.fields.CharField', [], {'default': "'SQ'", 'max_length': '2', 'blank': 'True'}),
            'uploaded_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uploadings'", 'to': "orm['auth.User']"})
        },
        'albums.albumreleasedownloadsource': {
            'Meta': {'object_name': 'AlbumReleaseDownloadSource'},
            'album_release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'download_sources'", 'to': "orm['albums.AlbumRelease']"}),
            'download_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['albums.FileHostingService']"})
        },
        'albums.artist': {
            'Meta': {'ordering': "['name']", 'object_name': 'Artist'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'albums.artistalbum': {
            'Meta': {'ordering': "['title']", 'object_name': 'ArtistAlbum', '_ormbases': ['albums.Album']},
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
            'Meta': {'ordering': "['title']", 'object_name': 'CompilationAlbum', '_ormbases': ['albums.Album']},
            'album_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.Album']", 'unique': 'True', 'primary_key': 'True'})
        },
        'albums.disc': {
            'Meta': {'ordering': "['number']", 'object_name': 'Disc'},
            'album_release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discs'", 'to': "orm['albums.AlbumRelease']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'albums.disctrack': {
            'Meta': {'ordering': "['number']", 'object_name': 'DiscTrack'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recordings'", 'to': "orm['albums.Artist']"}),
            'disc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracks'", 'to': "orm['albums.Disc']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recordings'", 'to': "orm['albums.Song']"})
        },
        'albums.filehostingservice': {
            'Meta': {'ordering': "['priority']", 'object_name': 'FileHostingService'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.IntegerField', [], {})
        },
        'albums.groupartist': {
            'Meta': {'ordering': "['name']", 'object_name': 'GroupArtist', '_ormbases': ['albums.Artist']},
            'artist_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.Artist']", 'unique': 'True', 'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'groups'", 'blank': 'True', 'to': "orm['albums.PersonArtist']"}),
            'past_members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'past_groups'", 'blank': 'True', 'to': "orm['albums.PersonArtist']"})
        },
        'albums.personartist': {
            'Meta': {'ordering': "['name']", 'object_name': 'PersonArtist', '_ormbases': ['albums.Artist']},
            'artist_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['albums.Artist']", 'unique': 'True', 'primary_key': 'True'})
        },
        'albums.song': {
            'Meta': {'ordering': "['name']", 'object_name': 'Song'},
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
