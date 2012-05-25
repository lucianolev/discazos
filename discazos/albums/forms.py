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
        exclude = ('album', 'main_release', 'uploader', 'stream_quality', )

class DiscsInfoUploadForm(forms.Form):
    xml_file = forms.FileField(label=u'Discs XML file')

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
            raise forms.ValidationError("Artist does not exist")
        else:
            return self.cleaned_data['artist']

class MediafireSourceShareForm(forms.ModelForm):
    
    class Meta:
        model = AlbumReleaseDownloadSource
        fields = ('download_link', )
