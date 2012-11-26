# -*- coding: utf-8 -*-

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.core.mail import send_mail
from django.core import urlresolvers
from django.contrib.sites.models import RequestSite

from registration.views import register as registration_register

from discazos.albums.models import *

from models import *
from forms import *

def logged_in_message(sender, user, request, **kwargs):
    messages.error(request, 
       "<strong>Importante: </strong>El sitio está actualmente en " 
       "<strong>fase de prueba</strong> y puede que no todo funcione como debería. "
       "Si encontrás algún problema, ayudanos a mejorar el sitio haciendo click "
       "en el botón de <strong>Reportar problema</strong> al pie de la página. "
       "Gracias por la paciencia!")

user_logged_in.connect(logged_in_message)

def home(request):
    latest_albums = ArtistAlbum.objects.filter(releases__published=True).order_by('-releases__uploaded_on')[:4]
    return render(request, 'home.html', 
                  {'latest_albums': latest_albums})

@login_required
def problem_report(request):
    if request.method == 'POST':
        report_form = ProblemReportForm(request.POST)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.sent_by = request.user
            report.sent_from_url = request.META['HTTP_REFERER'][:255]
            report.user_agent = request.META['HTTP_USER_AGENT'][:1024]
            report.save()
            # Send mail with report
            subject = "[Discazos] Reporte de problema enviado por " + report.sent_by.username
            subject += " (#%s)" % report.pk
            site = RequestSite(request)
            admin_url = site.domain + urlresolvers.reverse('admin:website_problemreport_change', 
                                                    args=(report.id,))
            message = render_to_string('problem_report/email.txt', 
                                       { 'report': report, 
                                         'admin_report_url': admin_url })
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.PROBLEM_REPORT_EMAIL])
                report.notified = True
                report.save()
            except:
                 pass
            return render(request, 'problem_report/thanks.html')
    else:
        report_form = ProblemReportForm()
    return render(request, 'problem_report/form.html', {
        'report_form': report_form,
    })

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
