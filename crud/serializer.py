from rest_framework.serializers import ModelSerializer
from crud.models import FichaTecnica, Tour

class DocumentModelSerializer(ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields='__all__'

class TourModelSerializer(ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
