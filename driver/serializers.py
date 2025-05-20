from driver.models import DriverCar, Driver
from rest_framework import serializers


class DriverCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverCar
        fields = ["id", "type", "model", "number", "color", "image", "documents"]

    def create(self, validated_data):
        user = self.context.get("user")
        driver = Driver.objects.get(user=user)
        return DriverCar.objects.create(driver=driver, **validated_data)
