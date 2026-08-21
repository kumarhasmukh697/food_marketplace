from django.db import transaction
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from .models import Payment
from .serializers import CreateRazorpayOrderSerializer
from .razorpay_service import RazorpayService




class CreateRazorpayOrderView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        # -----------------------------------------
        # Validate request
        # -----------------------------------------

        serializer = (CreateRazorpayOrderSerializer( data=request.data ))
        serializer.is_valid(raise_exception=True )
        order_id = ( serializer.validated_data["order_id"] )

        # -----------------------------------------
        # Get customer's order
        # -----------------------------------------

        try:

            order = (
                Order.objects.select_related( "customer", "vendor",)
                .get(
                    id=order_id,
                    customer=request.user,
                )
            )

        except Order.DoesNotExist:
            return Response(
                { "detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # -----------------------------------------
        # Check order status
        # -----------------------------------------

        if order.status != "pending_payment":

            return Response(
                {
                    "detail": (
                        "This order is not "
                        "pending payment."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------------------
        # Get Payment
        # -----------------------------------------

        try:
            payment = order.payment

        except Payment.DoesNotExist:
            return Response(
                {
                    "detail": (
                        "Payment record "
                        "does not exist."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------------------
        # Prevent duplicate Razorpay orders
        # -----------------------------------------

        if payment.razorpay_order_id:

            return Response(
                {
                    "message": (
                        "Razorpay order already exists."
                    ),

                    "order_id": order.id,

                    "razorpay_order_id":
                        payment.razorpay_order_id,

                    "amount":
                        str(payment.amount),

                    "amount_in_paise":
                        int(payment.amount * 100),

                    "currency":
                        payment.currency,

                    "key_id":
                        settings.RAZORPAY_KEY_ID,
                },
                status=status.HTTP_200_OK,
            )

        # -----------------------------------------
        # Create Razorpay Order
        # -----------------------------------------

        razorpay_service = ( RazorpayService())

        try:
            razorpay_order = (
                razorpay_service.create_order(
                    amount=payment.amount,
                    currency=payment.currency,
                    receipt=f"order_{order.id}",
                )
            )

        except Exception as error:
            return Response(
                {
                    "detail": (
                        "Unable to create "
                        "Razorpay order."
                    ),

                    "error": str(error),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # -----------------------------------------
        # Save Razorpay Order ID
        # -----------------------------------------

        payment.razorpay_order_id = (
            razorpay_order["id"]
        )

        payment.status = "pending"

        payment.save(
            update_fields=[
                "razorpay_order_id",
                "status",
                "updated_at",
            ]
        )

        # -----------------------------------------
        # Return data to frontend
        # -----------------------------------------

        return Response(

            {
                "message": (
                    "Razorpay order created successfully."
                ),

                "order_id": order.id,

                "razorpay_order_id":
                    razorpay_order["id"],

                "amount":
                    str(payment.amount),

                "amount_in_paise":
                    razorpay_order["amount"],

                "currency":
                    razorpay_order["currency"],

                "key_id":
                    settings.RAZORPAY_KEY_ID,

            },

            status=status.HTTP_201_CREATED,
        )