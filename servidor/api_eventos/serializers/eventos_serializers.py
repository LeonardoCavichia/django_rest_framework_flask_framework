from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from api_eventos.serializers.pessoa_evento_serializers import ParticipanteEventoSerializer
from api_eventos.serializers.user_serializer import PessoaSerializer
from ..models.eventos import Eventos, PessoaEvento
from ..serializers.eventos_tipo_serializers import EventosTipoSerializer


class EventosSerializer(ModelSerializer):
    eventType = EventosTipoSerializer()
    user = PessoaSerializer()
    participant = serializers.SerializerMethodField()
    def get_participant(self, Eventos):
        participante = PessoaEvento.objects.filter(eventoId=Eventos, status=True)
        participantes = ParticipanteEventoSerializer(participante, many=True)
        return participantes.data

    class Meta:
        model = Eventos
        fields = ["participant",'id', 'title', 'startDate', 'endDate', 'street', 'neighborhood', 'city',
                  'referencePoint','description', 'status', 'eventType', 'user']

