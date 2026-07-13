from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    
    # PAGE VIEWS URLS
    path("", include("accounts.page_urls")),
    path("", include("customer.page_urls")),
    path("", include("vendors.page_urls")),
    path("", include("delivery.page_urls")),



    # API VIEWS URLS
    path("api/accounts/", include("accounts.urls")),
    path("api/categories/", include("categories.urls")),
    # path("api/vendors/", include("vendors.urls")),
    # path("api/products/", include("products.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)