from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsDelivery
from .models import DeliveryPartnerProfile
from .serializers import DeliveryPartnerProfileSerializer, DeliveryOnlineStatusSerializer, DeliveryLocationSerializer






class DeliveryPartnerProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = DeliveryPartnerProfileSerializer
    permission_classes = [IsDelivery]
    parser_classes = [ MultiPartParser, FormParser]

    def get_object(self):

        delivery_partner, created = (
            DeliveryPartnerProfile.objects.get_or_create( user=self.request.user)
        )

        return delivery_partner





class DeliveryOnlineStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        delivery_partner = (request.user.delivery_partner)
        serializer = DeliveryOnlineStatusSerializer( delivery_partner,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        is_online = serializer.validated_data[ "is_online"]
        delivery_partner.is_online = is_online

        # -----------------------------------------
        # If going offline, automatically make
        # partner unavailable.
        # -----------------------------------------

        if not is_online:
            delivery_partner.is_available = False

        # -----------------------------------------
        # If going online and has no active order,
        # make partner available.
        #
        # For now we can make it available here.
        # Later we'll make this more intelligent
        # based on active orders.
        # -----------------------------------------

        else:

            delivery_partner.is_available = True

        delivery_partner.save(
            update_fields=[ "is_online", "is_available", "updated_at",]
        )

        return Response(
            {
                "message":
                    (
                        "You are now online."
                        if is_online
                        else
                        "You are now offline."
                    ),

                "is_online": delivery_partner.is_online,
                "is_available": delivery_partner.is_available,
            }
        )







class DeliveryLocationUpdateView(APIView):
    print("hello world")
    permission_classes = [IsAuthenticated]
    print("DeliveryLocationUpdateView initialized.")

    def patch(self, request):
        if request.user.role != "delivery":
            print("User is not a delivery partner.")
            return Response(
                {"detail": "Only delivery partners can update their location."},
                status=403
            )

        try:
            delivery_partner = request.user.delivery_partner
        except DeliveryPartnerProfile.DoesNotExist:
            return Response(
                {"detail": "Delivery partner profile not found."},
                status=404
            )

        serializer = DeliveryLocationSerializer(delivery_partner, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Location updated successfully.",
                "current_latitude": delivery_partner.current_latitude,
                "current_longitude": delivery_partner.current_longitude,
            },
            status=200
        )