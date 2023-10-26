from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from datetime import datetime

# Create your views here.
def hello(request):
    return HttpResponse("Hello World!")


def index(request):
    return render(request,'index.html')


def about(request):
    return render(request, 'about.html')


def blogpost(request):
    return render(request,'blog-post.html')




def elements(request):
    return render(request,'elements.html')


def recipepost(request):
    return render(request,'recipe-post.html')