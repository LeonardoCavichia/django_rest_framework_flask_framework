from rest_framework.serializers import ModelSerializer
from ..models.eventos import Pessoa

class PessoaSerializer(ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ('id','username','email','birthdate','sex')

