
from rest_framework.authtoken.models import Token

from api_eventos.models.eventos import Pessoa

#valida token
def valida_token(token):
    if token == None:
        return None
    try:
        validar = Token.objects.get(key=token)
        pessoa = Pessoa.objects.get(email = validar.user.username)
        if pessoa.status == 0:
            return False
        else:
            return True
    except:
        return False

#valida token e retorna o usuario
def valida_token_user(token):
    if token == None:
        return None
    try:
        token = Token.objects.get(key=token)
        pessoa = Pessoa.objects.get(email=token.user.username)
        if pessoa.status == 0:
            return False
        return token
    except:
        return False