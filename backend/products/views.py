from django.shortcuts import render
from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer





class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("vendor", "category").all()
    serializer_class = ProductSerializer