from rest_framework.permissions import BasePermission, SAFE_METHODS


# class ProductPermission(BasePermission):
#     """
#     Customers and Delivery:
#         Only GET, HEAD, OPTIONS

#     Vendors:
#         GET, POST, PUT, PATCH, DELETE (own products only)

#     Admin:
#         Everything
#     """

#     def has_permission(self, request, view):

#         # Allow read requests for everyone
#         # this SAFE_METHODS constant is a tuple that includes the HTTP methods that are considered "safe" (i.e., they do not modify resources). In this case, it includes GET, HEAD, and OPTIONS. If the request method is one of these, the permission check passes and returns True.
#         if request.method in SAFE_METHODS:
#             return True

#         # User must be logged in
#         # if user is not authenticated, the permission check fails and return the fals
#         if not request.user.is_authenticated:
#             return False

#         # Admin can do everything
#         if request.user.role == "admin":
#             return True

#         # Vendor can create/update/delete
#         return request.user.role == "vendor"
    

    
#     def has_object_permission(self, request, view, obj):

#         # Allow read requests for everyone
#         if request.method in SAFE_METHODS:
#             return True

#         if not request.user.is_authenticated:
#             return False

#         if request.user.role == "admin":
#             return True

#         if request.user.role == "vendor" and hasattr(request.user, "vendor_profile"):
#             return obj.vendor == request.user.vendor_profile

#         return False