# -*- encoding: utf-8 -*-

from django import forms

from models import *

'''
class ArtistTypeChooser(forms.Form):
    ARTIST_TYPES = (
        ('P', 'Person'),
        ('G', 'Group'),
    )
    artist_type = forms.ChoiceField(choices=ARTIST_TYPES, initial='P',
                                    widget=forms.RadioSelect)

class PersonArtistForm(forms.ModelForm):
    class Meta:
        model = PersonArtist

class GroupArtistExtraFields(forms.ModelForm):
    class Meta:
        model = GroupArtist
        fields = ('members', )
'''

class ArtistAlbumShareForm(forms.ModelForm):
    
    class Meta:
        model = ArtistAlbum

class AlbumReleaseShareForm(forms.ModelForm):
    
    class Meta:
        model = AlbumRelease
        exclude = ('album', 'main_release', 'uploader', 'stream_quality', 
                   'audiofile_size', )

class DiscsInfoUploadForm(forms.Form):
    xml_file = forms.FileField(label=u'Archivo XML de Discazos Creator')

class DiscShareForm(forms.ModelForm):
    number = forms.IntegerField(widget=forms.HiddenInput)
    
    class Meta:
        model = Disc
        fields = ('number', 'title', )

class DiscTrackShareForm(forms.Form):
    number = forms.IntegerField(widget=forms.HiddenInput)
    artist = forms.CharField(max_length=255)
    song = forms.CharField(max_length=255)
    length = forms.IntegerField(widget=forms.HiddenInput)
    
    def clean_artist(self):
        if not Artist.objects.filter(name=self.cleaned_data['artist']).exists():
            raise forms.ValidationError("El artista no existe")
        else:
            return self.cleaned_data['artist']

class DownloadSourceShareForm(forms.ModelForm):
    
    class Meta:
        model = AlbumReleaseDownloadSource
        exclude = ('album_release', 'enabled', )
