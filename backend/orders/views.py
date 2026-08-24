from decimal import Decimal
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from payments.models import Payment
from .models import Order, OrderItem
from .serializers import CheckoutSerializer, VendorOrderDetailSerializer
from django.shortcuts import get_object_or_404







class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        # -----------------------------------------
        # Validate request
        # -----------------------------------------

        serializer = CheckoutSerializer( data=request.data)
        serializer.is_valid( raise_exception=True)

        # -----------------------------------------
        # Get customer's cart
        # -----------------------------------------

        try:

            cart = (Cart.objects.select_related("customer","vendor",).prefetch_related("items__product").get(customer=request.user))
            print(cart)

        except Cart.DoesNotExist:

            return Response({ "detail": "Cart does not exist."},status=status.HTTP_400_BAD_REQUEST,)

        # -----------------------------------------
        # Check cart has items
        # -----------------------------------------

        cart_items = list(cart.items.all())

        if not cart_items:
            return Response({ "detail": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------------------
        # Validate products
        # -----------------------------------------

        for cart_item in cart_items:
            product = cart_item.product
            if not product.is_available:
                return Response({ "detail": ( f"{product.name} " "is currently unavailable.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if cart_item.quantity > product.stock:
                return Response(
                    {"detail": ( f"Only {product.stock} " f"units of {product.name} " "are available.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # -----------------------------------------
        # Calculate subtotal
        # -----------------------------------------

        subtotal = Decimal("0.00")
        for cart_item in cart_items:
            product = cart_item.product
            subtotal += ( product.price * cart_item.quantity)


        # -----------------------------------------
        # Delivery fee
        # -----------------------------------------

        delivery_fee = Decimal("40.00")

        # -----------------------------------------
        # Tax
        # -----------------------------------------

        tax = ( subtotal * Decimal("0.05") )

        # Round tax to 2 decimal places
        tax = tax.quantize( Decimal("0.01"))

        # -----------------------------------------
        # Discount
        # -----------------------------------------

        discount = Decimal("0.00")

        # -----------------------------------------
        # Final amount
        # -----------------------------------------

        total_amount = ( subtotal + delivery_fee + tax - discount)


        # -----------------------------------------
        # Create Order
        # -----------------------------------------

        order = Order.objects.create(
            customer=request.user,
            vendor=cart.vendor,
            status="pending_payment",
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            tax=tax,
            discount=discount,
            total_amount=total_amount,
        )

        # -----------------------------------------
        # Create OrderItems
        # -----------------------------------------

        order_items = []

        for cart_item in cart_items:
            product = cart_item.product
            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    product_name=product.name,
                    unit_price=product.price,
                    quantity=cart_item.quantity,
                    subtotal=( product.price * cart_item.quantity),
                )
            )

        OrderItem.objects.bulk_create( order_items)


        # -----------------------------------------
        # Create Payment
        # -----------------------------------------

        payment = Payment.objects.create(
            order=order,
            amount=total_amount,
            currency="INR",
            status="created",
        )

        # -----------------------------------------
        # Return checkout information
        # -----------------------------------------

        return Response(
            {
                "message": (
                    "Checkout created successfully."
                ),

                "order": {
                    "id": order.id,
                    "vendor": order.vendor.shop_name,
                    "subtotal": str( order.subtotal),
                    "delivery_fee": str( order.delivery_fee),
                    "tax": str( order.tax),
                    "discount": str(order.discount),
                    "total_amount": str( order.total_amount),
                    "status": order.status,
                },

                "payment": {
                    "id": payment.id,
                    "amount": str( payment.amount),
                    "currency": payment.currency,
                    "status": payment.status,
                },
            },
            status=status.HTTP_201_CREATED,
        )




class VendorOrderDetailView(APIView):

    permission_classes = [IsAuthenticated]
    print("we are inside view")

    def get(self, request, order_id):

        vendor = request.user.vendor_profile

        order = get_object_or_404(

            Order.objects.select_related("customer","vendor","customer__address")
            .prefetch_related("items__product"),

            id=order_id,
            vendor=vendor,
        )

        serializer = VendorOrderDetailSerializer(order)
        return Response(serializer.data)