# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from registration.views import register as registration_register

from discazos.albums.models import *
    
from models import *
from forms import *

@login_required
def home(request):
    latest_albums = ArtistAlbum.objects.filter(releases__published=True).order_by('-releases__uploaded_on')[:4]
    return render(request, 'home.html', 
                  {'latest_albums': latest_albums})

def register_invited(request):
    invitation_code = request.GET.get('code', None)
    if invitation_code and Invitation.objects.is_valid_code(invitation_code):
        backend = 'website.registration_backends.RegistrationByInvitation'
        success_url = 'home'
        form_class = InviteRegistrationForm
        disallowed_url = 'registration_disallowed' #Default
        post_registration_redirect = None #Default
        template_name = 'registration/register_invited.html'
        return registration_register(request, backend, success_url,
                                     form_class, disallowed_url,
                                     template_name)
    else:
        return render(request, 'registration/invalid_invitation_code.html')
