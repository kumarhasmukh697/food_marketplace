from django.contrib import admin
from .models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'description', 'address', 'is_active',)
    search_fields = ('shop_name', 'description', 'address')
    list_filter = ('is_active',)

admin.site.register(Vendor, VendorAdmin)
