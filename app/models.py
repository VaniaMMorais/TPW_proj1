from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# a classe que criar vai representar uma tabela da base de dados

class Categoria(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Receita(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # ambos os valores podem etar vazios
    # ingredients = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class Avaliacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE) # quando o pai é eliminado, os filhos tb são
    descricao = models.TextField()
    clasificacao = models.IntegerField()
    data = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao[0:50]