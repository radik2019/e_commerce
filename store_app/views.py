from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import (
    Customer,
    Cart,
    Product,
    Category,
    SubCategory
)


def index(request):
    print(request.COOKIES)
    pr = Product.objects.all()
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    if request.method == "POST":
        rqst = request.POST

        Product.objects.create(
            name=rqst.get('name'),
            category=Category.objects.get(name=rqst.get('cat')),
            sub_cat=SubCategory.objects.get(name=rqst.get('subcategory'))
        )
        print(Product.objects.all())
    context = {
        "auth": request.user.is_authenticated,
        "p": pr,
        "cat": cat,
        "subcat": subcat,
        "title": "Homepage",
        "name": request.user.username
    }
    if request.user.is_authenticated:
            return render(request, 'store_app/index.html', context)
    return render(request, 'store_app/auth_error.html', context)

def login_view(request):
    context = {'error': False,
               "title": "Login",
               "auth": request.user.is_authenticated}
    if request.method == "POST":
        context['error'] = "Login o password non corrette"
        user = authenticate(username=request.POST.get("username"),
                        password=request.POST.get("password"))
        if user is not None:
            
            login(request, user)
            return redirect('/')
 
        return render(request, "store_app/login.html", context)
    return render(request, "store_app/login.html", context)

def logout_view(request):
    logout(request)
    context = {"auth": request.user.is_authenticated}
    return redirect('/')
    # return render(request, 'store_app/login.html', context)


def register(request):
    context = {
        "name": request.user.username
        }
    if request.method == 'POST':
        print('\n\n', request.POST.dict)
    return render(request, 'store_app/register.html', context)




