from django.urls import path
from . import page_views



urlpatterns = [
    path('d-dashboard/', page_views.dashboard, name='d-dashboard'),
    path('d-home/', page_views.dashboard, name='d-home'),
    path('earnings/', page_views.earnings, name='earnings'),
    path('completed/delivery/', page_views.completed_delivery, name='delivery'),
    path('delivery/marketplace/', page_views.dashboard, name='marketplace'),
    path('orders/', page_views.order, name='orders'),
    

]