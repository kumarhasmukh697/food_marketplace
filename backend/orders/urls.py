from django.urls import path
from .views import CheckoutView, VendorOrderDetailView


urlpatterns = [

    path( "checkout/", CheckoutView.as_view(), name="checkout",),
    path("vendor/view/<int:order_id>/",VendorOrderDetailView.as_view(),name="vendor-order-detail",),

]