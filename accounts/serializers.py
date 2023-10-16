from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Country, City


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "gender",
            "age",
            "country",
            "city",
        )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


class CountrySerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ("id", "name", "cities")

    def get_cities(self, obj):
        """This method is used to get cities for each country."""

        cities = obj.cities
        return CitySerializer(cities, many=True).data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        """This method is used to get token for user."""

        token = super().get_token(user)

        token["email"] = user.email
        token["password"] = "password"

        return token

    def validate(self, attrs):
        """This method is used to validate data from request."""

        data = super().validate(attrs)

        data["token"] = data["access"]
        del data["refresh"]
        del data["access"]
        data["user_id"] = self.user.id

        return data
