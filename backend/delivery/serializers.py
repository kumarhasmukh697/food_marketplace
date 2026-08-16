from rest_framework import serializers

from accounts.models import Address
from .models import DeliveryPartnerProfile




class DeliveryPartnerProfileSerializer(serializers.ModelSerializer):

    # =====================================================
    # USER FIELDS
    # =====================================================

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

    # =====================================================
    # ADDRESS FIELDS
    # =====================================================

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

    # =====================================================
    # META
    # =====================================================

    class Meta:

        model = DeliveryPartnerProfile

        fields = [

            # -----------------------------
            # Delivery Partner
            # -----------------------------

            "vehicle_type",
            "vehicle_number",
            "driving_license_number",

            # -----------------------------
            # User
            # -----------------------------

            "first_name",
            "last_name",
            "phone_number",
            "profile_picture",

            # -----------------------------
            # Address
            # -----------------------------

            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "pincode",

            # -----------------------------
            # Delivery Statistics
            # -----------------------------

            "rating",
            "total_deliveries",
        ]

    # =====================================================
    # GET / SERIALIZATION
    # =====================================================

    def to_representation(self, instance):

        data = super().to_representation(instance)

        # =================================================
        # USER
        # =================================================

        user = instance.user

        data["first_name"] = user.first_name or ""
        data["last_name"] = user.last_name or ""
        data["phone_number"] = user.phone_number or ""

        # -----------------------------
        # Profile Picture
        # -----------------------------

        if user.profile_picture:

            request = self.context.get("request")

            if request:

                data["profile_picture"] = (
                    request.build_absolute_uri(
                        user.profile_picture.url
                    )
                )

            else:

                data["profile_picture"] = (
                    user.profile_picture.url
                )

        else:

            data["profile_picture"] = None

        # =================================================
        # ADDRESS
        # =================================================

        try:

            address = user.address

            data["address_line_1"] = (
                address.address_line_1 or ""
            )

            data["address_line_2"] = (
                address.address_line_2 or ""
            )

            data["city"] = (
                address.city or ""
            )

            data["state"] = (
                address.state or ""
            )

            data["pincode"] = (
                address.pincode or ""
            )

        except Address.DoesNotExist:

            data["address_line_1"] = ""
            data["address_line_2"] = ""
            data["city"] = ""
            data["state"] = ""
            data["pincode"] = ""

        # =================================================
        # DELIVERY PARTNER STATISTICS
        # =================================================

        data["rating"] = instance.rating
        data["total_deliveries"] = instance.total_deliveries

        return data

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, instance, validated_data):

        # =================================================
        # USER
        # =================================================

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

        # =================================================
        # ADDRESS
        # =================================================

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

                address_data[field] = validated_data.pop(
                    field
                )

        # ---------------------------------------------
        # Get existing address or create one
        # ---------------------------------------------

        address, created = Address.objects.get_or_create(

            user=user,

            defaults={
                "address_line_1": "",
                "address_line_2": "",
                "city": "",
                "state": "",
                "pincode": "",
            }
        )

        # ---------------------------------------------
        # Update address
        # ---------------------------------------------

        for field, value in address_data.items():

            setattr(
                address,
                field,
                value
            )

        address.save()

        # =================================================
        # DELIVERY PARTNER
        # =================================================

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        instance.save()

        return instance