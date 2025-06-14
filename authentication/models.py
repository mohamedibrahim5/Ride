from authentication.choices import ROLE_CHOICES
from authentication.managers import UserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.gis.db import models as gis_models



class User(AbstractUser):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to="user/images/")
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    location = PlainLocationField(based_fields=["cairo"])
    location2 = gis_models.PointField(srid=4326, null=True, blank=True)


    # inherited attributes
    username = None
    first_name = None
    last_name = None
    groups = None
    user_permissions = None
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "phone"

    def __str__(self):
        return str(self.phone)


class UserOtp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=20)

    def __str__(self):
        return self.user.name


class Service(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class ServiceImage(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="service/images/")

    def __str__(self):
        return self.service.name


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license = models.CharField(max_length=20, unique=True)
    in_ride = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class DriverCar(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    image = models.ImageField(upload_to="car/images/")
    license = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    in_ride = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class CustomerPlace(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="places")
    location = PlainLocationField(based_fields=["cairo"], zoom=7)

    def __str__(self):
        return self.customer.name


from django.db import models
from django.conf import settings

class RideStatus(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("starting", "Starting"),
        ("arriving", "Arriving"),
        ("finished", "Finished"),
        ("cancelled", "Cancelled"),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rides_as_client")
    provider = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="rides_as_provider")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lng = models.FloatField(null=True, blank=True)
    drop_lat = models.FloatField(null=True, blank=True)
    drop_lng = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

