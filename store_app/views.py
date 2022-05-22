from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from utils import debug_


from .models import (
    Customer,
    Cart,
    Product,
    Category,
    SubCategory
)


def index(request):
    pr = [i for i in Product.objects.all()]
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    debug_(pr)
    context = {
        "auth": request.user.is_authenticated,
        "user": request.user,
        "pr": pr,
        "cat": cat,
        "subcat": subcat,
        "title": "Homepage",
        "name": request.user.username
    }
    if request.user.is_authenticated:
            return render(request, 'store_app/index.html', context)
    return render(request, 'store_app/auth_error.html', context)



def add_prod(request):
    pr = Product.objects.all()
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    if request.method == "POST":
        rqst = request.POST

        pp = Product.objects.create(
            name=rqst.get('name'),
            category=Category.objects.get(name=rqst.get('cat')),
            sub_cat=SubCategory.objects.get(name=rqst.get('subcategory'))
        )
        debug_(pp)
    context = {
        "auth": request.user.is_authenticated,
        "user": request.user,
        "p": pr,
        "cat": cat,
        "subcat": subcat,
        "title": "Homepage",
        "name": request.user.username
    }
    if request.user.is_authenticated:
            return render(request, 'store_app/insert_data.html', context)
    return render(request, 'store_app/auth_error.html', context)


def login_view(request):
    context = {
        'error': False,
        "title": "Login",
        "auth": request.user.is_authenticated,
        "message":"",               
    }
    if request.method == "POST":
        context['error'] = "Login o password non corrette"
        user = authenticate(username=request.POST.get("username"),
                        password=request.POST.get("password"))
        if user is not None:
            
            login(request, user)
            debug_(User.objects.all() ,user.password)
            return redirect('/')
        return render(request, "store_app/login.html", context)
    return render(request, "store_app/login.html", context)


def logout_view(request):
    logout(request)
    context = {"auth": request.user.is_authenticated}
    return redirect('/')


def register_user(request):
    context = {
        "name": request.user.username,
        "message": '',
        "auth": request.user.is_authenticated,
        "user": request.user,
        "reg_type": "register"
        }

    if request.method == 'POST':
        name = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if name  and email and (password1 == password2):
            user = User.objects.create_user(name, email, password1)
            context['message'] = "Registrazione andata a buon fine"
            return render(request, 'store_app/register.html', context)
        context['message'] = "tutti i campi sono obbligatori e le password devono coincidere"
        return render(request, 'store_app/register.html', context)
    return render(request, 'store_app/register.html', context)



def register_superuser(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    context = {
        "title": "Register Superuser",
        "name": request.user.username,
        "message": '',
        "auth": request.user.is_authenticated,
        "reg_type": "registersuperuser"
        # "user": request.user,
        }

    if request.method == 'POST':
        name = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if name  and email and (password1 == password2):
            user = User.objects.create_superuser(name, email, password1)
            context['message'] = "Registrazione andata a buon fine"
            return render(request, 'store_app/register.html', context)
        context['message'] = "tutti i campi sono obbligatori e le password devono coincidere"
        return render(request, 'store_app/register.html', context)
    return render(request, 'store_app/register.html', context)    
        
        


def all_users(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    u = User.objects.all()
    
    

    context = {
    "title": "Allusers",
    "name": request.user.username,
    "message": '',
    "auth": request.user.is_authenticated,
    "reg_type": "registersuperuser",
    "user": request.user,
    "users": u,
    }

    return render(request, "store_app/allusers.html", context)
    


