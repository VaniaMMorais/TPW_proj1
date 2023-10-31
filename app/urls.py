# urls file just to handle all the routing for this app

from django.urls import path, include
from . import views

urlpatterns = [
    path('index/',  views.index, name = "index"),
    path('', views.loginp, name= 'loginp'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('fridge/', views.fridge, name ="fridge"),

    path('newrecipe/',  views.createRecipe, name = "createRecipe"),
    path('updaterecipe/<str:pk>',  views.updateReceita, name = "updateReceita"),
    path('deleterecipe/<str:pk>',  views.deleteRecipe, name = "deleteRecipe"),


]
