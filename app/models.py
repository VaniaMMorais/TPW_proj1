from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os

from django.conf import settings
from django.conf.urls.static import static

# Create your models here.

# a classe que criar vai representar uma tabela da base de dados

class Categoria(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class CategoriaIngrediente(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class CategoriaRefeicao(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Ingrediente(models.Model):
    nome = models.CharField(max_length=255)
    categoria = models.ForeignKey(CategoriaIngrediente, on_delete=models.SET_NULL, null=True)
    icon = models.CharField(max_length=255,null=True, blank=True)
    calorias = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Receita(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # ambos os valores podem etar vazios
    tempoPreparacao = models.IntegerField(null=True, blank=True)
    tempoCozinhar = models.IntegerField(null=True, blank=True)
    quantidadePessoas = models.IntegerField(null=True, blank=True)
    nivel = models.IntegerField(null=True, blank=True)
    imagem = models.ImageField(upload_to='static/img',null=True, blank=True)  # 'upload_to' define o diretório de armazenamento
    ingredients = models.ManyToManyField(Ingrediente, through='ReceitaIngrediente')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def save(self, *args, **kwargs):
        if not self.imagem:  # Adicionando verificação para evitar chamadas desnecessárias
            super().save(*args, **kwargs)
            return

        filename = f'{slugify(self.name)}.jpg'  

        filepath = os.path.join(settings.MEDIA_ROOT, 'static/img', filename)
        with open(filepath, 'wb') as file:
            for chunk in self.imagem.chunks():
                file.write(chunk)

        self.imagem.name = os.path.join('static/img', filename)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.name
    
# Modelo para Receitas_Receita_Ingrediente (tabela de associação)
class ReceitaIngrediente(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.ingrediente.nome} em {self.receita.name}"
    
class Avaliacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE) # quando o pai é eliminado, os filhos tb são
    descricao = models.TextField()
    clasificacao = models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    data = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao[0:50]
    

class Frigorifico(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    data = models.DateField()
    checklist = models.BooleanField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ingredient.nome} no frigorífico de {self.user.username}"


class Favoritos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receita.name} nos favoritos de {self.user.username}"


class ListaCompras(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    data = models.DateField()
    checklist = models.BooleanField()

    def __str__(self):
        return f"{self.ingredient.nome} na lista de compras de {self.user.username}"

# Create your models here.
class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)    