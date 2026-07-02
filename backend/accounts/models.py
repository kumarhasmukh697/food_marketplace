from django.db import models
from django.contrib.auth.models import AbstractUser



# user model to store user information and roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("vendor", "Vendor"),
        ("delivery", "Delivery"),
        ("admin", "Admin"),
    )

    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default="customer",)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField( upload_to="profile_pictures/",blank=True,null=True,)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True, blank=True)

    def __str__(self):
        return self.username



# Address model to store user addresses
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="addresses",)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.city}"



# OTP model to store one-time passwords for various purposes
class OTP(models.Model):
    PURPOSE_CHOICES = (
        ("registration", "Registration"),
        ("login", "Login"),
        ("forgot_password", "Forgot Password"),
        ("phone_verification", "Phone Verification"),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="otps",)
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.purpose}"

