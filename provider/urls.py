from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import ServiceProviderType
from django.urls import path, include


router = DefaultRouter()
router.register(r'service-types', ServiceProviderType, basename='service-type')



urlpatterns = [
    # Include service type routes
    path("", include(router.urls)),
]
