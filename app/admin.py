from django.contrib import admin

# Register your models here.

from .models import Receita,Categoria,Avaliacao,Ingrediente,ReceitaIngrediente,Frigorifico,Favoritos,ReceitasListaCompras,ReceitasPlanificacao,CategoriaIngrediente

admin.site.register(Receita)
admin.site.register(Categoria)
admin.site.register(CategoriaIngrediente)  
admin.site.register(Avaliacao)                   
admin.site.register(Ingrediente)  
admin.site.register(ReceitaIngrediente)  
admin.site.register(Frigorifico)  
admin.site.register(Favoritos)  
admin.site.register(ReceitasListaCompras)  
admin.site.register(ReceitasPlanificacao)  