from rest_framework import serializers


class CheckoutSerializer(serializers.Serializer):

    delivery_address_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )