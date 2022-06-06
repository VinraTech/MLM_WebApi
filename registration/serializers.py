from logging import raiseExceptions
from tokenize import group
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login','password','is_active')

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ('__all__')

class CustomerSerializer(serializers.ModelSerializer):
    addresses = CustomerAddressSerializer(many=True, read_only=True)
    
    class Meta:
        model = Customer
        fields = ('__all__')

