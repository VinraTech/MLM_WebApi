from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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
    country = models.CharField(max_length=100)

    def __str__(self):
        return "{0}, {1}, {2}, {3}".format(self.address_line_1, self.address_line_2, self.city, self.pincode)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nric_no = models.BigIntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=SELECT_GENDER,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    day = models.CharField(max_length=30, null=True,blank=True)
    month = models.CharField(max_length=30,null=True,blank=True)
    year = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(unique=True)
    mobile_no = models.BigIntegerField()
    addresses = models.ManyToManyField(CustomerAddress,blank=True)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE,null=True,blank=True)
    # city = models.CharField(max_length=20, null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    customer_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    referrer_id = models.IntegerField(null=True)
    referrer_name = models.CharField(max_length=100,null=True)
    profile_pic = models.ImageField(upload_to="images/profile/", null=True)
    def __str__(self):
        return self.full_name

class ResetPasswordOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField(null=True,blank=True)
    token = models.CharField(max_length=100)
    generated_on = models.DateTimeField(auto_now_add=True)
    expired_on = models.DateTimeField(null=True)
    
