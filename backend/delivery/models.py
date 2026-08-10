from django.db import models
from django.conf import settings


# Create your models here.
User = settings.AUTH_USER_MODEL

class DeliveryPartnerProfile(models.Model):

    VEHICLE_CHOICES = [
        ("bike", "Bike"),
        ("scooter", "Scooter"),
        ("bicycle", "Bicycle"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="delivery_partner",
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_CHOICES,
    )

    vehicle_number = models.CharField(max_length=20)

    driving_license_number = models.CharField(max_length=30)

    is_available = models.BooleanField(default=True)

    is_online = models.BooleanField(default=False)

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=5.00,
    )

    total_deliveries = models.PositiveIntegerField(default=0)
