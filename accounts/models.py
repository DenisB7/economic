from django.db import models
from django.contrib.auth.models import AbstractUser


class UserCustom(AbstractUser):
    """We can remove and add desired additional fields like this:

    new_field = models.CharField(max_length=300, null=True)
    ---
    NOTE:
    When you will have new model which you will need to link with User model,
    please don't use standard User model for ForeignKey, since we modified it, take it from settings.py:

    from trial_assignment.settings import AUTH_USER_MODEL

    class AnotherModel(models.Model):
        user = models.ForeignKey(AUTH_USER_MODEL, ...)
    ---
    """

    GENDERS = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    gender = models.CharField(max_length=30, choices=GENDERS)
    age = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"USERNAME: {self.username} EMAIL: {self.email}"
