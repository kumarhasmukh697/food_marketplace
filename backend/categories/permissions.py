from rest_framework.permissions import BasePermission, SAFE_METHODS # SAFE_METHODS CONTAINS GET,HEAD,OPTIONS



class CategoryPermission(BasePermission):

    def has_permission(self, request, view):

        # Everyone can view categories
        if request.method in SAFE_METHODS:
            return True

        # Must be logged in
        if not request.user.is_authenticated:
            return False
        
        # if user is authenticated then previous if condition will not execute and controls comes here and check for the user role and based on that return true
        # Only admin can modify categories
        return request.user.role == "admin"