import json
from datetime import datetime

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, action

from api_eventos.serializers.pessoa_evento_serializers import ParticipanteSerializer
from api_eventos.serializers.user_serializer import PessoaSerializer
from api_eventos.viewsets.AuthEvento import valida_token, valida_token_user
from ..models.eventos import Pessoa, PessoaEvento, Eventos, Mensagem


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def participant_view(request):

    if request.method == 'POST':
        data = post(request)
        return data

    if request.method == 'GET':
        pass
        #data = get_all()
        #return HttpResponse(data, content_type='application/json')

    if request.method == 'PUT':
        pass
        #data = put(request)
        #return data
    else:
        return Response(status=400, data="Metodo não permitido")

@api_view(['GET', 'DELETE'])
def participant_details(request, id):
    if request.method == 'GET':
        return get(id,request)
    if request.method == 'DELETE':
        return delete(id,request)

def post(request):
    valida = valida_token(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        userId = body['userId']
        eventoId = body['eventoId']
        user = Pessoa.objects.get(pk=userId, status = True)
        evento = Eventos.objects.get(pk=eventoId, status=True)
        valida_participante = PessoaEvento.objects.filter(userId=user, eventoId=evento, status=True)

        if valida_participante:
            return Response(status=400, data="Participante já cadastrado, neste evento!")

        PessoaEvento.objects.create(registrationDate=datetime.now(), eventoId=evento, userId=user)

        return Response(status=200, data="Sucesso")
    except:
        return Response(status=400, data="Erro")


def delete(id,request):
    valida = valida_token_user(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado!")
    try:
        pessoaevento = PessoaEvento.objects.get(pk=id, status=True)
        if pessoaevento.userId.email == valida.user.username:
            pessoaevento.status = False
            mensagem = Mensagem.objects.filter(participantId=pessoaevento)
            for m in mensagem:
                m.status = False
                m.save()
            pessoaevento.save()
            return Response(status=200, data="Sucesso")
        else:
            return Response(status=400, data="Não autorizado!")
    except:
        return Response(status=400, data="Erro")

def get(id,request):
    valida = valida_token(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")
    try:
        participante = PessoaEvento.objects.get(pk=id, status=True)
    except:
        return Response(status=400, data="Erro")

    serializer = ParticipanteSerializer(participante, many=False)
    response = JSONResponse(serializer.data)
    return response



class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)