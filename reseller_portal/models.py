from django.db import models
from django.contrib.auth.models import User
from registration.models import Country
# Create your models here.
SELECT_GENDER=(
    ('MALE','MALE'),
    ('FEMALE','FEMALE'),
)
ADDR_DOC_TYPE_CHOICES=(
    ('DOC1','DOC1'),
)

class Reseller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=SELECT_GENDER, null=True, blank=True)
    dob = models.DateField(null=True,blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.BigIntegerField(null=True, blank=True)
    mobile_no = models.BigIntegerField()
    unit_no = models.IntegerField(null=True,blank=True)
    address_1 = models.CharField(max_length=100, null=True, blank=True)
    address_2 = models.CharField(max_length=100, null=True, blank=True)
    billing_add_1 = models.CharField(max_length=100, null=True, blank=True)
    delivery_add_2 = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.IntegerField(null=True,blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)

    bank_name = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    bank_acc_no = models.BigIntegerField(null=True, blank=True)

    nric_no = models.BigIntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=50)
    address_doc_type = models.CharField(max_length=50, choices=ADDR_DOC_TYPE_CHOICES, null=True, blank=True)
    address_doc_no = models.BigIntegerField(null=True, blank=True)