from django.urls import path
from sales import views

urlpatterns = [
    path("api/v1/sale_statistics/", views.SaleStatistics.as_view(), name="sale-statistics"),
    path("api/v1/sales/$<int:pk>/", views.SaleDetail.as_view(), name="sale-detail"),
    path("api/v1/sales/", views.SaleList.as_view(), name="sales-list"),
]
