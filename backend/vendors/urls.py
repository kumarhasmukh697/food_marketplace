from django.urls import path
from .views import VendorProfileView, VendorLocationUpdateView


urlpatterns = [
    path("profile/", VendorProfileView.as_view(), name="vendor-profile"),
    path("profile/location/", VendorLocationUpdateView.as_view(), name="vendor-location-update"),
]
