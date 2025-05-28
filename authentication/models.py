from authentication.choices import ROLE_CHOICES
from authentication.managers import UserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from location_field.models.plain import PlainLocationField


class Service(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    REQUIRED_FIELDS = []
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to="user/images/")
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
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


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=20)

    def __str__(self):
        return self.user.full_name


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name


class CustomerPlace(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    location = PlainLocationField(based_fields=["cairo"], zoom=7)

    def __str__(self):
        return self.title
