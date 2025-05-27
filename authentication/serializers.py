from authentication.choices import (
    ROLE_CUSTOMER,
    ROLE_DRIVER,
    ROLE_PROVIDER,
    ROLE_CHOICES,
    FCM_CHOICES,
)
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
from authentication.utils import send_sms, extract_user_data, update_user_data
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils import timezone
from fcm_django.models import FCMDevice


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(write_only=True, choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "password",
            "image",
            "role",
            "location",
        ]

    def create(self, validated_data):
        phone = validated_data.get("phone")

        otp = send_sms(phone)

        if otp:
            user = User.objects.create_user(**validated_data)

            UserOtp.objects.update_or_create(user=user, otp=otp)

            return user
        else:
            raise serializers.ValidationError(
                {"sms": _("the sms service is not working try again later")}
            )

    def update(self, instance, validated_data):
        if "phone" in validated_data:
            validated_data.pop("phone")

        if "password" in validated_data:
            validated_data.pop("password")

        if "role" in validated_data:
            validated_data.pop("role")

        return super().update(instance, validated_data)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name"]


class ProviderSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Provider
        fields = ["id", "user", "service_id"]

    def validate(self, attrs):
        service_id = attrs.pop("service_id")

        service = Service.objects.filter(pk=service_id).first()

        if not service:
            raise serializers.ValidationError({"service": _("Service not found.")})

        attrs["service"] = service

        return attrs

    def create(self, validated_data):
        user_data = extract_user_data(self.initial_data)
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return Provider.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = update_user_data(instance, self.initial_data)
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return super().update(instance, validated_data)


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = ["id", "user", "license", "in_ride"]

    def create(self, validated_data):
        user_data = extract_user_data(self.initial_data)
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return Driver.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = update_user_data(instance, self.initial_data)
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return super().update(instance, validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user", "in_ride"]

    def create(self, validated_data):
        user_data = extract_user_data(self.initial_data)
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return Customer.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = update_user_data(instance, self.initial_data)
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=128, read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        user = User.objects.filter(phone=phone).first()

        if not user:
            raise serializers.ValidationError({"phone": _("Invalid phone")})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": _("Invalid password")})

        if not user.is_active:
            raise serializers.ValidationError({"active": _("User is not active")})

        is_verified = True

        if user.role == ROLE_PROVIDER:
            is_verified = user.provider.is_verified

        if user.role == ROLE_DRIVER:
            is_verified = user.driver.is_verified

        if is_verified:
            user.last_login = timezone.now()
            user.save()
            attrs["token"] = Token.objects.get(user=user).key
        else:
            raise serializers.ValidationError({"verified": _("User is not verified")})

        return attrs


class SendOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")

        user = User.objects.filter(phone=phone).first()

        if not user:
            raise serializers.ValidationError({"phone": _("Invalid phone")})

        otp = send_sms(phone)

        if otp:
            UserOtp.objects.update_or_create(user=user, otp=otp)
        else:
            raise serializers.ValidationError(
                {"sms": _("the sms service is not working try again later")}
            )

        return attrs


class VerifyOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, write_only=True)
    otp = serializers.CharField(max_length=20, write_only=True)
    token = serializers.CharField(max_length=128, read_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        otp = attrs.get("otp")

        user = User.objects.filter(phone=phone).first()

        if not user:
            raise serializers.ValidationError({"phone": _("Invalid phone")})

        user_otp = UserOtp.objects.filter(user=user).first()

        if not user_otp or user_otp.otp != otp:
            raise serializers.ValidationError({"otp": _("Invalid otp")})

        if user.role == ROLE_CUSTOMER:
            user.last_login = timezone.now()
            attrs["token"] = Token.objects.get(user=user).key

        user.is_active = True

        user.save()

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        otp = data.get("otp")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"password": _("Passwords do not match")})

        user = self.context.get("user")

        user_otp = UserOtp.objects.filter(user=user).first()

        if not user_otp or user_otp.otp != otp:
            raise serializers.ValidationError({"otp": _("Invalid otp")})

        data["user"] = user

        return data

    def save(self):
        user = self.validated_data["user"]

        password = self.validated_data["password"]

        user.set_password(password)

        user.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        old_password = data.get("old_password")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": _("Password do not match confirm password")}
            )

        user = self.context.get("user")

        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {"password": _("Old password is incorrect")}
            )

        data["user"] = user

        return data

    def save(self):
        user = self.validated_data["user"]

        password = self.validated_data["password"]

        user.set_password(password)

        user.save()

        return user


class FcmDeviceSerializer(serializers.Serializer):
    registration_id = serializers.CharField(max_length=255, write_only=True)
    device_type = serializers.ChoiceField(
        choices=FCM_CHOICES,
        write_only=True,
    )

    def create(self, validated_data):
        registration_id = validated_data.get("registration_id")
        device_type = validated_data.get("device_type")
        user = self.context.get("user")

        device, created = FCMDevice.objects.update_or_create(
            user=user,
            defaults={
                "registration_id": registration_id,
                "type": device_type,
                "active": True,
            },
        )

        return device


class LogoutSerializer(serializers.Serializer):
    def validate(self, attrs):
        user = self.context.get("user")

        attrs["user"] = user

        return attrs

    def save(self):
        user = self.validated_data["user"]

        device = FCMDevice.objects.get(user=user)

        device.active = False

        return device.save()


class DeleteUserSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")

        user = self.context.get("user")

        if not user.check_password(password):
            raise serializers.ValidationError({"password": _("Password is incorrect")})

        return attrs

    def save(self):
        user = self.context.get("user")

        user.auth_token.delete()

        device = FCMDevice.objects.get(user=user)

        device.delete()

        return user.delete()


class DriverCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverCar
        fields = ["id", "type", "model", "number", "color", "image", "documents"]

    def create(self, validated_data):
        user = self.context.get("user")
        driver = Driver.objects.get(user=user)
        return DriverCar.objects.create(driver=driver, **validated_data)


class CustomerPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPlace
        fields = ["id", "title", "location"]

    def create(self, validated_data):
        user = self.context.get("user")
        customer = Customer.objects.get(user=user)
        return CustomerPlace.objects.create(customer=customer, **validated_data)
