from django.urls import path

from categories.views import CategoryListCreateView

urlpatterns = [
    path("", CategoryListCreateView.as_view(), name="category-list-create"),
]