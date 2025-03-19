from django.urls import path  # type: ignore

from dj_rest_auth.jwt_auth import get_refresh_view  # type: ignore
from dj_rest_auth.registration.views import RegisterView  # type: ignore
from dj_rest_auth.views import LoginView, LogoutView  # type: ignore
from rest_framework_simplejwt.views import TokenVerifyView  # type: ignore

from . import api

urlpatterns = [
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('<uuid:pk>/', api.host_detail, name='host_details'),
    path('reservations/', api.reservations_list, name='reservations_list'),
]
