# urls file just to handle all the routing for this app

from django.urls import path, include
from . import views

urlpatterns = [
    path('index/<str:username>/', views.index, name="index"),
    path('', views.loginp, name= 'loginp'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('fridge/', views.fridge, name ="fridge"),
    path('filtered_recipies/<int:cat>', views.filtered_recipies, name='filtered_recipies'),
    path('recipepost/<int:id>', views.recipepost, name='recipepost'),


    path('newrecipe/',  views.createRecipe, name = "createRecipe"),
    path('updaterecipe/<str:pk>',  views.updateReceita, name = "updateReceita"),
    path('deleterecipe/<str:pk>',  views.deleteRecipe, name = "deleteRecipe"),


]
