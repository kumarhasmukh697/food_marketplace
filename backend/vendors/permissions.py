from rest_framework.permissions import BasePermission


class IsVendor(BasePermission):
    # Allows access only to authenticated vendors.
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == "vendor")


