import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api_eventos.serializers.user_serializer import PessoaSerializer
from api_eventos.viewsets.AuthEvento import valida_token, valida_token_user
from ..models.eventos import Pessoa

@api_view(['GET', 'POST', 'PUT'])
def user_view(request):
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
        return Response(status=400, data="Metodo não permitido")

@api_view(['GET', 'DELETE'])
def user_details(request, id):
    valida = valida_token(request.META.get('HTTP_TOKEN'))
    print(request.META)
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")

    if request.method == 'GET':
        return get(id, request)
    if request.method == 'DELETE':
        return delete(id,request)


@api_view(['POST'])
def user_login(request):

    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']

        try:
            pessoa = Pessoa.objects.get(email=email, password=password)
            if pessoa.status == 0:
                return Response(status=400, data="Não foi possivel fazer o login")
            token, created = Token.objects.get_or_create(user=pessoa.user)

            data = ({
                'token': token.key,
                'user':{
                    'id': pessoa.pk,
                    'email': pessoa.email,
                    'username':pessoa.username,
                    'sex':pessoa.sex,
                    'birthdate':pessoa.birthdate}
            })

            response = JSONResponse(data)
            return response
        except:
            return Response(status=400, data="Não foi possivel fazer o login")
    except:
        return Response(status=400, data="Entrada Invalida")

def get_all(request):
    valida = valida_token(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")
    pessoas = Pessoa.objects.filter(status=True)
    serializer = PessoaSerializer(pessoas, many=True)
    return JSONResponse(serializer.data)

def get(id,request):
    valida = valida_token(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado")
    try:

        pessoa = Pessoa.objects.get(pk=id, status=1)
    except:
        return Response(status=400, data="Usuário não encontrado!")

    serializer = PessoaSerializer(pessoa, many=False)
    response = JSONResponse(serializer.data)
    return response

def post(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = str(body['username'])
        password = str(body['password'])
        birthdate = body['birthdate']
        email = str(body['email'])
        sex = str(body['sex'])
        print(username+password+birthdate+email+sex)

        if sex == 'M' or sex == 'm':
            sex = 'M'
        elif sex == 'F' or sex == 'f':
            sex = 'F'
        else:
            return Response(status=400, data="Erro: sex não conforme!")

        if str(username).strip() == "" or str(password).strip() == "" or str(email).strip() == "" or str(birthdate).strip() == "":
            return Response(status=400, data="A entrada possui campos vazios!")

        valida_user = Pessoa.objects.filter(email=email)

        if valida_user:
            return Response(status=400, data="Email já cadastrado")
        else:

            user = User.objects.create(username=email)
            pessoa = Pessoa.objects.create(user=user, username=username, password=password, birthdate=birthdate, email=email,
                                           sex=sex)
            user.set_password(password)
            user.save()
            serializer = PessoaSerializer(pessoa, many=False)
            return JSONResponse(serializer.data, status=200)
    except:
        return Response(status=400, data="Entrada Invalida")


def put(request):
    valida = valida_token_user(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Não autorizado!")
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['username']
        password = body['password']
        birthdate = body['birthdate']
        email = body['email']
        sex = body['sex']

        if sex == 'M' or sex == 'm':
            sex = 'M'
        elif sex == 'F' or sex == 'f':
            sex = 'F'
        else:
            return Response(status=400, data="Campo sex não conforme!")

        if str(username).strip() == "" or str(password).strip() == "" or str(email).strip() == "" or str(birthdate).strip() == "":
            return Response(status=400, data="A entrada possui campos vazios!")

        try:
            pessoa = Pessoa.objects.get(email=valida.user.username)
            if (pessoa.status == 0):
                return Response(status=400, data="Usuario não encontrado")

        except:
            return Response(status=400, data="Usuario não encontrado")

        pessoa.email = email
        pessoa.birthdate = birthdate
        pessoa.password = password
        pessoa.sex = sex
        pessoa.username = username

        valida_email = Pessoa.objects.filter(email=email).exclude(email=valida.user.username)


        if valida_email:
            return Response(status=400, data="Email já cadastrado")
        else:
            valida.user.username = pessoa.email
            valida.user.set_password(pessoa.password)
            valida.user.save()
            pessoa.save()
            serializer = PessoaSerializer(pessoa, many=False)
            return JSONResponse(serializer.data, status=200)


    except:
        return Response(status=400, data="Entrada Invalida")


def delete(id, request):
    valida = valida_token_user(request.META.get('HTTP_TOKEN'))
    if valida == None:
        return Response(status=400, data="Token fornecido incorretamente!")
    if valida == False:
        return Response(status=400, data="Token invalido!")
    try:
        pessoa = Pessoa.objects.get(pk=id, status=1)
        if pessoa.email == valida.user.username:
            pessoa.status = 0
            pessoa.save()
            return Response(status=200, data="Desativado com sucesso!")
        else:
            return Response(status=400, data="Não autorizado!")
    except:
        return Response(status=400, data="Usuário não encontrado!")


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
