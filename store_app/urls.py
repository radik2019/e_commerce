
from store_app import api_views
from django.urls import path, include

urlpatterns = [
    path('products/', api_views.ProductViews.as_view(), name='productsapi'),
    path('products/<int:id>', api_views.ProductViews.as_view()),
]