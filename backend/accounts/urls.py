from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView , LogoutView

# AddressDetailView, AddressListCreateView, ProfileView
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("profile/", ProfileView.as_view(), name="profile"),
    # path("address/", AddressListCreateView.as_view(), name="address-list"),
    # path("address/<int:pk>/", AddressDetailView.as_view(), name="address-detail"),
]