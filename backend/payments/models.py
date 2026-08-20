from django.db import models


class Payment(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ("created", "Created"),
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    order = models.OneToOneField( "orders.Order", on_delete=models.PROTECT, related_name="payment",)
    # Razorpay Order ID
    razorpay_order_id = models.CharField( max_length=100, unique=True, null=True, blank=True,)
    # Razorpay Payment ID
    razorpay_payment_id = models.CharField( max_length=100, unique=True, null=True, blank=True,)
    # Used to verify that the payment response
    # actually came from Razorpay.
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True,)
    amount = models.DecimalField( max_digits=10, decimal_places=2,)
    currency = models.CharField( max_length=10, default="INR",)
    status = models.CharField( max_length=20, choices=PAYMENT_STATUS_CHOICES, default="created",)
    created_at = models.DateTimeField( auto_now_add=True, )
    updated_at = models.DateTimeField( auto_now=True,)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"