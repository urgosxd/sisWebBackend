from dj_rest_auth.views import AllowAny, LoginView
from dj_rest_auth.jwt_auth import get_refresh_view
from django.urls import path
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

from drfauth.views import CustomLoginEmailView

urlpatterns = [
        path("login/",CustomLoginEmailView.as_view(),name="rest_login"),
         path("register/", RegisterView.as_view(), name="rest_register"),
         path("tokken/refresh/",TokenRefreshView().as_view(),name="simplejwt")
        ]
