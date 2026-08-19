from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class CartProductSerializer(serializers.ModelSerializer):

    vendor_name = serializers.CharField(source="vendor.shop_name", read_only=True,)

    class Meta:
        model = Product

        fields = [ "id", "name", "description", "price", "image", "is_available", "stock", "vendor_name",]




class CartItemSerializer(serializers.ModelSerializer):

    product = CartProductSerializer( read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem

        fields = [ "id", "product", "price", "quantity", "subtotal",]

    def get_subtotal(self, obj):
        return obj.subtotal

    




class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer( many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    vendor_name = serializers.CharField( source="vendor.shop_name", read_only=True,)


    class Meta:
        model = Cart

        fields = [ "id", "vendor", "vendor_name", "items", "total_items", "subtotal", "created_at", "updated_at",]
        read_only_fields = [ "id", "vendor", "vendor_name", "items", "total_items", "subtotal", "created_at", "updated_at", ]

    def get_subtotal(self, obj):
        return obj.subtotal

    def get_total_items(self, obj):
        return sum( item.quantity for item in obj.items.all() )





class AddToCartSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField( min_value=1, default=1,)



    def validate_product_id(self, value):
        try:
            product = Product.objects.select_related( "vendor").get( id=value )

        except Product.DoesNotExist:

            raise serializers.ValidationError( "Product does not exist.")

        if not product.is_available:
            raise serializers.ValidationError("This product is currently unavailable.")

        if product.stock <= 0:
            raise serializers.ValidationError( "This product is out of stock." )

        self.product = product
        return value



    def validate(self, attrs):

        product = self.product
        quantity = attrs["quantity"]

        if quantity > product.stock:

            raise serializers.ValidationError({
                "quantity": (
                    f"Only {product.stock} units "
                    f"are available."
                )
            })

        return attrs




class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField( min_value=1)