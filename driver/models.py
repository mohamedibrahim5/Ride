from django.conf import settings
from django.db import models


class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name


class DriverCar(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="cars")
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    image = models.ImageField(upload_to="car/images/", null=True, blank=True)
    documents = models.FileField(upload_to="car/files/", null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.type
