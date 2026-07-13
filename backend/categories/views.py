from django.shortcuts import render
from rest_framework import generics
from categories.models import Category
from categories.serializers import CategorySerializer
from categories.permissions import CategoryPermission


# this veiw handles the GET and POST requests for the Category model
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]


# this view handles PUT,PATCH,DELETE request for the cateogry model only admi
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]
