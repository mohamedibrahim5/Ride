from django.contrib.auth.models import AbstractUser
from django.db import models
from location_field.models.plain import PlainLocationField
from user.choices import USER_CHOICES, SERVICE_CHOICES
from user.managers import UserManager

class ServiceType(models.Model):
    name = models.CharField(max_length=20, unique=True)


class User(AbstractUser):
    username = None
    REQUIRED_FIELDS = []
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to="user/images/")
    user_type = models.CharField(max_length=2, choices=USER_CHOICES)
    # service_type = models.CharField(
    #     max_length=2,
    #     choices=SERVICE_CHOICES,
    #     null=True,
    #     blank=True,
    # )
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    documents = models.FileField(upload_to="user/files/", null=True, blank=True)
    heading = models.CharField(max_length=20, null=True, blank=True)
    location = PlainLocationField(based_fields=["cairo"], zoom=7, null=True, blank=True)
    in_ride = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "phone"

    def __str__(self):
        return str(self.phone)
