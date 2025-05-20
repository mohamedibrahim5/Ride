from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from driver.models import Driver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_driver(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]

    if created and instance.user_type == "DR":
        Driver.objects.create(user=instance)
