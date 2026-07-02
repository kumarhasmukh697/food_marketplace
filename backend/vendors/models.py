from django.conf import settings
from django.db import models


# get the user model from settings
user = settings.AUTH_USER_MODEL


class Vendor(models.Model):
    user = models.OneToOneField(user,on_delete=models.CASCADE,related_name="vendor_profile",)
    shop_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name