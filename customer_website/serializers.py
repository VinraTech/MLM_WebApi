from rest_framework import serializers
from registration.models import CustomerAddress
from .models import *

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ('__all__')

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('__all__')

class ProductColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColors
        fields = ('__all__')

class ProductSerializer(serializers.ModelSerializer):
    colors = ProductColorsSerializer(many=True, read_only=True)
    images = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="ProductImageDetails")

    class Meta:
        model = Product
        fields = ('__all__')

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('__all__')