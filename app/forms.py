from django.forms import ModelForm
from django import forms

from .models import Receita

class ReceitaForm(ModelForm):
    class Meta:
        model = Receita
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)