# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from discazos.utils.random_code import *

class InvitationManager(models.Manager):
    def is_valid_code(self, invitation_code):
        return self.filter(code=invitation_code, accepted_by=None).exists()

class Invitation(models.Model):
    class Meta:
        verbose_name = u'invitación'
        verbose_name_plural = u'invitaciones'
    
    code = models.CharField(u'código de invitación', max_length=40, primary_key=True, editable=False)
    invited_by = models.ForeignKey(User, verbose_name=u'invitado por', 
                              related_name=u'invites', editable=False)
    email = models.EmailField(u'correo electrónico')
    send_by_email = models.BooleanField(u'envío por email', default=True)
    created = models.DateTimeField(u'creada el', auto_now_add=True)
    accepted_by = models.ForeignKey(User, verbose_name=u'aceptada por', 
                                 blank=True, null=True, editable=False)
    accepted_on = models.DateTimeField(u'aceptada el', blank=True, null=True, 
                                    editable=False)
    
    objects = InvitationManager()

    @property
    def accepted(self):
        return self.accepted_by is not None

    @property
    def invitation_url(self):
        url = reverse("register_invited") + "?code=" + self.code
        return url

    def mark_accepted(self, user):
        self.accepted_by = user
        self.accepted_on = datetime.datetime.now()
        self.save()

    def __unicode__(self):
        return u"%s" % self.email
    
    def validate_unique(self, *args, **kwargs):
        super(Invitation, self).validate_unique(*args, **kwargs)
        if User.objects.filter(email=self.email).exists():
            raise ValidationError({'email': ('Ya existe un usuario registrado con ' 
                                             'esta dirección de correo electrónico.', )})

    def save(self, *args, **kwargs):
        if self.pk:
            return super(Invitation, self).save(*args, **kwargs)
        else:
            self.code = random_code()
            try:
                return super(Invitation, self).save(*args, **kwargs)
            except IntegrityError:
                raise Exception('Could not generate unique invitation code')

    def send_email(self, site):
        subject = "Recibiste una invitación para unirte a Discazos.net"
        message = render_to_string('registration/invitation_email.txt',
                                   { 'invitation_url': self.invitation_url,
                                     'site': site })
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])

class ProblemReport(models.Model):
    REPORT_STATUSES = (
        ('NEW', u'Nuevo'),
        ('PENDING', u'Pendiente'),
        ('ARCHIVED', u'Archivado'),
        ('NOT_UNDERSTANDABLE', u'No se entiende'),
    )
    PROBLEMS = (
        ('EXTENSION_INSTALL_PROBLEM', u'No puedo instalar la extensión'),
        ('EXTENSION_INSTALL_PROBLEM2', u'Instalé la extensión pero vuelve a pedir instalarla'),
        ('ALBUM_NOT_LOADING_ANY_SOURCE', u'El álbum no carga con ninguna de las fuentes'),
        ('ALBUM_LOADING_VERY_SLOW', u'El álbum carga MUY lentamente'),
        ('ALBUM_PLAYBACK_PROBLEM', u'El álbum no se reproduce correctamente'),
        ('ALBUM_NOT_FULLY_LOADED', u'El álbum no se cargó por completo'),
        ('ALBUM_TRACKS SYNC_PROBLEM', u'Las pistas del album están desfasadas'),
        ('ALBUM_INFO_ERRORS', u'La información del álbum contiene errores'),
        ('OTHER', u'Otro problema'),
    )
    
    created_on = models.DateTimeField(u'fecha y hora', auto_now_add=True)
    sent_by = models.ForeignKey(User, verbose_name=u'enviado por')
    problem = models.CharField(u'problema', choices=PROBLEMS, max_length=100)
    details = models.TextField(u'detalle')
    sent_from_url = models.URLField(u'enviado desde')
    user_agent = models.TextField(u'User Agent', max_length=1024)
    notified = models.BooleanField(u'notificado', default=False)
    status = models.CharField(u'estado', choices=REPORT_STATUSES, 
                              default='NEW', max_length=50)
    
    class Meta:
        verbose_name = u'reporte de problema'
        verbose_name_plural = u'reportes de problemas'
