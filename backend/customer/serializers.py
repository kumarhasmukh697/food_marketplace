from rest_framework import serializers
from accounts.models import User, Address
from customer.models import CustomerProfile


class CustomerProfileSerializer(serializers.ModelSerializer):

    #
    # User Fields
    #

    first_name = serializers.CharField(
        source="user.first_name",
        required=False,
    )

    last_name = serializers.CharField(
        source="user.last_name",
        required=False,
    )

    phone_number = serializers.CharField(
        source="user.phone_number",
        required=False,
    )

    profile_picture = serializers.ImageField(
        source="user.profile_picture",
        required=False,
        allow_null=True,
    )

    #
    # Address Fields
    #

    address_line_1 = serializers.CharField(
        required=False,
    )

    address_line_2 = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    city = serializers.CharField(
        required=False,
    )

    state = serializers.CharField(
        required=False,
    )

    pincode = serializers.CharField(
        required=False,
    )

    class Meta:

        model = CustomerProfile

        fields = [

            #
            # CustomerProfile
            #

            "dietary_preference",
            "spice_level",

            #
            # User
            #

            "first_name",
            "last_name",
            "phone_number",
            "profile_picture",

            #
            # Address
            #

            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "pincode",

        ]

    def to_representation(self, instance):

        data = super().to_representation(instance)

        address = (
            instance.user.addresses
            .filter(is_default=True)
            .first()
        )

        if address:

            data["address_line_1"] = address.address_line_1
            data["address_line_2"] = address.address_line_2
            data["city"] = address.city
            data["state"] = address.state
            data["pincode"] = address.pincode

        return data

    def update(self, instance, validated_data):

        #
        # ---------------- User ----------------
        #

        user_data = validated_data.pop("user", {})

        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)

        user.save()

        #
        # ---------------- Address ----------------
        #

        address = (
            user.addresses
            .filter(is_default=True)
            .first()
        )

        if address is None:

            address = Address.objects.create(

                user=user,

                is_default=True,

                address_line_1="",
                address_line_2="",
                city="",
                state="",
                pincode="",

            )

        address.address_line_1 = validated_data.pop(
            "address_line_1",
            address.address_line_1,
        )

        address.address_line_2 = validated_data.pop(
            "address_line_2",
            address.address_line_2,
        )

        address.city = validated_data.pop(
            "city",
            address.city,
        )

        address.state = validated_data.pop(
            "state",
            address.state,
        )

        address.pincode = validated_data.pop(
            "pincode",
            address.pincode,
        )

        address.save()

        #
        # ---------------- Customer ----------------
        #

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        return instance