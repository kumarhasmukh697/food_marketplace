from django.contrib import admin
from .models import User, Address, OTP


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'role', 'is_verified', 'is_active', 'is_staff')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at','password',)
    ordering = ('username',)


admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(OTP)