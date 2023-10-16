import pytest

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from sales.models import Sale


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username="testuser", email="testuser@example.com", password="testpass"
    )


@pytest.fixture
def sale(user):
    return Sale.objects.create(
        date="2022-01-01",
        product="Test Product",
        sales_number=10,
        revenue=100.0,
        user=user,
    )


@pytest.mark.django_db
def test_sale_str(sale):
    assert str(sale) == "Test Product"


@pytest.mark.django_db
def test_sale_model(sale):
    assert sale.date == "2022-01-01"
    assert sale.product == "Test Product"
    assert sale.sales_number == 10
    assert sale.revenue == 100.0
    assert sale.user.username == "testuser"


@pytest.mark.django_db
def test_sale_model_date_null():
    with pytest.raises(IntegrityError):
        Sale.objects.create(
            date=None,
            product="Test Product",
            sales_number=10,
            revenue=100.0,
            user=get_user_model().objects.create_user(
                username="testuser2", email="testuser2@example.com", password="testpass"
            ),
        )


@pytest.mark.django_db
def test_sale_model_product_null():
    with pytest.raises(IntegrityError):
        Sale.objects.create(
            date="2022-01-01",
            product=None,
            sales_number=10,
            revenue=100.0,
            user=get_user_model().objects.create_user(
                username="testuser3", email="testuser3@example.com", password="testpass"
            ),
        )


@pytest.mark.django_db
def test_sale_model_sales_number_null():
    with pytest.raises(IntegrityError):
        Sale.objects.create(
            date="2022-01-01",
            product="Test Product",
            sales_number=None,
            revenue=100.0,
            user=get_user_model().objects.create_user(
                username="testuser4", email="testuser4@example.com", password="testpass"
            ),
        )


@pytest.mark.django_db
def test_sale_model_revenue_null():
    with pytest.raises(IntegrityError):
        Sale.objects.create(
            date="2022-01-01",
            product="Test Product",
            sales_number=10,
            revenue=None,
            user=get_user_model().objects.create_user(
                username="testuser5", email="testuser5@example.com", password="testpass"
            ),
        )


@pytest.mark.django_db
def test_sale_model_user_null():
    with pytest.raises(IntegrityError):
        Sale.objects.create(
            date="2022-01-01",
            product="Test Product",
            sales_number=10,
            revenue=100.0,
            user=None,
        )
