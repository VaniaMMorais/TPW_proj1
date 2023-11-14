from django.contrib.auth import authenticate
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse 
from django.utils import timezone
import datetime

from webproj import settings
from .models import Avaliacao, Frigorifico, Ingrediente, Receita, Favoritos, ListaCompras, ReceitaIngrediente, Categoria
from .forms import CategoryForm, FridgeForm, ComentarioForm, IngredienteForm, ReceitaForm, LoginForm, ShoplistForm,UserProfileForm

from django.shortcuts import get_object_or_404
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
from django.db.models import Avg
from django.db.models import Count

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from app import models
from django.contrib import messages
from datetime import date


from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

# Create your views here.

def hello(request):
    return HttpResponse("Hello World!")


def index(request, username=None):
    if username: user = User.objects.get(username=username)
    else: user = request.user
    # user = User.objects.get(username=username)
    receitas = Receita.objects.all().annotate(media_avaliacoes=Avg('avaliacao__clasificacao'))
    contagem_categorias = Receita.objects.values('category__name').annotate(contagem=Count('category__name')).order_by('category__name')

    nreceitas = Receita.objects.all().count()
    nvegan = contagem_categorias.filter(category__name='Vegan').first()['contagem']
    ncarne = contagem_categorias.filter(category__name='Meat').first()['contagem']
    nsobremesa = contagem_categorias.filter(category__name='Dessert').first()['contagem']

    return render(request, 'index.html', {'receitas': receitas, "nreceitas": nreceitas, "nvegan": nvegan, "ncarne": ncarne, "nsobremesa": nsobremesa})

def adminPage(request):
    categorias= Categoria.objects.all()
    ingredientes = Ingrediente.objects.all()
    return render(request, 'adminPage.html', {'categorias': categorias, 'ingredientes': ingredientes})

def loginp(request):
    return render(request,'login.html')


def about(request):
    nreceitas = Receita.objects.all().count()
    nvegan = Receita.objects.filter(category=13).count()
    ncarne = Receita.objects.filter(category=6).count()
    nsobremesa = Receita.objects.filter(category=9).count()
    return render(request, 'about.html', {"nreceitas": nreceitas, "nvegan": nvegan, "ncarne": ncarne, "nsobremesa": nsobremesa})

def settings(request):
    return render(request,'settings.html')

def blogpost(request):
    return render(request,'blog-post.html')


def elements(request):
    return render(request,'elements.html')


def recipepost(request, id):
    receita = Receita.objects.get(id=id)
    avaliacoes = Avaliacao.objects.filter(receita=receita)
    media_avaliacoes = Avaliacao.objects.filter(receita__id=id).aggregate(media=Avg('clasificacao'))['media']

    user_fridge = []
    if request.user.is_authenticated:
        user_fridge = Frigorifico.objects.filter(user=request.user).values_list('ingredient', flat=True)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.user = request.user 
            comentario.receita = receita 
            comentario.data = timezone.now()
            comentario.save()
            
    else:
        form = ComentarioForm()
    return render(request,'recipe-post.html', {'receita': receita, 'avaliacoes': avaliacoes, 'media_avaliacoes': media_avaliacoes, 'form': form, 'user_fridge': user_fridge})

def fridge(request):
    user = request.user  # Obtém o usuário logado
    frigorifico_itens = Frigorifico.objects.filter(user=user)
    ingredients = Ingrediente.objects.all()

    form = FridgeForm()  # Crie uma instância do formulário FridgeForm

    context = {'frigorifico_itens': frigorifico_itens, 'ingredients': ingredients, 'form': form}
    return render(request, 'fridge.html', context)


def shoplist(request):

    user = request.user
    #ingredientes_na_shoplist = ListaCompras.objects.filter(user=user, checklist=True).select_related('ingredient')
    ingredientes_na_shoplist = ListaCompras.objects.filter(user=user)
    todos_ingredientes = Ingrediente.objects.all()

    return render(request, 'shoplist.html', {'ingredientes_na_shoplist': ingredientes_na_shoplist, 'todos_ingredientes': todos_ingredientes})

def add_ingredient_to_shoplist(request):
    if request.method == 'POST':
        form = ShoplistForm(request.POST)
        if form.is_valid():
            ingrediente_id = form.cleaned_data['ingredient'].id

            # Verificar se o ingrediente já está na lista de compras
            if ListaCompras.objects.filter(user=request.user, ingredient__id=ingrediente_id).exists():
                messages.warning(request, 'This ingredient is already in your shopping list.')
                return redirect('shoplist')
            else:
                # Adicionar o ingrediente à lista de compras
                ingrediente = Ingrediente.objects.get(pk=ingrediente_id)
                ListaCompras.objects.create(user=request.user, ingredient=ingrediente, data=date.today(), checklist=False)
                messages.success(request, f'{ingrediente.nome} added to your shopping list.')

                return redirect('shoplist')  # Redireciona de volta à página da lista de compras ou outra página apropriada
    else:
        form = ShoplistForm()  # Crie uma instância do formulário ShoplistForm

    ingredientes_na_shoplist = ListaCompras.objects.filter(user=request.user)
    print("Passei aqui!!!!")

    return render(request, 'shoplist.html', {'form': form, 'ingredientes_na_shoplist': ingredientes_na_shoplist})

def delete_shoplist_item(request, item_id):
    item = get_object_or_404(ListaCompras, id=item_id)
    item.delete()
    return redirect('shoplist')

def favorites(request):
    if request.user.is_authenticated:
        user_favorites = Favoritos.objects.filter(user=request.user).select_related('receita')
        favorite_recipes = user_favorites.annotate(media_avaliacoes=Avg('receita__avaliacao__clasificacao'))

        context = {'receitas': favorite_recipes}
        return render(request, 'favorites.html', context)
    else:
        return redirect('login')
    
def add_to_favorites(request, pk):
    if request.user.is_authenticated:
        try:
            receita = Receita.objects.get(pk=pk)
            favorito, created = Favoritos.objects.get_or_create(user=request.user, receita=receita)

            if not created:
                message = "Recipe is already in your favorites."
                success = False
            else:
                message = "Recipe added to favorites successfully."
                success = True

        except Receita.DoesNotExist:
            message = "Recipe not found."
            success = False
    else:
        message = "You must be logged in to add recipes to favorites."
        success = False

    return JsonResponse({'success': success, 'message': message})

@login_required
def remove_from_favorites(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    
    favorito = Favoritos.objects.filter(user=request.user, receita=receita).first()

    if favorito:
        favorito.delete()
    
    return redirect('favorites')



def myrecipes(request):
    
    if request.user.is_authenticated:
        
        user_recipes = Receita.objects.filter(user=request.user).annotate(media_avaliacoes=Avg('avaliacao__clasificacao'))
        context = {'receitas': user_recipes}

        return render(request, 'myrecipes.html', context)
    else:
        
        return redirect('login')  # Certifique-se de ajustar 'login' para a URL real da sua página de login

def delete_item(request, item_id):
    item = get_object_or_404(Frigorifico, id=item_id)
    item.delete()
    return redirect('fridge')

def add_ingredient_to_fridge(request):
    if request.method == 'POST':
        form = FridgeForm(request.POST)
        if form.is_valid():
            fridge = form.save(commit=False)
            fridge.ingredient = form.cleaned_data['ingredient']
            fridge.user = request.user
            fridge.data = timezone.now()  # Defina a data atual
            fridge.checklist = False
            fridge.save()
            return redirect('fridge')  # Redireciona de volta à página do frigorífico ou outra página apropriada
    else:
        form = FridgeForm()  # Crie uma instância do formulário FridgeForm

    frigorifico_itens = Frigorifico.objects.filter(user=request.user)
    ingredients = Ingrediente.objects.all()

    return render(request, 'fridge.html', {'form': form, 'frigorifico_itens': frigorifico_itens, 'ingredients': ingredients})


def delete_category(request, cat_id):
    categoria = get_object_or_404(Categoria, id=cat_id)

    if request.method == 'POST':
        # Realize a exclusão da categoria
        categoria.delete()
        return redirect('adminPage')  # Redirecione para a página de categorias ou outra página apropriada

    return render(request, 'confirm_delete_category.html', {'categoria': categoria})

def delete_ingredient(request, ing_id):
    ingrediente = get_object_or_404(Ingrediente, id=ing_id)

    if request.method == 'POST':
        # Realize a exclusão do ingrediente
        ingrediente.delete()
        return redirect('adminPage')  # Redirecione para a página de ingredientes ou outra página apropriada

    return render(request, 'confirm_delete_ingredient.html', {'ingrediente': ingrediente})


def create_ingredient(request):
    if request.method == 'POST':
        ingredient = request.POST.get('ingredientName')
        if ingredient:
            Ingrediente.objects.create(nome= ingredient)
            return redirect('adminPage')  # Redirecione para a página apropriada

    return render(request, 'create_ingredient.html')


def create_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('categoryName')
        if category_name:
            Categoria.objects.create(name=category_name)
            return redirect('adminPage')  # Redirecione para a página que lista todas as categorias

    return render(request, 'create_category.html')


def createRecipe(request):
    form = ReceitaForm()
    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.user = request.user
            receita.save()
            
            # Limpe os ingredientes associados à receita
            receita.ingredients.clear()

            # Associe os ingredientes selecionados à receita
            ingredientes_selecionados = request.POST.getlist('ingredients')
            for ingrediente_id in ingredientes_selecionados:
                ingrediente = Ingrediente.objects.get(pk=ingrediente_id)
                ReceitaIngrediente.objects.create(receita=receita, ingrediente=ingrediente, quantidade=1.0)

            if request.user.is_authenticated:
                return redirect('index')

    context = {'form': form}
    return render(request, 'newrecipe.html', context)


def updateReceita(request,pk):
    recipe = Receita.objects.get(id=pk)
    form = ReceitaForm(instance=recipe)

    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated:
                return redirect('index')

    context = {'form': form}
    return render(request,'newrecipe.html', context)

def deleteRecipe(request,pk):
    recipe = Receita.objects.get(id=pk)
    if request.method == 'POST':
        recipe.delete()
        if request.user.is_authenticated:
                return redirect('index')
    
    return render(request,'delete.html', {'obj' : 'recipe'})

def filtered_recipies(request, cat=None, nome=None):
    nome = request.GET.get('name')
    receitas = Receita.objects.all()

    if cat:
        receitas = receitas.filter(category=cat).annotate(media_avaliacoes=Avg('avaliacao__clasificacao'))

    if nome:
        receitas = receitas.filter(name__icontains=nome).annotate(media_avaliacoes=Avg('avaliacao__clasificacao'))

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
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!!")
            return redirect('signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')

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
            return redirect('index')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')

    return render(request, "signin.html")


def signout(request):
    logout(request)
    #messages.success(request, "Logged Out Successfully!!")
    return redirect('index')


@login_required
def user_settings(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)

        if form.is_valid():
            
            old_password = form.cleaned_data.get('password')
            if old_password and not user.check_password(old_password):
                messages.error(request, 'Old password is incorrect.')
            else:
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('user_settings')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors.')

    else:
        form = UserProfileForm(instance=user)

    return render(request, 'settings.html', {'form': form})