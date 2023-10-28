from django.contrib import admin

# Register your models here.

from .models import Receita,Categoria,Avaliacao

admin.site.register(Receita)
admin.site.register(Categoria)
admin.site.register(Avaliacao)

