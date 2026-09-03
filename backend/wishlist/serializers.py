from rest_framework import serializers
from .models import FavoriteRestaurant



class FavoriteRestaurantSerializer(serializers.ModelSerializer):

    vendor_id = serializers.IntegerField(source="vendor.id")
    shop_name = serializers.CharField(source="vendor.shop_name")
    slug = serializers.CharField(source="vendor.slug")
    address = serializers.CharField(source="vendor.address.address_line_1")

    class Meta:
        model = FavoriteRestaurant
        fields = ["vendor_id", "shop_name", "slug", "address", "created_at",]