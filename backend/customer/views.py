from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CustomerProfileSerializer
from .permissions import IsCustomer
from .models import CustomerProfile


 
class CustomerProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = CustomerProfileSerializer
    permission_classes = [IsCustomer]

    parser_classes = [MultiPartParser, FormParser,]

    def get_object(self):
        customer, created = CustomerProfile.objects.get_or_create(
            user=self.request.user
        )
        return customer