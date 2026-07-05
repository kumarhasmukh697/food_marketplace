from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('is_available', 'category', 'vendor')
    search_fields = ('name', 'description', 'vendor__shop_name', 'category__name')

admin.site.register(Product, ProductAdmin)
