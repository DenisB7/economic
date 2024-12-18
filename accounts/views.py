from django.contrib.auth import authenticate, login, logout, get_user_model

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from accounts.models import Country
from accounts.serializers import (
    CountrySerializer,
    CustomLogoutSerializer,
    TokenSerializer,
    UserSerializer,
)


User = get_user_model()


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAuthenticated,)


class LoginView(generics.GenericAPIView):
    serializer_class = TokenSerializer

    def post(self, request):
        """Login a user with email and password."""

        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        serializer = self.get_serializer(instance=token)
        return Response(
            {
                "token": serializer.data["key"],
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomLogoutSerializer

    def get(self, request):
        """Logout a user."""

        logout(request)
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("sessionid")
        return response
