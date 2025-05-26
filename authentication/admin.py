from django.contrib import admin
from authentication.models import (
    Service,
    User,
    OneTimePassword,
    Provider,
    Driver,
    DriverCar,
    Customer,
    CustomerPlace,
)


admin.site.register(Service)
admin.site.register(OneTimePassword)
admin.site.register(User)
admin.site.register(Provider)
admin.site.register(Driver)
admin.site.register(DriverCar)
admin.site.register(Customer)
admin.site.register(CustomerPlace)
