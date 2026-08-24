from rest_framework import serializers
from .models import Order, OrderItem
from accounts.models import Address

class CheckoutSerializer(serializers.Serializer):
    delivery_address_id = serializers.IntegerField(required=False, allow_null=True,)




class VendorOrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.ImageField( source="product.image", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "product_image", "quantity", "unit_price", "subtotal", ]




class VendorOrderDetailSerializer(serializers.ModelSerializer):

    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.SerializerMethodField()
    delivery_address = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    items = VendorOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order

        fields = ["id", "customer_name", "customer_phone", "delivery_address","subtotal", 
                "delivery_fee", "tax", "discount", "total_amount", "status","payment_status",
                "created_at","items",]


   
    def get_customer_name(self, obj):
        customer = obj.customer
        return (f"{customer.first_name} {customer.last_name}").strip()


    def get_customer_phone(self, obj):
        return obj.customer.phone_number

    def get_delivery_address(self, obj):

        try:
            address = obj.customer.address
        except Address.DoesNotExist:
            return None

        return {
            "address_line_1": address.address_line_1,
            "address_line_2": address.address_line_2,
            "city": address.city,
            "state": address.state,
            "pincode": address.pincode,
        }
    
    def get_payment_status(self, obj):

        if hasattr(obj, "payment") and obj.payment:
            return obj.payment.status
        return None

