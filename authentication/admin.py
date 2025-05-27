from django.contrib import admin
from django.contrib.auth.models import Group
from authentication.models import (
    User,
    UserOtp,
    Service,
    Provider,
    Driver,
    DriverCar,
    Customer,
    CustomerPlace,
)

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(UserOtp)
admin.site.register(Service)
admin.site.register(Provider)
admin.site.register(Driver)
admin.site.register(DriverCar)
admin.site.register(Customer)
admin.site.register(CustomerPlace)
