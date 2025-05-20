from customer.views import CustomerPlaceViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("customer-places", CustomerPlaceViewSet, basename="customer-places")

urlpatterns = router.urls
