from django.conf import settings
from django.db import models
from accounts.models import Address

User = settings.AUTH_USER_MODEL

class Vendor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vendor_profile",)
    shop_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True,related_name="vendors",)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name