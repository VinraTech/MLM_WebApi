from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50)

SELECT_GENDER=(
    ('MALE','MALE'),
    ('FEMALE','FEMALE')
)

class CustomerAddress(models.Model):
    is_primary = models.BooleanField(default=False)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    mobile_no = models.BigIntegerField()

    def __str__(self):
        return "{0}, {1}, {2}, {3}".format(self.address_line_1, self.address_line_2, self.city, self.pincode)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=SELECT_GENDER)
    dob = models.DateField()
    mobile_no = models.BigIntegerField()
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=20, null=True)
    addresses = models.ManyToManyField(CustomerAddress)
    
    def __str__(self):
        return self.full_name

class ResetPasswordOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    generated_on = models.DateTimeField(auto_now_add=True)
    expired_on = models.DateTimeField(null=True)
    
