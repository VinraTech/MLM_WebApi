from django.urls import path
from .views import *

urlpatterns = [
    path('product_image/<int:pk>/', ProductImageAPI.as_view(), name='ProductImageDetails'),

    # Address APIs
    path('customer_address/', CustomerAddressAPI.as_view(), name='CustomerAddressAPI'),
    path('customer_address/<int:pk>/', CustomerAddressAPI.as_view(), name='CustomerAddressIdAPI'),

    # Products APIs
    path('product/', ProductsAPI.as_view(), name='ProductsAPI'),
    path('product/<int:pk>/', ProductsAPI.as_view(), name='ProductsIdAPI'),

    # Cart APIs
    path('cart/', CartAPI.as_view(), name='CartAPI'),
    path('cart/<int:pk>/', CartAPI.as_view(), name='CartIdAPI'),
]
