from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from vendors.models import VendorProfile
from .models import FavoriteRestaurant
from .serializers import FavoriteRestaurantSerializer

# Create your views here.


class FavoriteRestaurantView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, vendor_id):
        vendor = get_object_or_404(VendorProfile,id=vendor_id)
        favorite, created = FavoriteRestaurant.objects.get_or_create(user=request.user, vendor=vendor)

        if not created:
            favorite.delete()
            return Response({
                "message": "Restaurant removed from favorites",
                "is_favorite": False
            })

        return Response({
            "message": "Restaurant added to favorites",
            "is_favorite": True
        })
    



class FavoriteRestaurantListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteRestaurant.objects.filter(user=request.user).select_related("vendor", "vendor__address" )
        serializer = FavoriteRestaurantSerializer( favorites, many=True)
        return Response(serializer.data)