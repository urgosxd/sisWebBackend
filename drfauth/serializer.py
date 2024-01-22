from django.contrib.auth import authenticate
from rest_framework import serializers,exceptions
from drfauth.models import CustomUser
from dj_rest_auth.serializers import LoginSerializer

class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = [
      "username",
      "password",
    ]
    
class CustomLoginSerializer(LoginSerializer):
    email = None
    def authenticate(self, **options):
        return authenticate(self.context["request"], **options)

    def validate(self, attrs):
        username= attrs.get("username")
        password = attrs.get("password")
        if username and password:
            user = authenticate(
                username=username,
                password=password,
            )
            if not user:
                msg = "Incorrect credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = "No username provided."
            raise exceptions.ValidationError(msg)
        attrs["user"] = user
        return attrs

