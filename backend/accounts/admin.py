from django.contrib import admin
from .models import User, Address, OTP


admin.site.register(User)
admin.site.register(Address)
admin.site.register(OTP)