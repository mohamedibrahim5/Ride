from authentication.models import Service, DriverCar, CustomerPlace
from authentication.serializers import (
    UserSerializer,
    LoginSerializer,
    SendOtpSerializer,
    VerifyOtpSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    FcmDeviceSerializer,
    LogoutSerializer,
    DeleteUserSerializer,
    ServiceSerializer,
    DriverCarSerializer,
    CustomerPlaceSerializer,
)
from authentication.permissions import IsAdminOrReadOnly
from rest_framework import status, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from geopy.distance import geodesic
from .models import User


class UserRegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendOtpView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyOtpView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": self.request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": self.request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUserView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class FcmDeviceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FcmDeviceSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class DeleteUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteUserSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]


class DriverCarViewSet(viewsets.ModelViewSet):
    queryset = DriverCar.objects.select_related("driver__user")
    serializer_class = DriverCarSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return super().get_serializer_context() | {"user": self.request.user}


class CustomerPlaceViewSet(viewsets.ModelViewSet):
    queryset = CustomerPlace.objects.select_related("customer__user")
    serializer_class = CustomerPlaceSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return super().get_serializer_context() | {"user": self.request.user}



class NearbyUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            lat = float(request.query_params.get("lat"))
            lng = float(request.query_params.get("lng"))
        except (TypeError, ValueError):
            return Response({"detail": "lat and lng are required and must be valid floats"}, status=400)

        service_id = request.query_params.get("service_id")

        users = User.objects.filter(is_active=True, is_verified=True, location__isnull=False)

        if service_id:
            users = users.filter(service__id=service_id)

        current_location = (lat, lng)

        def distance(user):
            user_location = tuple(map(float, user.location.split(',')))
            return geodesic(current_location, user_location).km

        users_with_distance = [(user, distance(user)) for user in users]
        users_with_distance.sort(key=lambda x: x[1])  # sort by distance ascending

        nearby_users = [user for user, _ in users_with_distance]

        serializer = UserSerializer(nearby_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)