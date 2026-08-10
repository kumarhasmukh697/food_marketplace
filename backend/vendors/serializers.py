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

    ##############################
    # User Fields
    ##############################
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone_number = serializers.CharField(source="user.phone_number")
    profile_picture = serializers.ImageField(
        source="user.profile_picture",
        required=False,
        allow_null=True,
    )

    ##############################
    # Address Fields
    ##############################
    #

    address_line_1 = serializers.CharField(
        source="address.address_line_1"
    )

    address_line_2 = serializers.CharField(
        source="address.address_line_2",
        required=False,
        allow_blank=True,
    )

    city = serializers.CharField(
        source="address.city"
    )

    state = serializers.CharField(
        source="address.state"
    )

    pincode = serializers.CharField(
        source="address.pincode"
    )

    class Meta:

        model = VendorProfile

        fields = [

            #
            # VendorProfile
            #

            "shop_name",
            "opening_time",
            "closing_time",
            "accepting_orders",

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

    def update(self, instance, validated_data):

        ################################
        # User
        #################################

        user_data = validated_data.pop("user", {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()


        ##############################
        # Address
        ##############################

        address_data = validated_data.pop("address", {})
        address = instance.address
        if address is None:
            address = Address.objects.create(user=user)
            instance.address = address
        for attr, value in address_data.items():
            setattr(address, attr, value)
        #
        # keep address synced
        #
        address.save()


        ##############################
        # VendorProfile
        ##############################

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
