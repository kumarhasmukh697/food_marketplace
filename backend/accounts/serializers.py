import random
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from .models import Address, OTP

User = get_user_model()


# Serializer for user registration, OTP verification, login, profile, and address management
class RegisterSerializer(serializers.ModelSerializer):
    # this field is only used for writing data and it will not be returned in the response
    password = serializers.CharField(write_only=True, min_length=8)
   
    
    # this tell Django which model this serializer belongs to
    class Meta:
        model = User
        fields = ("username", "password", "phone_number", "role", "email")

    def validate_email(self, value):
        print("Validating email:", value)  # Debugging line to print the email being validated
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=password,
            phone_number=validated_data.get("phone_number", ""),
            role=validated_data.get("role", "customer"),
        )
      
        user.is_verified = False
        user.save(update_fields=["is_verified"])

        otp_code = f"{random.randint(100000, 999999)}"

        OTP.objects.create(user=user,otp=otp_code,purpose="registration",expires_at=timezone.now() + timedelta(minutes=10),)

        self.otp_code = otp_code
        return user



# Serializer for OTP verification
# class VerifyOTPSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField(max_length=6)

#     def validate(self, attrs):
#         user = User.objects.filter(email=attrs["email"]).first()

#         if not user:
#             raise serializers.ValidationError({"email": "User not found."})

#         otp_obj = (OTP.objects.filter(user=user,otp=attrs["otp"],purpose="registration",is_used=False,).order_by("-created_at").first())

#         if not otp_obj:
#             raise serializers.ValidationError({"otp": "Invalid OTP."})

#         if otp_obj.expires_at < timezone.now():
#             raise serializers.ValidationError({"otp": "OTP expired."})

#         attrs["user"] = user
#         attrs["otp_obj"] = otp_obj
#         return attrs



# Serializer for user login
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=False, allow_blank=False)
#     email = serializers.EmailField(required=False)
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         username = attrs.get("username")
#         email = attrs.get("email")
#         password = attrs.get("password")

#         if not username and not email:
#             raise serializers.ValidationError("Please provide username or email.")

#         user = None

#         if email:
#             user = User.objects.filter(email=email).first()

#         if not user and username:
#             user = User.objects.filter(username=username).first()

#         if not user or not user.check_password(password):
#             raise serializers.ValidationError("Invalid username/email or password.")

#         attrs["user"] = user
#         return attrs



# Serializer for user profile
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id","username","email","phone_number","role","profile_picture","is_verified","created_at","updated_at",]
#         read_only_fields = ["id", "is_verified", "created_at", "updated_at"]




# Serializer for user addresses
# class AddressSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Address
    #     fields = ["id", "full_name","phone_number","address_line_1","address_line_2","city","state","pincode","landmark","is_default",]
    #     read_only_fields = ["id"]