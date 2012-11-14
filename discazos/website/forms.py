# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from models import *

class InviteRegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label="Nombre de usuario",
                                error_messages={'invalid': 
                                                "El nombre de usuario puede contener únicamente letras, números y los caracteres @ . + - _"})
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Contraseña (de nuevo)")
    
    def clean_username(self):
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("Ya existe el nombre de usuario elegido.")
        else:
            return self.cleaned_data['username']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Las dos contraseñas ingresadas no coinciden.")
        return self.cleaned_data
    
class ProblemReportForm(forms.ModelForm):
    
    class Meta:
        model = ProblemReport
        fields = ('problem', 'details', )