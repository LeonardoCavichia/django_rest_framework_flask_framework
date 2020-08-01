import json
from datetime import datetime

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api_eventos.serializers.mensagem_serializers import MensagemSerializer, MensagemSerializerPut
from api_eventos.viewsets.AuthEvento import valida_token, valida_token_user
from ..models.eventos import PessoaEvento, Mensagem, Eventos


@api_view(['POST', 'PUT'])
def mensagem_view(request):

    if request.method == 'POST':
        data = post(request)
        return data
    if request.method == 'PUT':
        data = put(request)
        return data
    else:
        return Response(status = 400, data="Metodo não permitido")


@api_view(['GET', 'DELETE'])
def mensagem_details(request, id):
    if request.method == 'GET':
        return get_all(id,request)
    if request.method == 'DELETE':
        return delete(id,request)


def get_all(id,request):
    valida = valida_token(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:

        return Response(status=400, data="Não autorizado")
    try:
        evento = Eventos.objects.get(pk=id, status=True)
        mensagens = Mensagem.objects.filter(eventoId=evento, status=True)

        if not mensagens:
            return Response(status=400, data="Nennhum dado encontrado!")

        serializer = MensagemSerializer(mensagens, many=True)
        return JSONResponse(serializer.data)
    except:
        return Response(status=400, data="Erro")

def post(request):
    valida = valida_token_user(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado!")
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        message = body['message']
        participantId = body['participantId']

        if not str(message).strip():
            return Response(status=400, data="Campo mensagem vazio!")

        pessoaEvento = PessoaEvento.objects.get(pk=participantId, status=True)
        evento = Eventos.objects.get(id = pessoaEvento.eventoId.pk,status = True)

        if pessoaEvento.userId.email == valida.user.username:
            mensagem = Mensagem.objects.create(messageDate=datetime.now(), message=message, participantId=pessoaEvento, eventoId=evento)
            return Response(status=200, data="Sucesso")
        else:
            return Response(status=400, data="Não autorizado!")
    except:
        return Response(status=400, data="Erro")

def put(request):
    valida = valida_token_user(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado!")
    try:

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        message = body['message']
        id = body['id']

        if not str(message).strip():
            return Response(status=400, data="Campo mensagem vazio!")

        mensagem = Mensagem.objects.get(pk=id, status=True)
        mensagem.message = message
        if mensagem.participantId.userId.email == valida.user.username:
            mensagem.save()

        else:
            return Response(status=400, data="Não autorizado!")

        serializer = MensagemSerializerPut(mensagem, many=False)
        return JSONResponse(serializer.data)

    except:
        return Response(status=400, data="Erro")

def delete(id,request):
    valida = valida_token_user(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado!")
    try:
        mensagem = Mensagem.objects.get(pk=id, status=True)
        if mensagem.participantId.userId.email == valida.user.username:
            mensagem.status = False
            mensagem.save()
            return Response(status=200, data="Sucesso")
        else:
            return Response(status=400, data="Não autorizado!")
    except:
        return Response(status=400, data="Erro")

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



