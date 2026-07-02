from rest_framework import serializers
from categories.models import Category


# this serializer is used to convert the Category model into JSON format and vice versa
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "image"]