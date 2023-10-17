import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Country, UserCustom
from accounts.serializers import CountrySerializer, UserSerializer


@pytest.fixture
def user():
    """Create a user object."""

    return UserCustom.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        gender="male",
        age=25,
    )


@pytest.fixture
def country():
    """Create a country object."""

    return Country.objects.create(name="Test Country")


@pytest.fixture
def api_client():
    """Create an API client."""

    return APIClient()


@pytest.mark.django_db
def test_user_retrieve_update_view(api_client, user):
    """Test user retrieve and update view."""

    api_client.force_authenticate(user=user)
    url = reverse("user_detail", kwargs={"pk": user.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == UserSerializer(user).data

    new_data = {"username": "newusername"}
    response = api_client.patch(url, new_data)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.username == new_data["username"]


@pytest.mark.django_db
def test_country_list_view(api_client, user, country):
    """Test country list view."""

    api_client.force_authenticate(user=user)
    url = reverse("country_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [CountrySerializer(country).data]


@pytest.mark.django_db
def test_login_view(api_client, user):
    """Test login view."""

    url = reverse("login")
    data = {"email": user.email, "password": "testpass"}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
    assert "user_id" in response.data


@pytest.mark.django_db
def test_login_view_invalid_credentials(api_client, user):
    """Test login view with invalid credentials."""

    url = reverse("login")
    data = {"email": user.email, "password": "wrongpass"}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data == {"detail": "Invalid credentials"}


@pytest.mark.django_db
def test_logout_view(api_client, user):
    """Test logout view."""

    api_client.force_authenticate(user=user)
    url = reverse("logout")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "sessionid" in response.cookies.keys()
