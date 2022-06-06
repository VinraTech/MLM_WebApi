from rest_framework import serializers
from .models import *
class ResellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseller
        fields = ('__all__')