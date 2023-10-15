from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=300)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return self.name


class UserCustom(AbstractUser):
    """This is custom user model, please pay attention to the instructions below

    When you will have new model which you will need to link with User model,
    please don't use standard User model for ForeignKey, since we modified it, take it from settings.py.

    Check examples below:
    1. AUTH_USER_MODEL
    from trial_assignment.settings import AUTH_USER_MODEL

    class AnotherModel(models.Model):
        user = models.ForeignKey(AUTH_USER_MODEL, ...)

    2. get_user_model()
    from django.contrib.auth import get_user_model

    User = get_user_model()

    class AnotherModel(models.Model):
        user = models.ForeignKey(User, ...)
    """

    GENDERS = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    gender = models.CharField(max_length=30, choices=GENDERS)
    age = models.PositiveIntegerField(null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name="users_custom", null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name="users_custom", null=True)

    def __str__(self):
        return f"USERNAME: {self.username} EMAIL: {self.email}"
