from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address
from .serializers import RegisterSerializer,VerifyOTPSerializer
#  AddressSerializer,LoginSerializer,ProfileSerializer,RegisterSerializer



class RegisterView(APIView):
    # anyone can register, so we allow any user (authenticated or not) to access this view
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully. Please verify OTP.",
                "otp": serializer.otp_code,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        otp_obj = serializer.validated_data["otp_obj"]

        user.is_verified = True
        user.save(update_fields=["is_verified"])

        otp_obj.is_used = True
        otp_obj.save(update_fields=["is_used"])

        return Response(
            {"message": "Email verified successfully."},
            status=status.HTTP_200_OK,
        )


# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data["user"]
#         refresh = RefreshToken.for_user(user)

#         return Response(
#             {
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#                 "user": {
#                     "id": user.id,
#                     "username": user.username,
#                     "email": user.email,
#                     "role": user.role,
#                     "is_verified": user.is_verified,
#                 },
#             },
#             status=status.HTTP_200_OK,
#         )


# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         return Response(
#             {"message": "Logged out successfully. Please remove the token from the client."},
#             status=status.HTTP_200_OK,
#         )


# class ProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user


# class AddressListCreateView(generics.ListCreateAPIView):
#     serializer_class = AddressSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Address.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    # serializer_class = AddressSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return Address.objects.filter(user=self.request.user)