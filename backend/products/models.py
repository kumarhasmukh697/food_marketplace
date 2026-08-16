from django.db import models
from categories.models import Category
from vendors.models import VendorProfile


class Product(models.Model):
    vendor = models.ForeignKey(VendorProfile,on_delete=models.CASCADE,related_name="products")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True, blank=True,related_name="products",)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    is_veg = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

    