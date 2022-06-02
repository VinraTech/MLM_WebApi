from django.db import models

# Create your models here.

class ProductColours(models.Model):
    colour_name = models.CharField(max_length=20)
    def __str__(self):
        return self.colour_name

class SubCategories(models.Model):
    sub_category = models.CharField(max_length=20)

    def __str__(self):
        return self.sub_category

class Categories(models.Model):
    category = models.CharField(max_length=20)
    sub_category = models.ForeignKey(SubCategories, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

class Review(models.Model):
    rating = models.FloatField()
    message = models.TextField()

# COLOR_CHOICES = (
#     ('GREEN','GREEN'),
#     ('YELLOW','YELLOW'),
#     ('BLUE','BLUE'),
#     ('RED','RED'),
# )

# CATEGORIES_CHOICES = (
#     ('BOTTOM','BOTTOM'),
#     ('FOOTWEAR','FOOTWAER'),
#     ('JEANS','JEANS'),
# )

class Product(models.Model):
    product_id = models.PositiveBigIntegerField()     ##### id or integer field
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    # category = models.CharField(max_length=100,choices=CATEGORIES_CHOICES) ####
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()   ##### should be on cart
    colour = models.ForeignKey(ProductColours, on_delete=models.CASCADE)
    # colour = models.CharField(max_length=100, choices=COLOR_CHOICES)####
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    image = models.ImageField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)


    def __str__(self):
        return self.name