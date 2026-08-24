from rest_framework import serializers


class CreateRazorpayOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()





class VerifyPaymentSerializer(serializers.Serializer):

    razorpay_order_id = serializers.CharField( max_length=100)
    razorpay_payment_id = serializers.CharField( max_length=100)
    razorpay_signature = serializers.CharField( max_length=255)