from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

from discazos import settings

urlpatterns = patterns('',
    # Example:
    # (r'^discazos/', include('discazos.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', login_required(direct_to_template), {'template': 'home.html'}, name="home"),
    url(r'^install-extension$', login_required(direct_to_template), 
        {'template': 'extension_install.html'}, name="extension_install"),
    url(r'^update-extension$', login_required(direct_to_template), 
        {'template': 'extension_update.html'}, name="extension_update"),

    url(r'^albums/$', 'discazos.albums.views.albums_list', name="albums_list"),
    url(r'^album/(?P<album_id>\d+)$', 'discazos.albums.views.album_view', name="album_view"),
    url(r'^album/(?P<album_id>\d+)/sources$', 
        'discazos.albums.views.download_sources_list', name="dl_sources_list"),
    
    url(r'^artists/$', 'discazos.albums.views.artists_list', name="artists_list"),
    
    url(r'^share/new-album$', 'discazos.albums.views.share_new_album', name="share_new_album"),
    url(r'^share/add-discs$', 'discazos.albums.views.share_add_discs_xml', name="share_add_discs_xml"),
    url(r'^share/review-discs$', 'discazos.albums.views.share_review_discs', name="share_review_discs"),
    url(r'^share/review-discs/(\d)$', 'discazos.albums.views.share_review_disc_info', name="share_review_disc_info"),
    url(r'^share/upload-audio$', 'discazos.albums.views.share_upload_audio', name="share_upload_audio"),
    url(r'^share/add-release-info$', 'discazos.albums.views.share_add_release_info', name="share_add_release_info"),
    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    url(r'^accounts/register/invited/$', 'discazos.website.views.register_invited', name="register_invited"),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

#Static serving (enabled for devel only)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',  
            { 'document_root':settings.MEDIA_ROOT }),
    )
