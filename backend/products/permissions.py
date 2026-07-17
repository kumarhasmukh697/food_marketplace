from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProductPermission(BasePermission):

    def has_permission(self, request, view):

        # Everyone can view products
        if request.method in SAFE_METHODS:
            return True

        # Must be authenticated
        if not request.user.is_authenticated:
            return False

        # Only vendors can create/update/delete
        return request.user.role == "vendor"

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        # Vendor can modify only their own products
        return obj.vendor.user == request.user