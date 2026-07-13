from django.conf import settings
from django.db import models
from accounts.models import Address

User = settings.AUTH_USER_MODEL

class VendorProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vendor_profile",)
    shop_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True,related_name="vendors",)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    accepting_orders = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True) # handleled by admin when any vendor violated the platform rules they he will be make inactive and therefore not be able to sell the product and not customer can see that vendor
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name
    

