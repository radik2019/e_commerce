from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from utils import debug_
from .models import (
    Customer,
    Cart,
    Product,
    Category,
    SubCategory
)



def auth_superuser(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, "store_app/message.html", {"message": "error 403 Accesso negato!!"})
            raise PermissionDenied("accesso negato")
        return func(request, *args, **kwargs)
    return wrapper


def get_mycontext(request):
    context = {
    "title": "",
    "name": request.user.username,
    "message": '',
    "auth": request.user.is_authenticated,
    "reg_type": "registersuperuser",
    "user": request.user
    }
    return context


def index(request):
    pr = [i for i in Product.objects.all()]
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
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


@auth_superuser
def modifie_product(request, my_id):
    
    context = get_mycontext(request)
    context["p"] = Product.objects.all()
    context["cat"] = Category.objects.all()
    context["subcat"] = SubCategory.objects.all()

    try:
        product = Product.objects.get(pk=my_id)
        context['message'] = "prodotto aggiornato"
        context["product"] = product
        context["nm"] = product.name
        if request.method == "POST":
            product.name = request.POST.get("name")
            product.category = Category.objects.get(name=request.POST.get("cat"))
            product.sub_cat = SubCategory.objects.get(name=request.POST.get("subcategory"))
            product.price = request.POST.get("price")
            product.avaiability = request.POST.get("avaiability")
            product.code_product = request.POST.get("code_product")
            product.discount = request.POST.get("discount")
            
            product.save()
            context["message"] = "Le modifiche sono state salvate con successo"
            
            return render(request, "store_app/message.html", context)
            
    except ObjectDoesNotExist:
        context['message'] = "prodotto inesistente"
        render(request, "store_app/message.html", context)
    
    return render(request, 'store_app/modifie_product.html', context)


def add_prod(request):
    if request.method == "POST":
        rqst = request.POST
        pp = Product.objects.create(
            name=rqst.get('name'),
            category=Category.objects.get(name=rqst.get('cat')),
            sub_cat=SubCategory.objects.get(name=rqst.get('subcategory')),
            discount = rqst.get('discount'),
            code_product = rqst.get('code_product'),
            price = rqst.get('price'),
            avaiability = rqst.get('avaiability'),
        )

    context = get_mycontext(request)
    context["p"] = Product.objects.all()
    context["cat"] = Category.objects.all()
    context["subcat"] = SubCategory.objects.all()
    if request.user.is_authenticated:
            return render(request, 'store_app/insert_data.html', context)
    return render(request, 'store_app/auth_error.html', context)


def login_view(request):
    context = get_mycontext(request)
    context["title"] = "Login"
    context["error"] = False
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
    return redirect('/')


def register_user(request):
    context = get_mycontext(request)
    context["title"] = "Register User"

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
    context = get_mycontext(request)
    context["title"] = "Register Superuser"
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
    context = get_mycontext(request)
    context["title"] = "Allusers"
    context["users"] = User.objects.all()
    return render(request, "store_app/allusers.html", context)

# @auth_superuser
def detail_product(request, my_id):
    context = get_mycontext(request)
    context["title"] = "Detail Product"
    context["product"] = Product.objects.get(pk=my_id)
    return render(request, "store_app/detail_product.html", context)



def remove_detail(request, my_id):
    context = get_mycontext(request)

    try:
        Product.objects.get(pk=my_id).delete()
        context['message'] = "prodotto rimosso"

    except ObjectDoesNotExist:
        context['message'] = "prodotto inesistente"
        render(request, "store_app/message.html", context)
    return render(request, "store_app/message.html", context)
