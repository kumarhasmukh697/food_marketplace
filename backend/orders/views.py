from decimal import Decimal
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from payments.models import Payment
from delivery.models import DeliveryPartnerProfile
from .models import Order, OrderItem
from .serializers import CheckoutSerializer, VendorOrderDetailSerializer, VendorOrderStatusSerializer
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


class CustomerOrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):

        customer = request.user

        order = get_object_or_404(
            Order.objects.select_related(
                "customer",
                "vendor",
                "customer__address"
            ).prefetch_related(
                "items__product"
            ),
            id=order_id,
            customer=customer,
        )

        serializer = VendorOrderDetailSerializer(order)

        return Response(serializer.data)




class VendorOrderStatusUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, order_id):

        # -----------------------------------------
        # Get logged-in vendor
        # -----------------------------------------

        vendor = request.user.vendor_profile

        # -----------------------------------------
        # Get order belonging to this vendor
        # -----------------------------------------

        order = get_object_or_404(
            Order.objects.select_for_update(),
            id=order_id,
            vendor=vendor,
        )

        # -----------------------------------------
        # Validate requested status
        # -----------------------------------------

        serializer = VendorOrderStatusSerializer( order, data=request.data, partial=True)
        serializer.is_valid( raise_exception=True)
        new_status = serializer.validated_data["status"]

        # -----------------------------------------
        # Check valid status transition
        # -----------------------------------------

        current_status = order.status
        if current_status == "confirmed":
            if new_status != "preparing":
                return Response(
                    {"detail":"Confirmed order can only be changed to preparing."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        elif current_status == "preparing":
            if new_status != "ready":
                return Response(
                    { "detail": "Preparing order can only be changed to ready."},
                    status=status.HTTP_400_BAD_REQUEST,
                )


        elif current_status == "ready":
            return Response(
                {"detail": "Order is already ready."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        else:
            return Response(
                {"detail": f"Vendor cannot change order from {current_status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        # -----------------------------------------
        # Update status
        # -----------------------------------------

        order.status = new_status
        order.save( update_fields=["status", "updated_at"])


        # -----------------------------------------
        # If READY → assign delivery partner
        # -----------------------------------------

        delivery_partner = None
        if new_status == "ready":
            delivery_partner = (DeliveryPartnerProfile.objects.select_for_update()
                .filter(is_online=True, is_available=True,)
                .order_by("updated_at")
                .first()
            )

            if delivery_partner:
                order.delivery_partner = ( delivery_partner)
                order.save( update_fields=["delivery_partner","updated_at"])

                delivery_partner.is_available = False
                delivery_partner.save( update_fields=[ "is_available","updated_at",])


        # -----------------------------------------
        # Response
        # -----------------------------------------

        return Response(
            {
                "message": "Order status updated successfully.",
                "order_id": order.id,
                "status": order.status,
                "delivery_partner": ( delivery_partner.user.username if delivery_partner else None),
            },
            status=status.HTTP_200_OK,
        )