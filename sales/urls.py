from django.urls import path
from sales import views

urlpatterns = [
    path("api/v1/sale_statistics/", views.SaleStatistics.as_view()),
    path("api/v1/sales/$<int:pk>/", views.SaleDetail.as_view()),
    path("api/v1/sales/", views.SaleList.as_view()),
]
