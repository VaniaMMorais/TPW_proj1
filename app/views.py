from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse, JsonResponse 

from datetime import datetime

from webproj import settings
from .models import Receita
from .models import Categoria
from .models import Planificacao
from .forms import ReceitaForm, LoginForm


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token

# Create your views here.

""" receitas = [
    {'id':1, 'name' : 'bacalhau à brás'},
    {'id':2, 'name' : 'carbonara'},
    {'id':3, 'name' : 'carne de porco à alentejana'},

] """

def hello(request):
    return HttpResponse("Hello World!")


def index(request, username):
    user = User.objects.get(username=username)
    receitas = Receita.objects.all()
    return render(request, 'index.html', {'receitas': receitas, 'fname': user.first_name})

def loginp(request):
    return render(request,'login.html')


def about(request):
    nreceitas = Receita.objects.all().count()
    nvegan = Receita.objects.filter(category=13).count()
    ncarne = Receita.objects.filter(category=6).count()
    nsobremesa = Receita.objects.filter(category=9).count()
    return render(request, 'about.html', {"nreceitas": nreceitas, "nvegan": nvegan, "ncarne": ncarne, "nsobremesa": nsobremesa})


def blogpost(request):
    return render(request,'blog-post.html')


def elements(request):
    return render(request,'elements.html')


def recipepost(request, id):
    receita = Receita.objects.get(id=id)
    return render(request,'recipe-post.html', {'receita': receita})

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
            if request.user.is_authenticated:
                return redirect('index', username=request.user.username)

    context = {'form': form}
    return render(request,'newrecipe.html', context)

def updateReceita(request,pk):
    recipe = Receita.objects.get(id=pk)
    form = ReceitaForm(instance=recipe)

    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated:
                return redirect('index', username=request.user.username)

    context = {'form': form}
    return render(request,'newrecipe.html', context)

def deleteRecipe(request,pk):
    recipe = Receita.objects.get(id=pk)
    if request.method == 'POST':
        recipe.delete()
        if request.user.is_authenticated:
                return redirect('index', username=request.user.username)
    
    return render(request,'delete.html', {'obj' : 'recipe'})

def filtered_recipies(request, cat):
    receitas = Receita.objects.filter(category=cat)
    return render(request, 'filteredrecipies.html', {'receitas': receitas})


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('loginp')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('loginp')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('loginp')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('loginp')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('loginp')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = True
        myuser.save()
        messages.success(request,
                         "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")


        return redirect('signin')

    return render(request, "signup.html")


def activate(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(request, username=username, password=pass1)  # Corrigido para passar 'request'

        if user is not None:
            login(request, user)
            return redirect('index', username=user.username)
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('loginp')

    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('loginp')

# VIEWS para a PLANIFICAÇÃO
def planner(request):  
    all_events = Planificacao.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'planner.html',context)
 
def all_events(request):                                                                                                 
    all_events = Planificacao.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'recipe': event.receita.name,    
            'categoria': event.category,                                                                             
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 
 
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    recipe = request.GET.get("recipe", None)
    category = request.GET.get("category", None)
    
    # Certifique-se de que a receita e a categoria sejam válidas
    if recipe and category:
        event = Planificacao(
            receita=Receita.objects.get(id=recipe), 
            category=CategoriaRefeicao.objects.get(id=category),
            start=start, 
            end=end
        )
        event.save()
    
    data = {}
    return JsonResponse(data)

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    recipe = request.GET.get("recipe", None)
    id = request.GET.get("id", None)
    category = request.GET.get("category", None)

    if id:
        event = Planificacao.objects.get(id=id)
        event.start = start
        event.end = end

        # Certifique-se de que a receita e a categoria sejam válidas
        if recipe and category:
            event.receita = Receita.objects.get(id=recipe)
            event.category = CategoriaRefeicao.objects.get(id=category)

        event.save()

    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Planificacao.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)


