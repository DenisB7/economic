from django.contrib import admin

from accounts.models import UserCustom


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
