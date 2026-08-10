from rest_framework.permissions import BasePermission

class IsDelivery(BasePermission):
   
    # Allows access only to authenticated delivery partners.
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == "delivery")
