# Create your views here.
from django.shortcuts import render

from registration.views import register as registration_register

from website.models import *
from website.forms import *

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
