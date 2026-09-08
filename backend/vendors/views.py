from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from .permissions import IsVendor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import VendorLocationSerializer, VendorProfileSerializer1



# this view handles GET,PUT,PATCH reuqest from vendors only
class VendorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorProfileSerializer1
    permission_classes = [IsVendor]

    parser_classes = [MultiPartParser,FormParser,]

    def get_object(self):
        return self.request.user.vendor_profile




class VendorLocationUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        if request.user.role != "vendor":
            return Response(
                {
                    "detail": "Only vendors can update shop location."
                },
                status=403
            )

        address = getattr(request.user, "address", None)

        if not address:
            return Response(
                {
                    "detail": "Vendor address not found."
                },
                status=404
            )

        serializer = VendorLocationSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        address.latitude = serializer.validated_data["latitude"]
        address.longitude = serializer.validated_data["longitude"]

        address.save(
            update_fields=[
                "latitude",
                "longitude"
            ]
        )

        return Response(
            {
                "message": "Vendor location updated successfully.",
                "latitude": address.latitude,
                "longitude": address.longitude,
            },
            status=200
        )