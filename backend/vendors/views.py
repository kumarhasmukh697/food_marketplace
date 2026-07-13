from rest_framework import generics
from .serializers import VendorProfileSerializer
from .permissions import IsVendor


class VendorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorProfileSerializer
    permission_classes = [IsVendor]

    def get_object(self):
        return self.request.user.vendor_profile