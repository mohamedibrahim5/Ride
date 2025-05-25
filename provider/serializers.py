from user.models import ServiceType
from rest_framework import serializers

class ServiceProviderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = "__all__"