from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
   
    # Allows access only to authenticated customers.
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == "customer")
