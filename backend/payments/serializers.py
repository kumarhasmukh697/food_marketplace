from rest_framework import serializers


class CreateRazorpayOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()