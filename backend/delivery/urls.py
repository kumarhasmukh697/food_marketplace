from django.urls import path
from .views import DeliveryPartnerProfileView
from .views import DeliveryOnlineStatusView, DeliveryLocationUpdateView, DeliveryOrderStatusUpdateView



urlpatterns = [

    path("profile/", DeliveryPartnerProfileView.as_view(), name="delivery-profile",),
    path("profile/status/", DeliveryOnlineStatusView.as_view(), name="delivery-online-status",),
    path("profile/location/",DeliveryLocationUpdateView.as_view(), name="delivery-location-update",),
    path("orders/<int:order_id>/status/", DeliveryOrderStatusUpdateView.as_view(), name="delivery-order-status",),
  
    
]





