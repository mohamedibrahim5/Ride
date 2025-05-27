from authentication.views import (
    UserRegisterView,
    LoginView,
    SendOtpView,
    VerifyOtpView,
    ResetPasswordView,
    ChangePasswordView,
    ProfileUserView,
    FcmDeviceView,
    LogoutView,
    DeleteUserView,
    ServiceViewSet,
    DriverCarViewSet,
    CustomerPlaceViewSet,
    ProviderViewSet,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("services", ServiceViewSet, basename="services")
router.register("providers", ProviderViewSet, basename="providers")
router.register("driver-cars", DriverCarViewSet, basename="driver-cars")
router.register("customer-places", CustomerPlaceViewSet, basename="customer-places")


urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("send-otp/", SendOtpView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOtpView.as_view(), name="verify-otp"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/", ProfileUserView.as_view(), name="profile"),
    path("fcm-device/", FcmDeviceView.as_view(), name="fcm-device"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("delete/", DeleteUserView.as_view(), name="delete-user"),
    path("", include(router.urls)),
]
