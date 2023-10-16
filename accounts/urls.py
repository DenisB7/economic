from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import UserRetrieveUpdateView, CountryListView, LoginView, LogoutView


urlpatterns = [
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/users/$<int:pk>/', UserRetrieveUpdateView.as_view(), name='user_detail'),
    path('api/v1/countries/', CountryListView.as_view(), name='country_list'),
]
