from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api_eventos.viewsets.AuthEvento import valida_token_user
from ..models.eventos import EventoTipo, Pessoa
from ..serializers.eventos_tipo_serializers import EventosTipoSerializer

@api_view(['GET', 'PUT','POST','DELETE'])
def evento_tipo(request):
    if request.method == 'GET':
        data = get(request)
        return data
    else:
        return Response(status = 400, data="Metodo não permitido")

def get(request):
    valida = valida_token_user(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")
    try:
        pessoa = Pessoa.objects.get(email = valida.user.username)
        if pessoa.status == 1:
            evento = EventoTipo.objects.all()
            serializer = EventosTipoSerializer(evento, many=True)
            return JSONResponse(serializer.data)
        else:
            return Response(status=400, data="Não autorizado!")

    except:
        return Response(status=400, data="Não autorizado!")

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)