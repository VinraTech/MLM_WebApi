from django.contrib import admin
from .models import ProductColours,Product,Categories
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Product,ProductAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category',)
admin.site.register(Categories,CategoriesAdmin)

class ProductColoursAdmin(admin.ModelAdmin):
    list_display = ('colour_name',)
admin.site.register(ProductColours,ProductColoursAdmin)
