from django.forms import ModelForm
from django import forms

from .models import Avaliacao, Categoria, Frigorifico, Ingrediente, Receita

class ReceitaForm(ModelForm):
    class Meta:
        model = Receita
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ComentarioForm(forms.ModelForm):
    clasificacao = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], widget=forms.Select)
    class Meta:
        model = Avaliacao
        fields = ['descricao', 'clasificacao'] 


class FridgeForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingrediente.objects.all(),
        label='Escolha um ingrediente',
        empty_label=None  # Impede um valor vazio no dropdown
    )

    class Meta:
        model = Frigorifico
        fields = ['ingredient']

class FiltroReceitasForm(forms.Form):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Todas as Categorias",
        required=False
    )
    nome = forms.CharField(max_length=100, required=False)

class CategoryForm(forms.ModelForm):
    name = forms.CharField()
    class Meta:
        model = Categoria
        fields = ['name']

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nome', 'categoria', 'icon', 'calorias']


