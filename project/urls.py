from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import path, include
from project.admin import admin

urlpatterns = [
    path(
        "",
        lambda request: HttpResponse("Welcome to the Riders API"),
        name="welcome-page",
    ),
    path("admin/", admin.site.urls),
    path("customer/", include("customer.urls")),
    path("driver/", include("driver.urls")),
    path("authentication/", include("authentication.urls")),
    path("provider/", include("provider.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
