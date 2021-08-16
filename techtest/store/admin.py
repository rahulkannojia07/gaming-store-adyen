from django.contrib import admin
from .models import ProductDetails, ProductCart
# Register your models here.


class ProductDetailsAll(admin.ModelAdmin):
    list_display = ['product_id', 'product_name', 'product_price']
    search_fields = ['product_id']
    ordering = ['-product_id']

class ProductCartAll(admin.ModelAdmin):
    list_display = ['product_id', 'product_name', 'product_price','qty']
    search_fields = ['product_id']
    ordering = ['-product_id']


admin.site.register(ProductDetails, ProductDetailsAll)
admin.site.register(ProductCart, ProductCartAll)