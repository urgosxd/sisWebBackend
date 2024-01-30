from rest_framework.serializers import ModelSerializer
from crud.models import FichaTecnica, Tour
from rest_framework import serializers
import base64

class FichaTecnicaSerializer(ModelSerializer):
    def create(self, validated_data):
        print("GAA")
        format, filestr = validated_data["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        ext = format.split('/')[-1]  # guess file extension
        validated_data["Doc_Content"] = base64.b64decode(filestr)
        instance = FichaTecnica.objects.create(**validated_data)
        return instance
    def validate_Doc_Content(self, value):
        print(value)
        return value
    class Meta:
        model = FichaTecnica
        fields='__all__'

class TourModelSerializer(ModelSerializer):
    fichasTecnicas = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Tour
        # fields = ['ciudad','excursion','provedor','ppp','pvp','fichasTecnicas']
        fields = '__all__'


