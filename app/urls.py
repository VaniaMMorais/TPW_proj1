# urls file just to handle all the routing for this app

from django.urls import path
from . import views

urlpatterns = [
    path('',  views.index, name = "index"),
    path('fridge/', views.fridge, name ="fridge"),

    path('newrecipe/',  views.createRecipe, name = "createRecipe"),
    path('updaterecipe/<str:pk>',  views.updateReceita, name = "updateReceita"),
    path('deleterecipe/<str:pk>',  views.deleteRecipe, name = "deleteRecipe"),


]
