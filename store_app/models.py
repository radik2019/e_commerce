from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    debt_card = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    avaiability = models.IntegerField(default=0, null=True, blank=True)
    def __str__(self):
        return self


class Product(models.Model):
    first_add_date = models.DateField(auto_now_add=True, null=True, blank=True)
    avaiability = models.IntegerField(default=0, null=True, blank=True)
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


