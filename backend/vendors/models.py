from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from accounts.models import Address

User = settings.AUTH_USER_MODEL

class VendorProfile(models.Model):

    FOOD_TYPE_CHOICES = [
        ("veg", "Veg Only"),
        ("non_veg", "Non-Veg Only"),
        ("both", "Veg & Non-Veg"),
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vendor_profile",)
    shop_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True, null=True)
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES, default="both")
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    accepting_orders = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True) # handled by admin when any vendor violated the platform rules they he will be make inactive and therefore not be able to sell the product and not customer can see that vendor
    # Razorpay Route Linked Account ID
    razorpay_account_id = models.CharField( max_length=100, unique=True, null=True, blank=True,)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name

    def _generate_unique_slug(self):
        base_slug = slugify(self.shop_name)[:150]
        slug = base_slug
        index = 1
        while VendorProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{index}"
            index += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug and self.shop_name:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    @property
    def is_open(self):
        if not self.is_active or not self.accepting_orders:
            return False

        now = timezone.localtime().time()
        opening = self.opening_time
        closing = self.closing_time

        if opening == closing:
            return True

        if opening < closing:
            return opening <= now < closing

        return now >= opening or now < closing
    

