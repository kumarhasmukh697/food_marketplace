from django.urls import path
from .views import CheckoutView, VendorOrderDetailView, CustomerOrderDetailView, VendorOrderStatusUpdateView


urlpatterns = [

    path( "checkout/", CheckoutView.as_view(), name="checkout",),
    path("vendor/view/<int:order_id>/",VendorOrderDetailView.as_view(),name="vendor-order-detail",),
    path("customer/view/<int:order_id>/",CustomerOrderDetailView.as_view(),name="customer-order_detail,"),
    path("vendor/orders/<int:order_id>/status/", VendorOrderStatusUpdateView.as_view(), name="vendor-order-status-update",),

]