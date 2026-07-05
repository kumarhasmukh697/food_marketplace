from rest_framework import serializers
from products.models import Product
from categories.models import Category
from vendors.models import Vendor


# class ProductSerializer(serializers.ModelSerializer):
#     # read-only helper fields for output
#     vendor_shop_name = serializers.SerializerMethodField()
#     category_name = serializers.SerializerMethodField()

#     # writable relationship fields
#     # - `vendor` is optional for input (admins can set it). Vendor users will be auto-assigned in the view.
#     vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(), required=False)
#     # `category` must be provided for product creation
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)

#     class Meta:
#         model = Product
#         fields = [ "id", "name", "description", "price", "image", "is_available", "vendor","category","vendor_shop_name","category_name", ]

#     def get_vendor_shop_name(self, obj):
#         return obj.vendor.shop_name if obj.vendor else None

#     def get_category_name(self, obj):
#         return obj.category.name if obj.category else None