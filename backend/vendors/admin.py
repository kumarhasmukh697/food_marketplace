from django.contrib import admin
from .models import VendorProfile



@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ("shop_name","user","accepting_orders","is_active","opening_time","closing_time","created_at",)
    search_fields = ("shop_name","user__username","user__email",)
    list_filter = ("accepting_orders","is_active",)
    ordering = ("shop_name",)