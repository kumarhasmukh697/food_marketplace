from django.db import models
from django.conf import settings

# Create your models here.
User =  settings.AUTH_USER_MODEL



class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart",)
    # A cart belongs to one vendor at a time.
    vendor = models.ForeignKey("vendors.VendorProfile", on_delete=models.CASCADE, related_name="carts",null=True,blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )

    def __str__(self):
        return f"{self.customer.username}'s cart"

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items",)
    product = models.ForeignKey( "products.Product", on_delete=models.CASCADE, related_name="cart_items", )
    # Store the price at the time the product was added.
    price = models.DecimalField( max_digits=10, decimal_places=2,)
    quantity = models.PositiveIntegerField(default=1,)
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_in_cart",
            )
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity
    