from rest_framework import generics
from .models import Product
from .serializers import ProductListSerializer , ProductCreateUpdateSerializer
from .permissions import ProductPermission



# handles GET and POST request
class ProductListCreateView(generics.ListCreateAPIView):

    queryset = Product.objects.select_related("vendor","category")
    permission_classes = [ProductPermission]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductListSerializer
        return ProductCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.vendor_profile)



# handles UPDATE,DELETE request
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.select_related("vendor","category")
    permission_classes = [ProductPermission]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductListSerializer
        return ProductCreateUpdateSerializer