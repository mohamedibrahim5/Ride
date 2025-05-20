from driver.views import DriverCarViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("driver-cars", DriverCarViewSet, basename="driver-cars")

urlpatterns = router.urls
