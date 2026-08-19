from django.urls import path
from .views import (CartView, AddToCartView, CartItemUpdateView, CartItemDeleteView, ClearCartView,)



urlpatterns = [

    # View current cart
    path( "", CartView.as_view(), name="cart",),
    # Add product
    path( "add/", AddToCartView.as_view(), name="cart-add",),
    # Update quantity
    path("items/<int:item_id>/", CartItemUpdateView.as_view(), name="cart-item-update",),
    # Remove item
    path("items/<int:item_id>/remove/", CartItemDeleteView.as_view(), name="cart-item-delete",),
    # Clear cart
    path("clear/", ClearCartView.as_view(), name="cart-clear",),

]
