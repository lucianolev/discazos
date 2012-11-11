from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User

from registration import signals
from registration.backends.simple import SimpleBackend

from models import Invitation

class RegistrationByInvitation(SimpleBackend):
    def register(self, request, **kwargs):
        # Notice that the invitation code has been validated before  
        # by in registration view function
        invitation_code = request.GET.get('code', None)
        invitation = Invitation.objects.get(code=invitation_code)
        
        username, email, password = kwargs['username'], invitation.email, kwargs['password1']
        new_user = User.objects.create_user(username, email, password)
        
        invitation.mark_accepted(new_user)
        
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user