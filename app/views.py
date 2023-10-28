from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from datetime import datetime

from .models import Receita
from .forms import ReceitaForm

# Create your views here.

""" receitas = [
    {'id':1, 'name' : 'bacalhau à brás'},
    {'id':2, 'name' : 'carbonara'},
    {'id':3, 'name' : 'carne de porco à alentejana'},

] """

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

def fridge(request):

    """ ingredient = None
    for i in ingredients:
        if i['id'] == int(pk):
            ingredient = i """
    
    receitas = Receita.objects.all()
    context = {'receitas': receitas}
    return render(request,'fridge.html', context)

def createRecipe(request):

    form = ReceitaForm()
    if request.method == 'POST':
        #print(request.POST) printa o dicionário da informação que vai para a base de dados
        form = ReceitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form}
    return render(request,'newrecipe.html', context)

def updateReceita(request,pk):
    recipe = Receita.objects.get(id=pk)
    form = ReceitaForm(instance=recipe)

    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('fridge')

    context = {'form': form}
    return render(request,'newrecipe.html', context)

def deleteRecipe(request,pk):
    recipe = Receita.objects.get(id=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('index')
    
    return render(request,'delete.html', {'obj' : 'recipe'})

