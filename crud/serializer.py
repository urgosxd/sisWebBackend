from rest_framework.serializers import ModelSerializer, raise_errors_on_nested_writes
from rest_framework.utils import model_meta
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
        fields = ['id','ciudad','excursion','provedor','ppp','pvp','fichasTecnicas']
    def create(self,validated_data):
        print(self.context['request'])
        validated_data.pop('fichasTecnicas')
        user = self.context['request'].user
        newInstance = Tour.objects.create(lastAccessUser=user,**validated_data)
        return newInstance
    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        print(validated_data)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        user = self.context['request'].user
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                if attr == "lastAccessUser":
                    attr = user
                setattr(instance, attr, value)
        instance.save()
        
        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

