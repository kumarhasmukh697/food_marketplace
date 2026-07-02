from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address
from .serializers import RegisterSerializer,VerifyOTPSerializer,LoginSerializer , ProfileSerializer ,AddressSerializer




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



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        # This line checks if the data provided by the user is valid according to the rules defined in the LoginSerializer. If the data is not valid, it will raise an exception and return a 400 Bad Request response with details about what went wrong.
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data is a dictionary that contains the validated data from the serializer. In this case, it contains the user object that was authenticated based on the provided credentials (email and password). We are extracting the user object from this dictionary to use it for generating JWT tokens.
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "is_verified": user.is_verified,
                },
            },
            status=status.HTTP_200_OK,
        )




class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token is required."},status=status.HTTP_400_BAD_REQUEST,)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid or already blacklisted refresh token."},status=status.HTTP_400_BAD_REQUEST,)

        return Response(
            {"message": "Logged out successfully."},status=status.HTTP_200_OK)





class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user




# this below class is for listing and creating addresses for the authenticated user
class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




# this below class is for retrieving, updating and deleting a specific address for the authenticated user
class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)