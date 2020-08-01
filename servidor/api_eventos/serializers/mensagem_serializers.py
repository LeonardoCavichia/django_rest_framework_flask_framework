from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from api_eventos.models.eventos import Mensagem

class MensagemSerializer(ModelSerializer):

    username = serializers.SerializerMethodField('get_username')
    userId = serializers.SerializerMethodField('get_userid')

    def get_username(self, Mensagem):
        pk = Mensagem.participantId
        pessoa = pk.userId
        return str(pessoa.username)

    def get_userid(self, Mensagem):
        pk = Mensagem.participantId
        pessoa = pk.userId
        return pessoa.pk

    class Meta:
        model = Mensagem
        fields = ('id', 'userId', 'username', 'messageDate', 'message')

class MensagemSerializerPut(ModelSerializer):
    class Meta:
        model = Mensagem
        fields = ('id','messageDate', 'message','participantId')

