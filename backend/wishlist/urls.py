from django.urls import path
from .views import FavoriteRestaurantView


urlpatterns = [
path( "favorites/<int:vendor_id>/", FavoriteRestaurantView.as_view(), name="favorite-restaurant"),
]