from rest_framework import serializers
from .models import VendorProfile
from accounts.models import Address, User
from vendors.models import VendorProfile




class VendorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProfile

        fields = ["shop_name", "address", "opening_time", "closing_time", "accepting_orders", "is_active"]
        read_only_fields = ["is_active",]



# this nested serializer will be used in product serializer so that we do not have to expose all the fields to the frontend
class VendorNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProfile
        fields = ["id","shop_name",]




class VendorProfileSerializer1(serializers.ModelSerializer):

    # ==============================
    # User Fields
    # ==============================

    first_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    last_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    phone_number = serializers.CharField(
        required=False,
        allow_blank=True
    )

    profile_picture = serializers.ImageField(
        required=False,
        allow_null=True
    )

    # ==============================
    # Address Fields
    # ==============================

    address_line_1 = serializers.CharField(
        required=False,
        allow_blank=True
    )

    address_line_2 = serializers.CharField(
        required=False,
        allow_blank=True
    )

    city = serializers.CharField(
        required=False,
        allow_blank=True
    )

    state = serializers.CharField(
        required=False,
        allow_blank=True
    )

    pincode = serializers.CharField(
        required=False,
        allow_blank=True
    )

    # ==============================
    # Meta
    # ==============================

    class Meta:

        model = VendorProfile

        fields = [
            # VendorProfile
            "shop_name",
            "food_type",
            "opening_time",
            "closing_time",
            "accepting_orders",

            # User
            "first_name",
            "last_name",
            "phone_number",
            "profile_picture",

            # Address
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "pincode",
        ]

    # ==============================
    # GET / Response
    # ==============================

    def to_representation(self, instance):

        data = super().to_representation(instance)

        user = instance.user

        # ------------------------------
        # User
        # ------------------------------

        data["first_name"] = user.first_name
        data["last_name"] = user.last_name
        data["phone_number"] = user.phone_number

        if user.profile_picture:
            request = self.context.get("request")

            if request:
                data["profile_picture"] = request.build_absolute_uri(
                    user.profile_picture.url
                )
            else:
                data["profile_picture"] = user.profile_picture.url
        else:
            data["profile_picture"] = None

        # ------------------------------
        # Address
        # ------------------------------

        try:
            address = user.address

            data["address_line_1"] = address.address_line_1 or ""
            data["address_line_2"] = address.address_line_2 or ""
            data["city"] = address.city or ""
            data["state"] = address.state or ""
            data["pincode"] = address.pincode or ""

        except Address.DoesNotExist:

            data["address_line_1"] = ""
            data["address_line_2"] = ""
            data["city"] = ""
            data["state"] = ""
            data["pincode"] = ""

        return data

    # ==============================
    # UPDATE
    # ==============================

    def update(self, instance, validated_data):

        # ==============================
        # User
        # ==============================

        user = instance.user

        user_fields = [
            "first_name",
            "last_name",
            "phone_number",
            "profile_picture",
        ]

        for field in user_fields:

            if field in validated_data:
                setattr(
                    user,
                    field,
                    validated_data.pop(field)
                )

        user.save()

        # ==============================
        # Address
        # ==============================

        address_fields = [
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "pincode",
        ]

        address_data = {}

        for field in address_fields:

            if field in validated_data:
                address_data[field] = validated_data.pop(field)

        # Get existing address or create one

        address, created = Address.objects.get_or_create(
            user=user,
            defaults={
                "address_line_1": "",
                "city": "",
                "state": "",
                "pincode": "",
            }
        )

        # Update address fields

        for field, value in address_data.items():
            setattr(address, field, value)

        address.save()

        # ==============================
        # VendorProfile
        # ==============================

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance