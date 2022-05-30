
from django.core.serializers.json import DjangoJSONEncoder
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
from django.views.generic import View
import datetime

'''from venv import create
from django.views.generic import View
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from .models import Product, Brand, Category
import json
from hashlib import sha256
from django.views.decorators.csrf import csrf_exempt
'''


'''
class RetrieveRESTViewMixin:
    def get_detail(self, request, pk=None, *args, **kwargs):
        resource = self.model.objects.filter(pk=pk)  # Retrieve
        if not resource.exists():
            return JsonResponse({"detail": "Resource not found"}, status=404)
        return JsonResponse(model_to_dict(resource.first()), status=200, safe=False)


class DeleteRESTViewMixin:
    def del_detail(self, request, pk=None, *args, **kwargs):
        resource = self.model.objects.filter(pk=pk)  # Retrieve
        if not resource.exists():
            return JsonResponse({"detail": "Resource not found"}, status=404)
        resource_name = resource.first()
        try:
            resource_name.delete()
        except ProtectedError:
            return JsonResponse({"error": "Cannot delete some instances of model" /
                                          "because they are referenced through protected foreign keys"},
                                status=500)
        return JsonResponse({"detail": f"[{resource_name}] has been deleted"}, status=200, safe=False)


class CreateRESTViewMixin:
    def create_detail(self, request, *args, **kwargs):
        req_payload = json.loads(request.body)
        try:
            self.model.objects.create(name=req_payload.get("name"))
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Errore nella creazione del modello"}, status=500)
        return JsonResponse(model_to_dict(self.model.objects.get(name=req_payload["name"])), status=201)

    def create_product(self, request):
        """
        {
        "name": "product_name",  # string
        "price": 200.01,      # float
        "availability": 10,   # int
        "category": 3,        # int (id category)
        "brand": 4            # int (id brand)
        }
        """
        try:
            req_payload = json.loads(request.body)
            task = Product.objects.create(
                hash_summ=self.hash_product(req_payload),
                name=req_payload.get("name"),
                price=req_payload.get("price"),
                availability=int(req_payload.get("availability")),
                category=Category.objects.get(pk=req_payload.get("category")),
                brand=Brand.objects.get(pk=req_payload.get("brand"))
            )
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Errore nella creazione del modello"}, status=500)
        return JsonResponse(model_to_dict(task), status=201)


class ListRESTViewMixin:
    def get_list(self, request, *args, **kwargs):
        collection = self.model.objects.all()
        to_serialize = [*map(lambda m: model_to_dict(m), collection)]
        return JsonResponse(to_serialize, status=200, safe=False)


class UpdateRESTViewMixin:
    def update_detail(self, request, pk=None, *args, **kwargs):
        req_payload = json.loads(request.body)
        try:
            obj = self.model.objects.filter(pk=pk)
            obj.update(name=req_payload.get("name"))
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Errore nella modifica del modello"}, status=500)
        return JsonResponse(model_to_dict(self.model.objects.get(pk=pk)), status=201)

    def update_product(self, request, pk=None, *args, **kwargs):
        req_payload = json.loads(request.body)
        try:
            product_obj = Product.objects.filter(pk=pk)

            product_obj.update(hash_summ=self.hash_product(req_payload))
            product_obj.update(name=req_payload.get("name"))
            product_obj.update(price=req_payload.get("price"))
            product_obj.update(availability=req_payload.get("availability"))
            product_obj.update(category=Category.objects.get(
                pk=req_payload.get("category"))),
            product_obj.update(brand=Brand.objects.get(
                pk=req_payload.get("brand")))
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Errore nella modifica del modello"}, status=500)
        return JsonResponse(model_to_dict(Product.objects.get(pk=pk)), status=201)


class RESTView(View):
    model = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        class_name = self.__class__.__name__
        if request.method.lower() in self.http_method_names:

            if request.method.lower() == "get":
                if "pk" in kwargs.keys():
                    handler = getattr(self, "get_detail", self.http_method_not_allowed)
                else:
                    handler = getattr(self, "get_list", self.http_method_not_allowed)

            elif request.method.lower() == "delete":
                handler = getattr(self, "del_detail", self.http_method_not_allowed)

            elif request.method.lower() == "post":
                if class_name == 'ProductView':
                    handler = getattr(self, "create_product", self.http_method_not_allowed)
                else:
                    handler = getattr(self, "create_detail", self.http_method_not_allowed)

            elif request.method.lower() == "put":
                if class_name == 'ProductView':
                    handler = getattr(self, "update_product", self.http_method_not_allowed)
                else:
                    handler = getattr(self, "update_detail", self.http_method_not_allowed)
            else:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({"detail": "Method not allowed!"}, status=405)


class ProductView(RESTView,
                  ListRESTViewMixin,
                  RetrieveRESTViewMixin,
                  DeleteRESTViewMixin,
                  UpdateRESTViewMixin,
                  CreateRESTViewMixin):
    """{
        "name": "updated_product_name",
        "price": int,
        "availability": 10,
        "category": 2,
        "brand": 5
    }
        """
    model = Product

    def hash_product(self, req_payload):
        name: str = req_payload.get("name")
        category = Category.objects.get(pk=req_payload.get("category")).name
        brand = Brand.objects.get(pk=req_payload.get("brand")).name
        s = (name + category + brand).encode(encoding='utf-8')
        hashed = sha256(s).hexdigest()
        return hashed


class BrandView(RESTView,
                ListRESTViewMixin,
                RetrieveRESTViewMixin,
                DeleteRESTViewMixin,
                CreateRESTViewMixin,
                UpdateRESTViewMixin):
    model = Brand
    """
        --- PUT --
    {"name": "modified_brand_name"}

        --- POST ---
    {"name": "category_name"}
    """


class CategoryView(RESTView,
                   ListRESTViewMixin,
                   RetrieveRESTViewMixin,
                   DeleteRESTViewMixin,
                   CreateRESTViewMixin,
                   UpdateRESTViewMixin):
    model = Category
    """
        --- PUT --
    {"name": "modified_category_name"}

        --- POST ---
    {"name": "category_name"}
    """
'''

from django.core.serializers import serialize
import json
from json import JSONEncoder
from typing import Any
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt


class RESTView(View):
    model = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):

        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)



class ProductViews(RESTView):

    def get(self, request, id=None):
        if id:
            query_dict = Product.objects.filter(pk=id)
            if len(query_dict) == 0:
                
                return JsonResponse({"error 404": "prodotto ineststente"}, safe=False, status=204)
            sr = query_dict[0]
            sr = sr.get_json_data
        else:
            query_set = Product.objects.all()
            sr = [i.get_json_data for i in query_set]
        return JsonResponse(sr, safe=False, status=200)
    
    @csrf_exempt
    def post(self, request, id=None):

        if id:
            query_dict = Product.objects.filter(pk=id)
            if len(query_dict) == 0:
                return JsonResponse({"error 404": "prodotto ineststente"}, safe=False, status=204)
            prod = query_dict[0]
            prod.name = prod.name.upper()
            prod.save()
            # allowed_field_names = {
            #     f.name for f in prod._meta.get_fields()
            #     if is_simple_editable_field(f)
            # }
            lst = [fil for fil in prod._meta.get_fields()]
            for i in lst:
                if not i.is_relation:
                    debug_(f'{i.name}, is_relation: {i.is_relation}, is_editable: {i.editable}, is_ID: {i.primary_key}')
                else:
                    
                    n = i.many_to_many
                    if n: n= 'many to many'
                    elif i.many_to_one:
                        n= 'many to one'
                        # debug_(dir(i))
                    elif i.one_to_one: n= 'one to one'
                    elif i.one_to_many: n = 'one to many'


                    debug_(f'---->   {i.model}    {i.name} not_relation , rel_class: {n},')




            return JsonResponse({'asdasd': 'jhgjhgj'}, safe=False)
        debug_('POST Create Products')
        sr = {"method": "Post request"}

        return JsonResponse(sr, safe=False)



def is_simple_editable_field(field):
    return (
            field.editable
            and not field.primary_key
            and not isinstance(field, (ForeignObjectRel, RelatedField))
    )

def update_from_dict(instance, attrs, commit):
    allowed_field_names = {
        f.name for f in instance._meta.get_fields()
        if is_simple_editable_field(f)
    }

    for attr, val in attrs.items():
        if attr in allowed_field_names:
            setattr(instance, attr, val)

    if commit:
        instance.save()