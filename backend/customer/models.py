from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class CustomerProfile(models.Model):
    DIETARY_PREFERENCE_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('non_vegetarian', 'Non Vegetarian'),
    ]

    SPICE_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer",)
    dietary_preference = models.CharField(max_length=20,choices=DIETARY_PREFERENCE_CHOICES,default='vegetarian',)
    spice_level = models.CharField(max_length=10,choices=SPICE_LEVEL_CHOICES,default='medium',)
   
    def __str__(self):
        return self.user.username
