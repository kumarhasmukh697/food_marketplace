from django.db import models
from django.conf import settings
from vendors.models import VendorProfile

User = settings.AUTH_USER_MODEL

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name="favorite_restaurants")
    vendor = models.ForeignKey( VendorProfile, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "vendor"],
                name="unique_user_favorite_restaurant"
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.vendor.shop_name}"