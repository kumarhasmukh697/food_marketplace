from django.urls import include, path
from . views import CustomerProfileView, CustomerLocationUpdateView, CustomerOrderTrackingView



urlpatterns = [
    path("profile/", CustomerProfileView.as_view(), name="customer-profile"),
    path("profile/location/", CustomerLocationUpdateView.as_view(), name="customer-location-update"),
    path("orders/<int:order_id>/tracking/", CustomerOrderTrackingView.as_view(), name="customer-order-tracking"),
]