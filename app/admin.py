from django.contrib import admin

# Register your models here.

from .models import Receita,Categoria,Avaliacao,Ingrediente,ReceitaIngrediente,Frigorifico,Favoritos,ListaCompras,CategoriaIngrediente,CategoriaRefeicao,Events

admin.site.register(Receita)
admin.site.register(Categoria)
admin.site.register(CategoriaIngrediente)  
admin.site.register(CategoriaRefeicao)  
admin.site.register(Avaliacao)                   
admin.site.register(Ingrediente)  
admin.site.register(ReceitaIngrediente)  
admin.site.register(Frigorifico)  
admin.site.register(Favoritos)  
admin.site.register(ListaCompras)  
admin.site.register(Events) 
