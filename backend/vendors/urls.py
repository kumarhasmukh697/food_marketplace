from django.urls import path
from vendors.views import VendorProfileView

urlpatterns = [
    path("profile/", VendorProfileView.as_view(), name="vendor-profile"),
]
