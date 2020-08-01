from rest_framework.serializers import ModelSerializer
from ..models.eventos import EventoTipo

class EventosTipoSerializer(ModelSerializer):
    class Meta:
        model = EventoTipo
        fields = ('name','id')

