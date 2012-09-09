from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from models import *
from forms import *
from xml_import import *

@login_required
def albums_list(request):
    albums = ArtistAlbum.objects.all()
    return render_to_response('albums_list.html', 
                              { 'albums' : albums },
                              context_instance=RequestContext(request))

@login_required
def album_view(request, album_id):
    album = ArtistAlbum.objects.get(pk=album_id)
    return render_to_response('album_view.html', 
                              { 'album' : album, 
                                'BROWSER_EXTENSION_VERSION': 
                                 settings.BROWSER_EXTENSION_VERSION },
                              context_instance=RequestContext(request))

@login_required
def download_sources_list(request, album_id):
    album = ArtistAlbum.objects.get(pk=album_id)
    #import pdb; pdb.set_trace()
    dl_sources = album.main_release().download_sources.all()
    return render_to_response('download_sources_list.html', 
                              { 'dl_sources' : dl_sources },
                              context_instance=RequestContext(request))

#Assistant: Step 1
@login_required
def share_new_album(request):
    if request.method == 'POST':
        artistAlbumForm = ArtistAlbumShareForm(request.POST)
        if artistAlbumForm.is_valid():
            request.session['album_data'] = artistAlbumForm.cleaned_data
            return redirect('share_add_discs_xml')
    else:
        artistAlbumForm = ArtistAlbumShareForm()
    return render_to_response('share/new_album.html',
                              {'artistAlbumForm': artistAlbumForm }, 
                              context_instance=RequestContext(request))

#Assistant: Step 2
@login_required
def share_add_discs_xml(request):
    if request.method == 'POST':
        xmlUploadForm = DiscsInfoUploadForm(request.POST, request.FILES)
        if xmlUploadForm.is_valid():
            try:
                xmlParser = DiscazosCreatorXML.load_from_file(xmlUploadForm.cleaned_data['xml_file'])
                creatorAlbumTitle = xmlParser.get_album_title()
                choosenAlbumTitle = request.session['album_data']['title']
                if creatorAlbumTitle == choosenAlbumTitle:
                    request.session['audiofile_size'] = xmlParser.get_audiofile_size()
                    request.session['discs_data'] = xmlParser.get_discs_info()
                    return redirect('share_review_discs')
                else:
                    messages.error(request, "The XML file provided is for a "
                                            "different album (\""+creatorAlbumTitle+"\"). "
                                            "Please upload the XML file for the "
                                            "album \""+choosenAlbumTitle+"\".")
            except InvalidXMLFile:
                messages.error(request, "The file provided is not a valid XML "
                                        "file! Please make sure to upload the "
                                        "XML file provided by the latest "
                                        "of Discazos Creator.")
            except UnsupportedCreatorVersion:
                messages.error(request, "The XML file provided was generated with "
                                        "an old version of Discazos Creator. "
                                        "Please download the latest version "
                                        "of Discazos Creator, create the album "
                                        "again and re-upload the XML file. "
                                        "Sorry for the inconvenience.")
    else:
        xmlUploadForm = DiscsInfoUploadForm()
    return render_to_response('share/add_discs_xml.html',
                              { 'xmlUploadForm': xmlUploadForm },
                              context_instance=RequestContext(request))

#Assistant: Step 3
@login_required
def share_review_discs(request):
    nums_discs = range(len(request.session['discs_data']))
    return render_to_response('share/review_discs.html',
                              { 'nums_discs': nums_discs },
                              context_instance=RequestContext(request))

@login_required
def share_review_disc_info(request, disc_num):
    DiscTracksFormset = formset_factory(DiscTrackShareForm, extra=0)
    if request.method == 'POST':
        discForm = DiscShareForm(request.POST, prefix='disc')
        tracksFormset = DiscTracksFormset(request.POST, prefix='tracks')
        if discForm.is_valid() and tracksFormset.is_valid():
            discData = discForm.cleaned_data
            tracksData = [form.cleaned_data for form in tracksFormset.forms]
            request.session['discs_data'][int(disc_num)] = (discData, tracksData)
            request.session.modified = True
            return redirect('share_review_discs')
    else:
        discData, tracksData = request.session['discs_data'][int(disc_num)]
        discForm = DiscShareForm(initial=discData, prefix='disc')
        tracksFormset = DiscTracksFormset(initial=tracksData, prefix='tracks')
    return render_to_response('share/review_disc_info.html',
                              {'discForm': discForm, 
                               'tracksFormset': tracksFormset, },
                              context_instance=RequestContext(request))

#Assistant: Step 4
@login_required
def share_upload_audio(request):
    if request.method == 'POST':
        downloadSourceForm = MediafireSourceShareForm(request.POST)
        if downloadSourceForm.is_valid():
            request.session['download_source_data'] = downloadSourceForm.cleaned_data
            return redirect('share_add_release_info')
    else:
        downloadSourceForm = MediafireSourceShareForm()
    return render_to_response('share/upload_audio.html',
                              { 'downloadSourceForm': downloadSourceForm, },
                              context_instance=RequestContext(request))

#Assistant: Step 5 & Finish
@login_required
def share_add_release_info(request):
    if request.method == 'POST':
        albumReleaseForm = AlbumReleaseShareForm(request.POST, request.FILES)
        if albumReleaseForm.is_valid():
            album = ArtistAlbum.create(request.session['album_data'])
            audiofile_size = request.session['audiofile_size']
            albumRelease = AlbumRelease.create_main_release(albumReleaseForm.cleaned_data, 
                                                            request.user, album, 
                                                            audiofile_size)
            for discData, tracksData in request.session['discs_data']:
                disc = Disc.create_with_release(discData, albumRelease)
                for trackData in tracksData:
                    DiscTrack.create_from_assistant(trackData, disc)
            AlbumReleaseDownloadSource.create_mediafire(request.session['download_source_data'], 
                                                        albumRelease)
            return render_to_response('share/finish.html',
                                      {'albumPk': album.pk }, 
                                      context_instance=RequestContext(request))
    else:
        albumReleaseForm = AlbumReleaseShareForm()
    return render_to_response('share/add_release_info.html',
                              { 'albumReleaseForm': albumReleaseForm, },
                              context_instance=RequestContext(request))
