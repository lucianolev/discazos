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
    