

from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from utils import debug_
from .models import (
    Customer,
    Cart,
    Product,
    Category,
    SubCategory
)
import datetime



def all_product(request):
    debug_(dir(request.method))
    collection = Product.objects.all()
    serializated = [*map(lambda m: model_to_dict(m), collection)]
    serializated = [model_to_dict(i) for i in collection]

    debug_(collection[0].get_json_data)

    return JsonResponse(serializated, status=200, safe=False)
