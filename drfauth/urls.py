from dj_rest_auth.views import AllowAny, LoginView
from django.urls import path
from dj_rest_auth.registration.views import RegisterView

from drfauth.views import CustomLoginEmailView

urlpatterns = [
        path("login/",LoginView.as_view(),name="rest_login"),
         path("register/", RegisterView.as_view(), name="rest_register"),
        ]
