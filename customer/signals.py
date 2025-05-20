from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from customer.models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]

    if created and instance.user_type == "CU":
        Customer.objects.create(user=instance)
