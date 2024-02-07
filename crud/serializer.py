from rest_framework.serializers import ModelSerializer
from crud.models import FichaTecnica, Notification, Tour
from rest_framework import serializers
import base64

class BinaryField(serializers.Field):
    def to_representation(self, value):
        return value.decode('latin-1')
    def to_internal_value(self, value):
         return value

class FichaTecnicaSerializer(ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields='__all__'
    Doc_Content = BinaryField()

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
class TourModelSerializer(ModelSerializer):
    fichasTecnicas = serializers.PrimaryKeyRelatedField(many=True,queryset=FichaTecnica.objects.all())
    class Meta:
        model = Tour
        # fields = ['ciudad','excursion','provedor','ppp','pvp','fichasTecnicas']
        fields = '__all__'


