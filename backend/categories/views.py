from django.shortcuts import render
from rest_framework import generics
from categories.models import Category
from categories.serializers import CategorySerializer


# this veiw handles the GET and POST requests for the Category model
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
