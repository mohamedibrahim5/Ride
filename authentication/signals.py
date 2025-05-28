from authentication.models import User, Provider, Driver, Customer
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_token(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]

    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_provider(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]

    if created and instance.role == "PR":
        Provider.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_driver(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]

    if created and instance.role == "DR":
        Driver.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_customer(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]

    if created and instance.role == "CU":
        Customer.objects.create(user=instance)
