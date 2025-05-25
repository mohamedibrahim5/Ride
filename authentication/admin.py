from django.contrib import admin
from authentication.models import UserOtp
from user.models import ServiceType


admin.site.register(UserOtp)
admin.site.register(ServiceType)
