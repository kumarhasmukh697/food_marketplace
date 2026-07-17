from rest_framework import serializers
from .models import VendorProfile



class VendorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProfile

        fields = ["shop_name","description","address","opening_time","closing_time","accepting_orders","is_active",]
        read_only_fields = ["is_active",]



# this nested serializer will be used in product serializer so that we do not have to expose all the fields to the frontend
class VendorNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProfile
        fields = ["id","shop_name",]