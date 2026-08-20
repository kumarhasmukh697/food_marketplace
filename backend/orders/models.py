from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Order(models.Model):

    ORDER_STATUS_CHOICES = [
        ("pending_payment", "Pending Payment"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("ready", "Ready for Pickup"),
        ("picked_up", "Picked Up"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey( User, on_delete=models.PROTECT,related_name="orders",)
    vendor = models.ForeignKey( "vendors.VendorProfile", on_delete=models.PROTECT, related_name="orders", )
    status = models.CharField( max_length=30, choices=ORDER_STATUS_CHOICES, default="pending_payment",)
    subtotal = models.DecimalField( max_digits=10, decimal_places=2,)
    delivery_fee = models.DecimalField( max_digits=10, decimal_places=2, default=0,)
    tax = models.DecimalField( max_digits=10, decimal_places=2, default=0,)
    discount = models.DecimalField( max_digits=10, decimal_places=2, default=0,)
    total_amount = models.DecimalField( max_digits=10, decimal_places=2,)
    created_at = models.DateTimeField( auto_now_add=True,)
    updated_at = models.DateTimeField( auto_now=True,)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"






class OrderItem(models.Model):

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="items",)
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT,related_name="order_items",)
    # Snapshot of the product name at the time of purchase
    product_name = models.CharField( max_length=255,)
    # Price of one unit at the time of purchase
    unit_price = models.DecimalField( max_digits=10, decimal_places=2,)
    quantity = models.PositiveIntegerField()
    # unit_price × quantity
    subtotal = models.DecimalField( max_digits=10, decimal_places=2,)
    created_at = models.DateTimeField( auto_now_add=True,)

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"