

from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout, authenticate, login

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from utils import debug_, subtract_perecnt
from django.contrib.sessions.backends.db import SessionStore
from .models import (
    Customer,
    Cart,
    Order,
    Product,
    Category,
    SubCategory
)


def auth_superuser(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, "store_app/message.html", {"message": "error 403 Accesso negato!!"})
        return func(request, *args, **kwargs)
    return wrapper


def get_mycontext(request):
    context = {
    "title": "",
    "name": request.user.username,
    "message": '',
    "auth": request.user.is_authenticated,
    "reg_type": "registersuperuser",
    "user": request.user,
    "is_staff": request.user.is_staff
    }
    return context


class ViewMixin(View):
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        debug_(args, kwargs)
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class MyAccount(ViewMixin):

    def password_modifier(self, request, new_password):
        usr = Customer.objects.get(user=request.user)
        usr.user.set_password(new_password)
        usr.user.save()

    def get(self, request):
        usr = Customer.objects.get(user=request.user)

        return render(request, 'store_app/user_account.html', get_mycontext(request))

    def post(self, request):
        return HttpResponse('My Account POST result')


class BuyFromCart(ViewMixin):

    def get(self, request):
        debug_("buy_from_cart", "get")
        return HttpResponse('GET result')

    def post(self, request):
        debug_("buy_from_cart", "post")
        return HttpResponse('POST result')


class BuyDetail(ViewMixin):

    def get(self, request):
        debug_("buy_detail", 'get')
        return redirect('cart')

    def post(self, request):
        debug_("buy_detail", 'get')
        return redirect('cart')


class BuyAllCart(ViewMixin):

    def post(self, request):
        context = get_mycontext(request)
        usr = User.objects.get(username=request.user.get_username())
        customer = Customer.objects.get(user=usr)
        cart = Cart.objects.filter(user=customer)
        for product in cart:
            Order.objects.create(
                customer=customer,
                product=product.product,
                avaiability=product.avaiability,)
            product.delete()
        order = ''.join([f'<p style="background-color: gray; color: yellow;">{i.product.name}<p>' for i in Order.objects.filter(customer=customer)])
        return HttpResponse(f"{order}")
    
    def get(self, request):
        context = get_mycontext(request)
        usr = User.objects.get(username=request.user.get_username())
        customer = Customer.objects.get(user=usr)
        cart = Cart.objects.filter(user=customer)
        order = ''.join([f'<p style="background-color: gray; color: yellow;">{i.product.name}<p>' for i in Order.objects.filter(customer=customer)])
        return HttpResponse(f"{order}")


def add_to_order(request):
    context = get_mycontext(request)
    if request.user.is_authenticated and (not request.user.is_staff):
        usr = User.objects.get(username=request.user.get_username())
        customer = Customer.objects.get(user=usr)
        cart = Cart.objects.filter(user=customer)
        if request.method == "POST":
            deleted, lst = [], request.POST.dict()
            pieces_to_remove = {int(i[3:]): lst[i] for i in lst if (i.startswith('pcs') and lst[i].isdigit())}
            product_to_remove = [int(i[2:]) for i in lst if i.startswith('rm')]
            for i in pieces_to_remove:
                prd = cart.get(pk=i)
                rest_of_cart =  prd.avaiability - int(pieces_to_remove[i])
                if rest_of_cart:
                    prd.avaiability = rest_of_cart
                    prd.save()
                    deleted.append(i)
                else:
                    prd.delete()
            for k in product_to_remove:
                if k not in deleted:
                    prd = cart.get(pk=k)
                    prd.delete()
        return render(request, 'store_app/order.html', context)
    return render(request, 'store_app/auth_error.html', context)


def remove_from_cart(request):
    context = get_mycontext(request)
    if request.user.is_authenticated and (not request.user.is_staff):

        usr = User.objects.get(username=request.user.get_username())
        customer = Customer.objects.get(user=usr)
        cart = Cart.objects.filter(user=customer)
        if request.method == "POST":
            deleted, lst = [], request.POST.dict()
            pieces_to_remove = {int(i[3:]): lst[i] for i in lst if (i.startswith('pcs') and lst[i].isdigit())}
            product_to_remove = [int(i[2:]) for i in lst if i.startswith('rm')]
            for i in pieces_to_remove:
                prd = cart.get(pk=i)
                rest_of_cart =  prd.avaiability - int(pieces_to_remove[i])
                if rest_of_cart:
                    prd.avaiability = rest_of_cart
                    prd.save()
                    deleted.append(i)
                else:
                    prd.delete()
            for k in product_to_remove:
                if k not in deleted:
                    prd = cart.get(pk=k)
                    prd.delete()
        return redirect('cart')
    return render(request, 'store_app/auth_error.html', context)


def add_to_cart(request):
    context = get_mycontext(request)
    if request.user.is_authenticated and (not request.user.is_staff):

        usr = User.objects.get(username=request.user.get_username())
        customer = Customer.objects.get(user=usr)
        cart = Cart.objects.filter(user=customer)
        context["cart_summ"] = sum([i.get_sum_of_product_cost for i in cart])
        context["cart_dicounted_summ"] = sum([i.get_discounted_sum for i in cart])
        context["cart"] = cart
        if request.method == "POST":
            if not request.POST.get("avaiability"):
                context["message"] = "Seleziona la quantita` da aggiungere"
                return render(request, 'store_app/message.html', context)
            prd = Product.objects.get(pk=request.POST.get('id'))
            df = cart.filter(product=prd)
            if df:
                df = df[0]
                if (df.avaiability + int(request.POST.get('avaiability'))) > prd.avaiability:
                    context['message'] = f"Puoi aggiungere non piu` di {prd.avaiability - df.avaiability} pezzi"
                    return render(request, 'store_app/message.html', context)
                else:
                    df.avaiability += int(request.POST.get('avaiability'))
                    df.save()
            else:
                cart = Cart.objects.create(
                    user=customer,
                    product=prd,
                    avaiability=request.POST.get('avaiability')
                    )
        return render(request, "store_app/cart.html", context)
    return render(request, 'store_app/auth_error.html', context)


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
        "name": request.user.username,
        "is_staff": request.user.is_staff
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
            system_user = User.objects.create_user(name, email, password1)
            customer = Customer.objects.create(
                name = request.POST.get("name", system_user.username.capitalize()),
                debt_card= request.POST.get("debt_card", ''),
                user = system_user
            )
            context['message'] = "Registrazione andata a buon fine"
            return render(request, 'store_app/message.html', context)
        context['message'] = "tutti i campi sono obbligatori e le password devono coincidere"
        return render(request, 'store_app/message.html', context)
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
    try:
        prd = Product.objects.get(pk=my_id)
        context["product"] = prd
        return render(request, "store_app/detail_product.html", context, status=200)
    except:
        return HttpResponse('----------------', status=404)


def remove_detail(request, my_id):
    context = get_mycontext(request)
    try:
        Product.objects.get(pk=my_id).delete()
        context['message'] = "prodotto rimosso"
    except ObjectDoesNotExist:
        context['message'] = "prodotto inesistente"
        render(request, "store_app/message.html", context)
    return render(request, "store_app/message.html", context)



