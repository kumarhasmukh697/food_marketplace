from django.contrib import admin
from .models import CustomerProfile

# Register your models here.
@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dietary_preference', 'spice_level')
    search_fields = ('user__username', 'user__email')
    list_filter = ('dietary_preference', 'spice_level')
