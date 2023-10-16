from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.authtoken.models import Token

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
        fields = ("id", "name")


class CountrySerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ("id", "name", "cities")

    def get_cities(self, obj):
        """This method is used to get cities for each country."""

        cities = obj.cities
        return CitySerializer(cities, many=True).data


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ("key",)


class CustomLogoutSerializer(serializers.Serializer):
    pass
