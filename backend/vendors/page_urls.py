from django.urls import path
from . import page_views



urlpatterns = [
    path('v-dashboard/', page_views.dashboard, name='v-dashboard'),
    path('v-orders/', page_views.dashboard, name='v-orders'),
    path('menu/', page_views.dashboard, name='menu'),
    path('analytics/',page_views.dashboard, name='analytics'),
]