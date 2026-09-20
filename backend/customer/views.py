from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CustomerProfileSerializer, CustomerLocationSerializer
from .permissions import IsCustomer
from .models import CustomerProfile
from django.shortcuts import get_object_or_404
from orders.models import Order



 
class CustomerProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = CustomerProfileSerializer
    permission_classes = [IsCustomer]
    parser_classes = [MultiPartParser, FormParser,]

    def get_object(self):
        customer, created = CustomerProfile.objects.get_or_create( user=self.request.user)
        return customer






class CustomerLocationUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):
        if request.user.role != "customer":
            return Response({"detail": "Only customer can update their location."},status=403)

        address = getattr(request.user, "address", None)

        if not address:
            return Response({"detail": "Customer address not found."}, status=404)

        serializer = CustomerLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address.latitude = serializer.validated_data["latitude"]
        address.longitude = serializer.validated_data["longitude"]

        address.save(update_fields=["latitude", "longitude"])

        return Response(
            {
                "message": "Customer location updated successfully.",
                "latitude": address.latitude,
                "longitude": address.longitude,
            },
            status=200
        )






class CustomerOrderTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):

        order = get_object_or_404(
            Order.objects.select_related(
                "delivery_partner",
                "delivery_partner__user",
            ),
            id=order_id,
            customer=request.user,
        )

        if not order.delivery_partner:
            return Response(
                {
                    "detail": "A delivery partner has not been assigned yet."
                },
                status=404
            )

        delivery_partner = order.delivery_partner

        return Response(
            {
                "order_id": order.id,
                "status": order.status,

                "delivery_partner": {
                    "latitude": delivery_partner.current_latitude,
                    "longitude": delivery_partner.current_longitude,
                }
            },
            status=200
        )