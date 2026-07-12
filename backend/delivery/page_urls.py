from django.urls import path
from . import page_views



urlpatterns = [
    path('d-dashboard/', page_views.dashboard, name='d-dashboard'),
    path('d-home/', page_views.dashboard, name='d-home'),
    path('earnings/', page_views.dashboard, name='earnings'),
    path('delivery/', page_views.dashboard, name='delivery'),
    path('d-orders/', page_views.dashboard, name='d-orders'),

]