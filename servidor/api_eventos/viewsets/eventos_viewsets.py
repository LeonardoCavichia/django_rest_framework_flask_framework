import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from datetime import date, datetime
import datetime as DT
from api_eventos.models.eventos import Eventos, EventoTipo, Pessoa
from api_eventos.serializers.eventos_serializers import EventosSerializer
from api_eventos.viewsets.AuthEvento import valida_token, valida_token_user


@api_view(['GET', 'POST', 'PUT'])
def events_view(request):
    if request.method == 'POST':
        data = post(request)
        return data

    if request.method == 'GET':
        data = get_all(request)
        return data

    if request.method == 'PUT':
        data = put(request)
        return data
    else:
        return Response(status=400, data="Erro")


@api_view(['GET', 'DELETE'])
def event_details(request, id):
    if request.method == 'GET':
        return get(id, request)
    if request.method == 'DELETE':
        return delete(id, request)


def post(request):
    valida = valida_token_user(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        title = body['title']
        startDate = body['startDate']
        endDate = body['endDate']
        street = body['street']
        neighborhood = body['neighborhood']
        city = body['city']
        referencePoint = body['referencePoint']
        description = body['description']
        eventTypeId = body['eventTypeId']


        if str(title).strip() == "" or str(startDate).strip() == "" or str(endDate).strip() == "" or str(
                street).strip() == "" or str(city).strip() == "" or str(neighborhood).strip() == "":
            return Response(status=400, data="Erro!")

        eventotipo = EventoTipo.objects.get(id=eventTypeId)
        pessoa = Pessoa.objects.get(email=valida.user.username, status=True)

        Eventos.objects.create(title=title, startDate=startDate, endDate=endDate, street=street,
                                         neighborhood=neighborhood, city=city, referencePoint=referencePoint,
                                         description=description, eventType=eventotipo, status=True, user=pessoa)

        return Response(status=200, data="Sucesso")
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

        id = body['id']
        title = body['title']
        startDate = body['startDate']
        endDate = body['endDate']
        street = body['street']
        neighborhood = body['neighborhood']
        city = body['city']
        referencePoint = body['referencePoint']
        description = body['description']
        eventTypeId = body['eventTypeId']

        if str(title).strip() == "" or str(startDate).strip() == "" or str(endDate).strip() == "" or str(
                street).strip() == "" or str(city).strip() == "" or str(neighborhood).strip() == "":
            return Response(status=400, data="Erro!")

        evento = Eventos.objects.get(id=id, status=True)

        evento.city = city
        evento.title = title
        evento.startDate = startDate
        evento.endDate = endDate
        evento.street = street
        evento.referencePoint = referencePoint
        evento.neighborhood = neighborhood
        evento.description = description

        evento_tipo = EventoTipo.objects.get(id=eventTypeId)
        evento.eventType = evento_tipo

        if evento.user.email == valida.user.username:
            evento.save()
            serializer = EventosSerializer(evento, many=False)
            response = JSONResponse(serializer.data)
            return response
        else:
            return Response(status=400, data="Não autorizado!")
    except:
        return Response(status=400, data="Erro")


@api_view(['GET'])
def search_event_viewset(request):
    valida = valida_token(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")
    busca = request.query_params
    evento = Eventos.objects.filter(status=True)
    try:
        if "event_type" in busca and "start_date" in busca and "end_date" in busca:

            evento = evento.filter(eventType=busca['event_type'],
                                   startDate__range=(busca['start_date'], busca['end_date']))

        elif "event_type" not in busca and "start_date" in busca and "end_date" in busca:

            evento = evento.filter(startDate__range=(busca['start_date'], busca['end_date']))

        elif "event_type" in busca and "start_date" not in busca and "end_date" not in busca and "rdate" not in busca:
            evento = evento.filter(eventType=busca['event_type'])

        else:
            return Response(status=400, data="Filtros incorretos")

        serializer = EventosSerializer(evento, many=True)
        response = JSONResponse(serializer.data)
        return response
    except:
        return Response(status=400, data="Erro")


def get(id, request):
    valida = valida_token(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")
    try:
        evento = Eventos.objects.get(pk=id, status=True)
    except:
        return Response(status=400, data="Erro")
    serializer = EventosSerializer(evento, many=False)
    response = JSONResponse(serializer.data)
    return response


def get_all(request):
    valida = valida_token(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")
    try:
        evento = Eventos.objects.all()
    except:
        return Response(status=400, data="Erro")
    serializer = EventosSerializer(evento, many=True)
    response = JSONResponse(serializer.data)
    return response


def delete(id, request):
    valida = valida_token_user(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado!")
    try:
        evento = Eventos.objects.get(pk=id, status=True)
        if evento.user.email == valida.user.username:
            evento.status = False
            evento.save()
            return Response(status=200, data="Desativado com sucesso!")
        else:
            return Response(status=400, data="Não autorizado!")
    except:
        return Response(status=400, data="Erro!")


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
