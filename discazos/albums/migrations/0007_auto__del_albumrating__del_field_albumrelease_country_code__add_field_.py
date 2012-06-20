# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'AlbumRating'
        db.delete_table('albums_albumrating')

        # Deleting field 'AlbumRelease.country_code'
        db.delete_column('albums_albumrelease', 'country_code')

        # Adding field 'AlbumRelease.country'
        db.add_column('albums_albumrelease', 'country', self.gf('django_countries.fields.CountryField')(max_length=2, null=True, blank=True), keep_default=False)

        # Deleting field 'Artist.youtube_profile'
        db.delete_column('albums_artist', 'youtube_profile')

        # Deleting field 'Artist.official_site'
        db.delete_column('albums_artist', 'official_site')

        # Deleting field 'Artist.country_code'
        db.delete_column('albums_artist', 'country_code')

        # Adding field 'Artist.country'
        db.add_column('albums_artist', 'country', self.gf('django_countries.fields.CountryField')(max_length=2, null=True, blank=True), keep_default=False)

        # Adding M2M table for field past_members on 'GroupArtist'
        db.create_table('albums_groupartist_past_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groupartist', models.ForeignKey(orm['albums.groupartist'], null=False)),
            ('personartist', models.ForeignKey(orm['albums.personartist'], null=False))
        ))
        db.create_unique('albums_groupartist_past_members', ['groupartist_id', 'personartist_id'])

        # Removing M2M table for field composers on 'Song'
        db.delete_table('albums_song_composers')


    def backwards(self, orm):
        
        # Adding model 'AlbumRating'
        db.create_table('albums_albumrating', (
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['albums.Album'])),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('albums', ['AlbumRating'])

        # Adding field 'AlbumRelease.country_code'
        db.add_column('albums_albumrelease', 'country_code', self.gf('django.db.models.fields.CharField')(default='', max_length=2, blank=True), keep_default=False)

        # Deleting field 'AlbumRelease.country'
        db.delete_column('albums_albumrelease', 'country')

        # Adding field 'Artist.youtube_profile'
        db.add_column('albums_artist', 'youtube_profile', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'Artist.official_site'
        db.add_column('albums_artist', 'official_site', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'Artist.country_code'
        db.add_column('albums_artist', 'country_code', self.gf('django.db.models.fields.CharField')(default='', max_length=2, blank=True), keep_default=False)

        # Deleting field 'Artist.country'
        db.delete_column('albums_artist', 'country')

        # Removing M2M table for field past_members on 'GroupArtist'
        db.delete_table('albums_groupartist_past_members')

        # Adding M2M table for field composers on 'Song'
        db.create_table('albums_song_composers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('song', models.ForeignKey(orm['albums.song'], null=False)),
            ('personartist', models.ForeignKey(orm['albums.personartist'], null=False))
        ))
        db.create_unique('albums_song_composers', ['song_id', 'personartist_id'])


    models = {
        'albums.album': {
            'Meta': {'ordering': "['title']", 'object_name': 'Album'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recording_type': ('django.db.models.fields.CharField', [], {'default': "'ST'", 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'wikipedia': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'albums.albumrelease': {
            'Meta': {'object_name': 'AlbumRelease'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['albums.Album']"}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_release': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'release_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'stream_quality': ('django.db.models.fields.CharField', [], {'default': "'SQ'", 'max_length': '2', 'blank': 'True'}),
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
            'Meta': {'ordering': "['name']", 'object_name': 'Artist'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'wikipedia': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
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
