from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Country)
admin.site.register(Customer)
admin.site.register(CustomerAddress)
admin.site.register(ResetPasswordOTP)
