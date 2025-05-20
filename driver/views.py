from driver.models import DriverCar
from driver.serializers import DriverCarSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class DriverCarViewSet(ModelViewSet):
    queryset = DriverCar.objects.select_related("driver__user")
    serializer_class = DriverCarSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return super().get_serializer_context() | {"user": self.request.user}
