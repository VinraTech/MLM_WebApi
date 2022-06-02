from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50)

SELECT_GENDER=(
    ('MALE','MALE'),
    ('FEMALE','FEMALE')
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=SELECT_GENDER)
    dob = models.DateField()
    mobile_no = models.BigIntegerField()
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.full_name

class ResetPasswordOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    generated_on = models.DateTimeField(auto_now_add=True)
    expired_on = models.DateTimeField(null=True)
    
