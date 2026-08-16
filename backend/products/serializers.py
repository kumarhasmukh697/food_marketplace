from rest_framework import serializers
from products.models import Product
from categories.serializers import CategoryNestedSerializer
from vendors.serializers import VendorNestedSerializer


class ProductListSerializer(serializers.ModelSerializer):

    vendor = VendorNestedSerializer(read_only=True)
    category = CategoryNestedSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"



class ProductCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id","category","name","description","price","image","stock","is_available","is_veg"]