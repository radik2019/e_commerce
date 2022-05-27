
from django.contrib import admin
from django.urls import path
from store_app.views import *
from store_app import api_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_user, name='register'),
    path('registersuperuser/', register_superuser, name='registersuperuser'),
    path('allusers/', all_users, name='allusers'),

    path('addprod/', add_prod, name='addprod'),
    path('<int:my_id>/del/', remove_detail,),
    path('<int:my_id>/', detail_product,),
    path('<int:my_id>/mod/', modifie_product,),

    path('cart', add_to_cart, name="cart"),
    path('removefromcart', remove_from_cart, name="removefromcart"),

    path('buyselected/', add_to_order, name="buyselected"),
    path('buyfromcart/', BuyFromCart.as_view(), name="buyfromcart"),
    path('buydetail/', BuyDetail.as_view(), name="buydetail"),
    path('buyallcart/', BuyAllCart.as_view(), name="buyallcart"),

    path('api/products/', api_views.all_product, name='productsapi'),
]

