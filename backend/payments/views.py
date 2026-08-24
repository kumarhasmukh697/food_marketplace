from django.db import transaction
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from products.models import Product
from .models import Payment
from .serializers import CreateRazorpayOrderSerializer, VerifyPaymentSerializer
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
                .get(id=order_id, customer=request.user,)
            )

        except Order.DoesNotExist:
            return Response({ "detail": "Order not found."},status=status.HTTP_404_NOT_FOUND,)

        # -----------------------------------------
        # Check order status
        # -----------------------------------------

        if order.status != "pending_payment":
            return Response({"detail": "This order is not pending payment."}, status=status.HTTP_400_BAD_REQUEST)

        # -----------------------------------------
        # Get Payment
        # -----------------------------------------

        try:
            payment = order.payment

        except Payment.DoesNotExist:
            return Response({ "detail": "Payment record does not exist."},status=status.HTTP_400_BAD_REQUEST,)

        # -----------------------------------------
        # Prevent duplicate Razorpay orders
        # -----------------------------------------

        if payment.razorpay_order_id:
            return Response(
                {
                    "message": "Razorpay order already exists.",
                    "order_id": order.id,
                    "razorpay_order_id": payment.razorpay_order_id,
                    "amount": str(payment.amount),
                    "amount_in_paise": int(payment.amount * 100),
                    "currency": payment.currency,
                    "key_id": settings.RAZORPAY_KEY_ID,
                },
                status=status.HTTP_200_OK,
            )

        # -----------------------------------------
        # Create Razorpay Order
        # -----------------------------------------

        razorpay_service =  (RazorpayService())

        try:
            razorpay_order = (
                razorpay_service.create_order(
                    amount=payment.amount,
                    currency=payment.currency,
                    receipt=f"order_{order.id}",
                )
            )

        except Exception as error:
            return Response({"detail": "Unable to create Razorpay order.", "error": str(error)},status=status.HTTP_502_BAD_GATEWAY,)

        # -----------------------------------------
        # Save Razorpay Order ID
        # -----------------------------------------

        payment.razorpay_order_id = (razorpay_order["id"] )
        payment.status = "pending"
        payment.save( update_fields=["razorpay_order_id","status","updated_at",] )

        # -----------------------------------------
        # Return data to frontend
        # -----------------------------------------

        return Response(
            {
                "message": "Razorpay order created successfully.",
                "order_id": order.id,
                "razorpay_order_id": razorpay_order["id"],
                "amount": str(payment.amount),
                "amount_in_paise": razorpay_order["amount"],
                "currency": razorpay_order["currency"],
                "key_id": settings.RAZORPAY_KEY_ID,

            },
            status=status.HTTP_201_CREATED,
        )





class VerifyPaymentView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        # -----------------------------------------
        # Validate request
        # -----------------------------------------

        serializer = VerifyPaymentSerializer( data=request.data)
        serializer.is_valid( raise_exception=True)
        razorpay_order_id = ( serializer.validated_data["razorpay_order_id"])
        razorpay_payment_id = ( serializer.validated_data["razorpay_payment_id" ])
        razorpay_signature = (serializer.validated_data[ "razorpay_signature"])

        # -----------------------------------------
        # Find Payment
        # -----------------------------------------

        try:
            payment = (
                Payment.objects.select_related( "order", "order__customer")
                .get( razorpay_order_id= razorpay_order_id)
            )

        except Payment.DoesNotExist:
            return Response( { "detail": "Payment record not found."},status=status.HTTP_404_NOT_FOUND,)


        # -----------------------------------------
        # Verify ownership
        # -----------------------------------------

        if ( payment.order.customer_id!= request.user.id):
            return Response({"detail": "You are not allowed to verify this payment."},status=status.HTTP_403_FORBIDDEN)

        # -----------------------------------------
        # Already paid?
        # -----------------------------------------

        if payment.status == "paid":
            return Response(
                {
                    "message":"Payment is already verified.",
                    "order_id": payment.order.id,
                    "payment_status": payment.status,
                    "order_status": payment.order.status,
                },
                status=status.HTTP_200_OK,
            )

        # -----------------------------------------
        # Verify Razorpay signature
        # -----------------------------------------

        razorpay_service = RazorpayService()

        try:
            razorpay_service.verify_payment_signature(
                razorpay_order_id= razorpay_order_id,
                razorpay_payment_id= razorpay_payment_id,
                razorpay_signature= razorpay_signature,
            )

        except Exception:
            payment.status = "failed"
            payment.save(update_fields=[ "status", "updated_at"] )
            return Response({"detail": "Payment verification failed."}, status=status.HTTP_400_BAD_REQUEST,)


        # =================================================
        # PAYMENT IS VALID
        # =================================================

        order = payment.order

        # -----------------------------------------
        # Get OrderItems
        # -----------------------------------------

        order_items = (order.items.select_related("product") .select_for_update())

        # -----------------------------------------
        # Check stock first
        # -----------------------------------------

        for item in order_items:
            product = Product.objects.select_for_update().get(id=item.product_id)
            product = item.product
            if product.stock < item.quantity:

                # Payment has technically succeeded,
                # but we cannot fulfill the order.

                return Response({"detail": f"Insufficient stock for {product.name}."}, status=status.HTTP_400_BAD_REQUEST)

        # -----------------------------------------
        # Reduce stock
        # -----------------------------------------

        for item in order_items:
            product = item.product
            product.stock -= item.quantity
            product.save( update_fields=["stock","updated_at"])

        # -----------------------------------------
        # Mark Payment as PAID
        # -----------------------------------------

        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature =  razorpay_signature
        payment.status = "paid"
        payment.save(update_fields=["razorpay_payment_id","razorpay_signature","status","updated_at"])

        # -----------------------------------------
        # Mark Order as CONFIRMED
        # -----------------------------------------

        order.status = "confirmed"
        order.save(update_fields=["status", "updated_at"])

        # -----------------------------------------
        # Clear Cart
        # -----------------------------------------

        cart = getattr(request.user, "cart", None)

        if cart:
            cart.items.all().delete()
            # If you want to completely remove
            # the cart itself:
            cart.delete()

        # -----------------------------------------
        # Success
        # -----------------------------------------

        return Response(
            {
                "message": "Payment verified and order confirmed.",
                "order_id": order.id,
                "payment_id": payment.razorpay_payment_id,
                "payment_status": payment.status,
                "order_status": order.status,
                "message_stock": "Product stock updated successfully.",
                "message_cart": "Cart cleared successfully.",
            },
            status=status.HTTP_200_OK,
        )

