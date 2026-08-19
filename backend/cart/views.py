from django.db import transaction
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from customer.permissions import IsCustomer
# from products.models import Product
from .models import Cart, CartItem
from .serializers import ( CartSerializer, AddToCartSerializer, UpdateCartItemSerializer,)




class CartView(APIView):
    permission_classes = [IsCustomer]
   
    def get(self, request):

        try:
            cart = Cart.objects.prefetch_related( "items__product").select_related("vendor").get( customer=request.user)

        except Cart.DoesNotExist:

            return Response(
                { "id": None, "vendor": None, "vendor_name": None, "items": [], "total_items": 0, "subtotal": 0,},
                status=status.HTTP_200_OK
            )

        serializer = CartSerializer(cart)

        return Response( serializer.data, status=status.HTTP_200_OK )





class AddToCartView(APIView):

    permission_classes = [ IsCustomer]

    @transaction.atomic
    def post(self, request):

        serializer = AddToCartSerializer( data=request.data)
        serializer.is_valid( raise_exception=True)
        product = serializer.product
        quantity = serializer.validated_data["quantity"]
        customer = request.user

        # ------------------------------------------------
        # Check whether customer already has a cart
        # ------------------------------------------------

        try:
            cart = Cart.objects.select_related("vendor").get( customer=customer)

        except Cart.DoesNotExist:
            cart = Cart.objects.create(customer=customer,vendor=product.vendor)

        # ------------------------------------------------
        # Make sure product belongs to same vendor
        # ------------------------------------------------

        if cart.vendor_id != product.vendor_id:

            return Response(
                {
                    "detail": (
                        "Your cart contains products from "
                        f"{cart.vendor.shop_name}. "
                        "Clear your cart before adding "
                        "products from another vendor."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ------------------------------------------------
        # Check existing cart item
        # ------------------------------------------------

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"price": product.price, "quantity": quantity,}
        )

        if not created:
            new_quantity = (cart_item.quantity + quantity)

            if new_quantity > product.stock:
                return Response(
                    {
                        "detail": (
                            f"Only {product.stock} "
                            "units are available."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = new_quantity
            cart_item.price = product.price
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(
            {
                "message": "Product added to cart.",
                "cart": serializer.data,
            },
            status=status.HTTP_200_OK
        )





class CartItemUpdateView(APIView):

    permission_classes = [ IsCustomer]

    def patch(self, request, item_id):

        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.select_related("cart","product").get(
                id=item_id,
                cart__customer=request.user
            )

        except CartItem.DoesNotExist:

            return Response(
                {
                    "detail": "Cart item not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        product = cart_item.product
        if not product.is_available:

            return Response(
                {
                    "detail": (
                        "This product is no longer "
                        "available."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > product.stock:

            return Response(
                {
                    "detail": (
                        f"Only {product.stock} "
                        "units are available."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.price = product.price
        cart_item.save()
        cart = cart_item.cart

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )





class CartItemDeleteView(APIView):

    permission_classes = [ IsCustomer]

    def delete(self, request, item_id):

        try:

            cart_item = CartItem.objects.get(id=item_id, cart__customer=request.user)

        except CartItem.DoesNotExist:

            return Response(
                {
                    "detail": "Cart item not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        cart = cart_item.cart

        cart_item.delete()

        # -----------------------------------------------
        # If no items remain, delete the cart itself.
        # -----------------------------------------------

        if not cart.items.exists():

            cart.delete()

            return Response(
                {
                    "message": "Item removed from cart.",
                    "cart": None,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": "Item removed from cart.",
                "cart": CartSerializer(cart).data,
            },
            status=status.HTTP_200_OK
        )






class ClearCartView(APIView):

    permission_classes = [
        IsCustomer
    ]

    def delete(self, request):

        try:

            cart = Cart.objects.get(
                customer=request.user
            )

        except Cart.DoesNotExist:

            return Response(
                {
                    "message": "Cart is already empty."
                },
                status=status.HTTP_200_OK
            )

        cart.delete()

        return Response(
            {
                "message": "Cart cleared successfully."
            },
            status=status.HTTP_200_OK
        )