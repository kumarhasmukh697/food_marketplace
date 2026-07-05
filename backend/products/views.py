from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from products.models import Product
# from products.serializers import ProductSerializer
# from .permissions import ProductPermission


 

# class ProductListCreateView(generics.ListCreateAPIView):
#     # This view handles the collection endpoint:
#     #   GET  /api/products/  -> list all products
#     #   POST /api/products/  -> create a new product
#     # this below queryset is used to optimize the database queries by fetching related vendor and category objects in a single query, which can improve performance when listing products.
#     queryset = Product.objects.select_related("vendor", "category").all()
#     serializer_class = ProductSerializer
#     permission_classes = [ProductPermission]

#     def perform_create(self, serializer):
#         user = self.request.user
#         # vendor users: auto-assign their vendor profile
#         if getattr(user, "role", None) == "vendor":
#             if not hasattr(user, "vendor_profile"):
#                 raise PermissionDenied("Vendor profile not found.")
#             serializer.save(vendor=user.vendor_profile)
#         else:
#             # admins may pass `vendor` id in the request body; serializer will handle it
#             serializer.save()


# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
#     # This view handles a single product endpoint:
#     #   GET    /api/products/<id>/  -> get one product
#     #   PUT    /api/products/<id>/  -> update a product
#     #   PATCH  /api/products/<id>/  -> partially update a product
#     #   DELETE /api/products/<id>/  -> delete a product
#     queryset = Product.objects.select_related("vendor","category").all()
#     serializer_class = ProductSerializer
#     permission_classes = [ProductPermission]
#     lookup_field = "id"