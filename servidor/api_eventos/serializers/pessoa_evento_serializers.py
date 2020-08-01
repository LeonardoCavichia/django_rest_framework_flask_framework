from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_eventos.models.eventos import PessoaEvento, Pessoa
from api_eventos.serializers.user_serializer import PessoaSerializer


class ParticipanteSerializer(ModelSerializer):
    class Meta:
        model = PessoaEvento
        fields = ["id", "userId", "eventoId","registrationDate"]


class ParticipanteEventoSerializer(ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    def get_username(self, PessoaEvento):
        pk = PessoaEvento.userId
        participante = Pessoa.objects.get(id= pk.id)
        return str(participante.username)

    class Meta:
        model = PessoaEvento
        fields = ["id", "username", "registrationDate"]


