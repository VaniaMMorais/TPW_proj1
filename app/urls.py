# urls file just to handle all the routing for this app

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('loginp', views.loginp, name= 'loginp'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('fridge/', views.fridge, name ="fridge"),
    path('favorites/', views.favorites, name ="favorites"),
    path('myrecipes/', views.myrecipes, name ="myrecipes"),
    path('filtered_recipies/', views.filtered_recipies, name='filtered_recipies'),
    path('filtered_recipies/<str:cat>/', views.filtered_recipies, name='filtered_recipies'),
    path('filtered_recipies/<str:nome>/', views.filtered_recipies, name='filtered_recipies'),
    path('filtered_recipies/<str:cat>/<str:nome>/', views.filtered_recipies, name='filtered_recipies'),
    path('adminPage/', views.adminPage, name="adminPage"),


    path('recipepost/<int:id>', views.recipepost, name='recipepost'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('add_ingredient_to_fridge/', views.add_ingredient_to_fridge, name='add_ingredient_to_fridge'),
    path('delete_category/<int:cat_id>/', views.delete_category, name='delete_category'),
    path('create_category/', views.create_category, name='create_category'),
    path('delete_ingredient/<int:ing_id>/', views.delete_ingredient, name='delete_ingredient'),
    path('create_ingredient/', views.create_ingredient, name='create_ingredient'),



    path('newrecipe/',  views.createRecipe, name = "createRecipe"),
    path('updaterecipe/<str:pk>',  views.updateReceita, name = "updateReceita"),
    path('deleterecipe/<str:pk>',  views.deleteRecipe, name = "deleteRecipe"),

    path('planner/', views.planner, name='planner'),
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)