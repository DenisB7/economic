import pytest

from django.db.utils import IntegrityError

from accounts.models import Country, City, UserCustom


@pytest.fixture
def country():
    """Create a country object."""

    return Country.objects.create(name="Test Country")


@pytest.fixture
def city(country):
    """Create a city object."""

    return City.objects.create(name="Test City", country=country)


@pytest.fixture
def user(country, city):
    """Create a user object."""

    return UserCustom.objects.create(
        username="testuser",
        email="testuser@example.com",
        gender="male",
        age=25,
        country=country,
        city=city,
    )


@pytest.mark.django_db
def test_country_str(country):
    """Test country string representation."""

    assert str(country) == "Test Country"


@pytest.mark.django_db
def test_city_str(city):
    """Test city string representation."""

    assert str(city) == "Test City"


@pytest.mark.django_db
def test_user_str(user):
    """Test user string representation."""

    assert str(user) == "USERNAME: testuser EMAIL: testuser@example.com"


@pytest.mark.django_db
def test_user_custom_model(country, city):
    """Test user model."""

    user = UserCustom.objects.create(
        username="testuser2",
        email="testuser2@example.com",
        gender="male",
        age=25,
        country=country,
        city=city,
    )
    assert user.username == "testuser2"
    assert user.email == "testuser2@example.com"
    assert user.gender == "male"
    assert user.age == 25
    assert user.country == country
    assert user.city == city


@pytest.mark.django_db
def test_country_model():
    """Test country model."""

    with pytest.raises(IntegrityError):
        Country.objects.create(name=None)


@pytest.mark.django_db
def test_city_model(country):
    """Test city model."""

    with pytest.raises(IntegrityError):
        City.objects.create(name=None, country=country)
