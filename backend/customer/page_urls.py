from django.urls import path
from . import page_views


urlpatterns = [
    path('home/', page_views.dashboard, name='home'),
    path('orders/', page_views.dashboard, name='orders'),
    path('explore/<slug:slug>/', page_views.explore_vendor, name='explore'),
    path('favorites/', page_views.dashboard, name='favorites'),
    path('tracking/', page_views.dashboard, name='tracking'),
]