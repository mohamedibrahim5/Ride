from user.models import ServiceType
from rest_framework import viewsets
from .serializers import ServiceProviderTypeSerializer


class ServiceProviderType(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceProviderTypeSerializer

    def get_queryset(self):
        return self.queryset