from django.urls import path
from . import page_views


urlpatterns = [
    path("", page_views.home, name='home-page'),
    path("register/", page_views.register, name='register-page'),
    path("login/", page_views.login, name='login-page'),
    path('verify-otp/', page_views.verifyotp, name='verify-otp-page'),
]