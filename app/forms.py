from django.forms import ModelForm

from .models import Receita

class ReceitaForm(ModelForm):
    class Meta:
        model = Receita
        fields = '__all__'