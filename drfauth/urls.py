from dj_rest_auth.views import AllowAny, LoginView
from dj_rest_auth.jwt_auth import get_refresh_view
from django.urls import path
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
        path("login/",LoginView.as_view(),name="rest_login"),
         path("register/", RegisterView.as_view(), name="rest_register"),
         path("tokken/refresh/",get_refresh_view().as_view(),name="simplejwt")
        ]
