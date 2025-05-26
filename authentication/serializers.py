from authentication.choices import ROLE_CHOICES, FCM_CHOICES
from authentication.models import (
    Service,
    User,
    OneTimePassword,
    Driver,
    DriverCar,
    Customer,
    CustomerPlace,
)
from authentication.utils import send_sms
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils import timezone
from fcm_django.models import FCMDevice


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(write_only=True, choices=ROLE_CHOICES)
    service_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "password",
            "image",
            "role",
            "service_id",
            "documents",
        ]

    def validate(self, attrs):
        role = attrs.get("role")
        service_id = attrs.get("service_id", None)

        if role == "PR":
            if service_id:
                service_id = attrs.pop("service_id")
                attrs["service"] = Service.objects.get(pk=service_id)
            else:
                raise serializers.ValidationError(_("Service ID is required"))
        elif service_id:
            attrs.pop("service_id")

        return attrs

    def create(self, validated_data):
        phone = validated_data.get("phone")

        otp = send_sms(phone)

        if otp:
            user = User.objects.create_user(**validated_data)

            OneTimePassword.objects.update_or_create(user=user, otp=otp)

            return user
        else:
            raise serializers.ValidationError(_("Try again later"))

    def update(self, instance, validated_data):
        if "phone" in validated_data:
            validated_data.pop("phone")

        if "password" in validated_data:
            validated_data.pop("password")

        if "role" in validated_data:
            validated_data.pop("role")

        if "service_id" in validated_data:
            validated_data.pop("service_id")

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
            print("njhjhjhj")
            raise serializers.ValidationError(_("Invalid phone"))

        if not user.check_password(password):
            raise serializers.ValidationError(_("Invalid password"))

        if not user.is_active:
            raise serializers.ValidationError(_("User is not active"))

        if user.is_verified:
            attrs["token"] = Token.objects.get(user=user).key
            user.last_login = timezone.now()
            user.save()
        else:
            attrs["is_verified"] = False

        return attrs


class SendOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")

        user = User.objects.filter(phone=phone).first()

        if not user:
            raise serializers.ValidationError(_("Invalid phone"))

        otp = send_sms(phone)

        if otp:
            OneTimePassword.objects.update_or_create(user=user, otp=otp)
        else:
            raise serializers.ValidationError(_("Try again later"))

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
            raise serializers.ValidationError(_("Invalid phone"))

        user_otp = OneTimePassword.objects.filter(user=user).first()

        if not user_otp or user_otp.otp != otp:
            raise serializers.ValidationError(_("Invalid otp"))

        if user.is_verified or user.role == "CU":
            attrs["token"] = Token.objects.get(user=user).key
            user.last_login = timezone.now()
            user.is_verified = True
            user.is_active = True
            user.save()
        else:
            attrs["is_verified"] = False

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
            raise serializers.ValidationError(_("Passwords do not match"))

        user = self.context.get("user")

        user_otp = OneTimePassword.objects.filter(user=user).first()

        if not user_otp or user_otp.otp != otp:
            raise serializers.ValidationError(_("Invalid otp"))

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
                _("Password do not match confirm password")
            )

        user = self.context.get("user")

        if not user.check_password(old_password):
            raise serializers.ValidationError(_("Old password is incorrect"))

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

        token = user.auth_token

        attrs["token"] = token

        return attrs

    def save(self):
        token = self.validated_data["token"]

        token.delete()

        return token


class DeleteUserSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")

        user = self.context.get("user")

        if not user.check_password(password):
            raise serializers.ValidationError(_("Password is incorrect"))

        return attrs

    def save(self):
        user = self.context.get("user")

        user.auth_token.delete()

        user.delete()

        return user


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name"]


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
