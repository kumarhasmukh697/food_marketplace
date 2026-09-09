from django.urls import include, path
from . views import CustomerProfileView, CustomerLocationUpdateView



urlpatterns = [
    path("profile/", CustomerProfileView.as_view(), name="customer-profile"),
    path("profile/location/", CustomerLocationUpdateView.as_view(), name="customer-location-update"),
]