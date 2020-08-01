from django.contrib import admin

from api_eventos.models.eventos import Pessoa,Mensagem,Eventos,EventoTipo,PessoaEvento


# Register your models here.

admin.site.register(Eventos)
admin.site.register(EventoTipo)
admin.site.register(Pessoa)
admin.site.register(PessoaEvento)
admin.site.register(Mensagem)

