

from django.urls import path

from .views import DeliveryPartnerProfileView

urlpatterns = [

    path(
        "profile/",
        DeliveryPartnerProfileView.as_view(),
        name="delivery-profile",
    ),

]