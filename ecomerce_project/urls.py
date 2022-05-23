
from django.contrib import admin
from django.urls import path
from store_app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_user, name='register'),
    path('registersuperuser/', register_superuser, name='registersuperuser'),
    path('addprod/', add_prod, name='addprod'),
    path('allusers/', all_users, name='allusers'),
    path('<int:my_id>/del/', remove_detail,),
    path('<int:my_id>/', detail_product,),
    path('<int:my_id>/', detail_product,),
    path('<int:my_id>/mod/', modifie_product,),
]








