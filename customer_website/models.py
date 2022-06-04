from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ProductImages(models.Model):
    image = models.ImageField(upload_to="images/products/")

class ProductColors(models.Model):
    color_name = models.CharField(max_length=20)
    hax_value = models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return self.color_name

class SubCategories(models.Model):
    sub_category = models.CharField(max_length=20)

    def __str__(self):
        return self.sub_category

class Categories(models.Model):
    category = models.CharField(max_length=20)
    sub_category = models.ManyToManyField(SubCategories)

    def __str__(self):
        return self.category

class Product(models.Model):
    product_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    discounted_price = models.FloatField()
    colors = models.ManyToManyField(ProductColors)
    images = models.ManyToManyField(ProductImages)

    def __str__(self):
        return self.name
        

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField()
    message = models.TextField()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_on = models.DateTimeField(auto_now_add=True)