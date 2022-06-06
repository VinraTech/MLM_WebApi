from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Product,ProductAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category',)
admin.site.register(Categories,CategoriesAdmin)

class ProductColorsAdmin(admin.ModelAdmin):
    list_display = ('color_name',)
admin.site.register(ProductColors,ProductColorsAdmin)

admin.site.register(SubCategories)
admin.site.register(ProductImages)
admin.site.register(Cart)
