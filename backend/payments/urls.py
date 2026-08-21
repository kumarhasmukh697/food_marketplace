from django.urls import path
from .views import CreateRazorpayOrderView


urlpatterns = [

    path("create-order/", CreateRazorpayOrderView.as_view(), name="create-razorpay-order",),

]