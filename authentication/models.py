from django.conf import settings
from django.db import models


class UserOtp(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=20)

    def __str__(self):
        return self.user.full_name
