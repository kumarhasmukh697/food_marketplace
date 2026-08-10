from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from .serializers import VendorProfileSerializer1
from .permissions import IsVendor


# this view handles GET,PUT,PATCH reuqest from vendors only
class VendorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorProfileSerializer1
    permission_classes = [IsVendor]

    parser_classes = [MultiPartParser,FormParser,]

    def get_object(self):
        return self.request.user.vendor_profile