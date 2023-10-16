from django.contrib import admin

from accounts.models import City, Country, UserCustom


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country__name",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)


@admin.register(UserCustom)
class UserCustomAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )
    list_filter = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )
