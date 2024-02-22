from django.contrib.auth import authenticate
from rest_framework import serializers,exceptions
from drfauth.models import CustomUser
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = [
      "username",
      "password",
      "role"
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
class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.CharField(max_length=30)
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['role'] = self.validated_data.get('role', '')
        return data_dict


