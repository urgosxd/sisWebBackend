from rest_framework.serializers import ModelSerializer
from crud.models import FichaTecnica, Tour
from rest_framework import serializers

class FichaTecnicaSerializer(ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields='__all__'

class TourModelSerializer(ModelSerializer):
    fichasTecnicas = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Tour
        # fields = ['ciudad','excursion','provedor','ppp','pvp','fichasTecnicas']
        fields = '__all__'


