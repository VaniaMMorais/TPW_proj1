"""webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Route directory urls file
from django.contrib import admin
from django.urls import include,path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.conf import settings
from django.conf.urls.static import static


from app import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('hello/', views.hello, name='hello'),
    path('index/', views.index, name='index'),
    path('',include('app.urls')),
    path('about/', views.about, name='about'),
    path('blog-post/', views.blogpost, name='blogPost'),
    path('elements/', views.elements, name='elements'),
    path('recipe-post/', views.recipepost, name='recipePost'),
    path('login/', views.login, name='login'),

    path('planner/', views.planner, name='planner'), 
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)