# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.sites.models import RequestSite

from models import *

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'invited_by', 'created', 'invitation_link', 
                    'send_by_email', 'accepted_display')
    ordering = ('-created', )

    def accepted_display(self, obj):
        if obj.accepted_on:
            return obj.accepted_on.strftime('%d %b. %Y %H:%M:%S')
        else:
            return u"Pendiente"
    accepted_display.short_description = u"Aceptada"

    def invitation_link(self, obj):
        if not obj.accepted:
            return mark_safe("<a href='%s'>%s</a>" % (obj.invitation_url, u"Disponible"))
        else:
            return u"Invitación ya utilizada"
    invitation_link.allow_tags = True
    invitation_link.short_description = u"Link de invitación"

    def get_readonly_fields(self, request, obj=None):
        if obj: # Editing
            readonly_fields = ('invited_by', 'email', 'send_by_email', 
                               'created', )
            if obj.accepted:
                readonly_fields += ('accepted_by', 'accepted_on', )
            else:
                readonly_fields += ('invitation_link', )
            return readonly_fields
        return ()
    
    def save_model(self, request, obj, form, change):
        if change:
            return False
        else:
            obj.invited_by = request.user
            obj.save()
            if obj.send_by_email:
                site = RequestSite(request)
                try:
                    obj.send_email(site)
                    messages.info(request, u"Se ha enviado un email con la invitación a %s." % obj.email)
                except:
                    messages.error(request, u"Ocurrió un error al enviar el email de invitación a %s." % obj.email)

class ProblemReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'sent_from_url', 'sent_by', 
                    'created_on', 'notified', 'status', )
    readonly_fields = ('sent_by', 'problem', 'details', 'sent_from_url', 'user_agent' , 
                       'created_on', 'notified', )
    ordering = ('-created_on', )
    
    def has_add_permission(self, request):
        return False

admin.site.register(Invitation, InvitationAdmin)
admin.site.register(ProblemReport, ProblemReportAdmin)