from django.db import models
from django.contrib.auth.models import User
from utils import subtract_perecnt
from django.forms.models import model_to_dict
# from store_app.models import *



class Customer(models.Model):
    
    name = models.CharField(max_length=255, blank=True, null=True)
    debt_card = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.JSONField(null=True, name="address")
    
    def __str__(self):
        return self.name
    
    @property
    def get_json_data(self):
        dct = {
            'id': self.pk,
            'username': self.user.username,
            'name': self.name,
            'debt_card': self.debt_card,
            'email': self.user.email
        }
        return dct


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, blank=True, null=True)
    avaiability = models.IntegerField(default=0, null=True, blank=True)
    delivered = models.BooleanField(default=False)
    delivery_date = models.DateField(null=True, blank=True)

    @property
    def address(self):
        return self.customer.address

    @property
    def get_avaiability(self):
        if self.avaiability > self.product:
            return False
        return True
    
    def __str__(self):
        s = f"Order {self.customer.user.username} {self.product.name}"
        return s


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    avaiability = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"Cart {self.user.name}"
    
    @property
    def get_sum_of_product_cost(self):
        return round(self.product.price * self.avaiability, 2)
    
    @property
    def get_discounted_sum(self):
        return round(self.product.discounted_price * self.avaiability, 2)

    @property
    def get_json_data(self):
        dct = {
            'id': self.pk,
            'user': self.user.get_json_data,
            'avaiability': self.avaiability,
            'product': self.product.get_json_data
        }
        return dct


class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
    first_add_date = models.DateField(
        verbose_name="Data quando e` stato aggiunto per la prima volta",
        auto_now_add=True,
        null=True,
        blank=True
    )
    avaiability = models.IntegerField(default=0, null=True, blank=True, verbose_name="Quantita` di prodotti nel magazzino")
    price = models.FloatField(default=0.00, null=True, blank=True)
    code_product = models.CharField(max_length=234, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255)
    discount = models.FloatField(default=0.00, null=True, blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    sub_cat = models.ForeignKey(
        'SubCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    
    @property
    def get_immage(self):
        try:
            return self.image.url
        except:
            return None

    @property
    def get_json_data(self):
        dct = model_to_dict(self)
        dct["image"] = self.get_immage
        return (dct)
    
    @property
    def discounted_price(self):
        return subtract_perecnt(self.price, self.discount)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sub_cat = models.ManyToManyField(
        'SubCategory',
        blank=True
    )
    def __str__(self):
        return self.name
    
    def get_sub_cat(self):
        cat = self.sub_cat.all()
        return [subcategory.name for subcategory in cat]


class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


