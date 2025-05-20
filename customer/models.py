from django.conf import settings
from django.db import models
from location_field.models.plain import PlainLocationField


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name


class CustomerPlace(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    location = PlainLocationField(based_fields=["cairo"], zoom=7)

    def __str__(self):
        return self.title
