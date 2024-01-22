
from django.shortcuts import render
from dj_rest_auth.views import AllowAny, LoginView
from drfauth.serializer import CustomLoginSerializer

class CustomLoginEmailView(LoginView):
    serializer_class = CustomLoginSerializer


