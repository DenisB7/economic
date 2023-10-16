from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from accounts.models import UserCustom


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserCustom
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserCustom
        fields = "__all__"
