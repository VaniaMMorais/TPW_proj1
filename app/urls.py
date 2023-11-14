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
    path('settings/', views.settings, name="settings"),
    path('adminPage/', views.adminPage, name="adminPage"),

    # views para a shoplist
    path('shoplist/', views.shoplist, name='shoplist'),
    path('add_ingredient_to_shoplist/', views.add_ingredient_to_shoplist, name='add_ingredient_to_shoplist'),
    path('delete_shoplist_item/<int:item_id>/', views.delete_shoplist_item, name='delete_shoplist_item'),


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
    path('add_to_favorites/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:pk>/', views.remove_from_favorites, name='remove_from_favorites'),

    path('settings/', views.user_settings, name='user_settings'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)