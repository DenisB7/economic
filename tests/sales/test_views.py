import io
import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sales.models import Sale


@pytest.fixture
def user():
    """Create a user object."""

    return get_user_model().objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass"
    )


@pytest.fixture
def sale(user):
    """Create a sale object."""

    return Sale.objects.create(
        date="2022-01-01",
        product="Test Product",
        sales_number=10,
        revenue=100.0,
        user=user
    )


@pytest.fixture
def api_client(user):
    """Create an API client."""

    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_sale_list(api_client, sale):
    """Test sale list."""

    url = reverse("sales-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["product"] == "Test Product"


@pytest.mark.django_db
def test_sale_create(api_client):
    """Test sale create."""

    url = reverse("sales-list")
    data = {
        "date": "2022-01-01",
        "product": "Test Product",
        "sales_number": 10,
        "revenue": 100.0,
        "file": io.StringIO(
            "date,product,sales_number,revenue\n"
            "2022-01-01,Test Product 2,20,200.0\n"
        ),
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_201_CREATED
    assert Sale.objects.count() == 1


@pytest.mark.django_db
def test_sale_create_no_file(api_client):
    """Test sale create with no file."""

    url = reverse("sales-list")
    data = {
        "date": "2022-01-01",
        "product": "Test Product",
        "sales_number": 10,
        "revenue": 100.0,
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"error": "File not found"}


@pytest.mark.django_db
def test_sale_detail(api_client, sale):
    """Test sale detail."""

    url = reverse("sale-detail", args=[sale.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["product"] == "Test Product"


@pytest.mark.django_db
def test_sale_update(api_client, sale):
    """Test sale update."""

    url = reverse("sale-detail", args=[sale.pk])
    data = {"product": "Updated Product"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["product"] == "Updated Product"


@pytest.mark.django_db
def test_sale_delete(api_client, sale):
    """Test sale delete."""

    url = reverse("sale-detail", args=[sale.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Sale.objects.count() == 0


@pytest.mark.django_db
def test_sale_statistics(api_client, sale):
    """Test sale statistics."""

    url = reverse("sale-statistics")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["average_sales_for_current_user"] == 10.0
    assert response.data["average_sale_all_user"] == 10.0
    assert response.data["highest_revenue_sale_for_current_user"]["revenue"] == 100.0
    assert response.data["product_highest_revenue_for_current_user"]["product_name"] == "Test Product"
    assert response.data["product_highest_sales_number_for_current_user"]["product_name"] == "Test Product"
    assert response.data["product_highest_sales_number_for_current_user"]["sales_number"] == 10
