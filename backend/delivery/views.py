from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsDelivery

from .models import DeliveryPartnerProfile
from .serializers import DeliveryPartnerProfileSerializer


class DeliveryPartnerProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = DeliveryPartnerProfileSerializer

    permission_classes = [IsDelivery]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_object(self):

        delivery_partner, created = (
            DeliveryPartnerProfile.objects.get_or_create(
                user=self.request.user
            )
        )

        return delivery_partner