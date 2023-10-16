import pytest

from django.db.utils import IntegrityError

from accounts.models import Country, City, UserCustom


@pytest.fixture
def country():
    return Country.objects.create(name="Test Country")


@pytest.fixture
def city(country):
    return City.objects.create(name="Test City", country=country)


@pytest.fixture
def user(country, city):
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
    assert str(country) == "Test Country"


@pytest.mark.django_db
def test_city_str(city):
    assert str(city) == "Test City"


@pytest.mark.django_db
def test_user_str(user):
    assert str(user) == "USERNAME: testuser EMAIL: testuser@example.com"


@pytest.mark.django_db
def test_user_custom_model(country, city):
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
    with pytest.raises(IntegrityError):
        Country.objects.create(name=None)


@pytest.mark.django_db
def test_city_model(country):
    with pytest.raises(IntegrityError):
        City.objects.create(name=None, country=country)
