import functools

from flask import (Blueprint, flash, g, make_response, redirect,
                   render_template, request, session, url_for)

from blueprints.users import login_required
from util import api_urls
import requests

import json

from util.api_urls import url_cadastrar_participant

__autor__ = "Leonardo Augusto Cavichia Cotovicz"

bp = Blueprint('event', __name__, url_prefix='/event')


@bp.route('/')
@login_required
def events():
    meu_token = session.get('token')
    user_id = session.get('user_id')
    headers = {'content-type': 'application/json', 'token': meu_token}
    r = requests.get(api_urls.url_events_all, headers=headers)
    eventos = r.json()
    print(r.json())
    if r.status_code != 200:
        return render_template('erros/erro.html', status=r.status_code, json=eventos,
                               solicitacao=api_urls.url_events_all)

    return render_template('events/events.html', userid=user_id, eventos=eventos)


@bp.route('/criar', methods=('GET', 'POST'))
@login_required
def events_created():
    meu_token = session.get('token')
    user_id = session.get('user_id')
    headers = {'content-type': 'application/json', 'token': meu_token}
    tipo_evento = requests.get(api_urls.url_event_type_all, headers=headers)
    tipo_evento = tipo_evento.json()

    if request.method == 'POST':

        title = str(request.form['title'])
        street = str(request.form['street'])
        neighborhood = str(request.form['neighborhood'])
        referencePoint = str(request.form['referencePoint'])
        description = str(request.form['description'])
        city = str(request.form['city'])
        startDate = str(request.form['startDate'])
        tipo_evento_name = str(request.form['tipo_evento'])
        endDate = str(request.form['endDate'])

        for p in tipo_evento:
            if p['name'] == tipo_evento_name:
                tipo_evento_name = p['id']

        endDate = endDate + ":39.281Z"
        startDate = startDate + ":39.281Z"

        dados = {
            "startDate": startDate,
            "endDate": endDate,
            "title": title,
            "street": street,
            "neighborhood": neighborhood,
            "city": city,
            "referencePoint": referencePoint,
            "description": description,
            "eventTypeId": tipo_evento_name,
            "ownerId": user_id,
            "status": True
        }

        r = requests.post(api_urls.url_events_all, data=json.dumps(dados), headers=headers)

        if r.status_code != 200:
            return render_template('erros/erro.html', status=r.status_code, json=r.json(),
                                   solicitacao=api_urls.url_events_all)
        else:
            return render_template('events/events_create.html', tipo_evento=tipo_evento,
                                   feedback="Cadastrado com sucesso")

    return render_template('events/events_create.html', tipo_evento=tipo_evento,
                           feedback="Todos os campos devem ser preenchidos")


@bp.route('/<int:evento_id>', methods=('GET', 'POST'))
@login_required
def event_details(evento_id):
    if request.method == "GET":
        try:
            meu_token = session.get('token')

            headers = {'content-type': 'application/json', 'token': meu_token}
            e = requests.get(api_urls.url_events_all + str(evento_id), headers=headers)
            eventos = e.json()
            user_id = session.get('user_id')
            cont = 0
            partipant_id = 0
            for participantes in eventos['participant']:
                headers = {'content-type': 'application/json', 'token': meu_token}
                try:
                    valida_participacao = requests.get(api_urls.url_participant + str(participantes['id']), headers=headers)
                    valida = valida_participacao.json()
                    if valida['userId'] == user_id:
                        partipant_id = participantes['id']
                        cont = cont + 1
                except:
                    pass

            if e.status_code != 200:
                return render_template('erros/erro.html', status=e.status_code, json=eventos,
                                       solicitacao=api_urls.url_events_all + str(evento_id))

            if "id" in eventos:
                m = requests.get(api_urls.url_mensagem_all + str(evento_id), headers=headers)

                mensagens = m.json()
                print(str(mensagens))
                return render_template('events/events_details.html', userid=user_id, partipant_id=partipant_id, cont=cont,
                                       e=eventos,
                                       m=mensagens)
            else:
                return render_template('erros/erro.html', status=e.status_code, json=eventos,
                                       solicitacao=api_urls.url_events_all + str(evento_id))
        except:
            return redirect(url_for('event.events'))

    if request.method == "POST":
        if request.form['action'] == 'Nova mensagem':
            meu_token = session.get('token')
            headers = {'content-type': 'application/json', 'token': meu_token}
            mensagem = request.form['mensagem']
            participante = request.form['participanteID']

            data_mensagem = {
                "message": str(mensagem),
                "participantId": participante
            }

            e = requests.post(api_urls.url_mensagem, data=json.dumps(data_mensagem), headers=headers)
            mensagem = e.json()

            if e.status_code != 200:
                return render_template('erros/erro.html', status=e.status_code, json=mensagem,
                                       solicitacao=api_urls.url_mensagem)
            else:
                return redirect(url_for('event.event_details', evento_id=evento_id))

    if request.form['action'] == 'Atualizar Mensagem':
        meu_token = session.get('token')
        headers = {'content-type': 'application/json', 'token': meu_token}
        mensagem = request.form['mensagem']
        mensagemid = request.form['mensagemid']

        data_mensagem = {
            "id": mensagemid,
            "message": mensagem
        }

        e = requests.put(api_urls.url_mensagem, data=json.dumps(data_mensagem), headers=headers)
        mensagem = e.json()

        if e.status_code != 200:
            return render_template('erros/erro.html', status=e.status_code, json=mensagem,
                                   solicitacao=api_urls.url_mensagem)
        else:
            return redirect(url_for('event.event_details', evento_id=evento_id))


@bp.route('participar/<int:evento_id>')
@login_required
def participar(evento_id):
    meu_token = session.get('token')
    print(meu_token)
    id = session.get('user_id')
    headers = {'content-type': 'application/json', 'token': meu_token}

    data = {
        "userId": id,
        "eventoId": evento_id
    }

    e = requests.post(url_cadastrar_participant, data=json.dumps(data), headers=headers)
    participacao = e.json()

    if e.status_code != 200:
        return render_template('erros/erro.html', status=e.status_code, json=participacao,
                               solicitacao=api_urls.url_events_all + str(evento_id))
    else:
        return redirect(url_for('event.event_details', evento_id=evento_id))


@bp.route('cancelar/<int:partipant>')
@login_required
def carcelar_participacao(partipant):
    meu_token = session.get('token')
    headers = {'content-type': 'application/json', 'token': meu_token}
    e = requests.delete(api_urls.url_cadastrar_participant + str(partipant), headers=headers)
    participacao = e.json()
    if e.status_code != 200:
        return render_template('erros/erro.html', status=e.status_code, json=participacao,
                               solicitacao=api_urls.url_cadastrar_participant + str(partipant))
    else:
        return redirect(url_for('event.events'))


@bp.route('deletarmensagem/<int:mensagem>')
@login_required
def deletar_mensagem(mensagem):
    meu_token = session.get('token')

    headers = {'content-type': 'application/json', 'token': meu_token}

    e = requests.delete(api_urls.url_mensagem + str(mensagem), headers=headers)
    mensagems = e.json()
    if e.status_code != 200:
        return render_template('erros/erro.html', status=e.status_code, json=mensagems,
                               solicitacao=api_urls.url_cadastrar_participant + str(mensagem))
    else:
        return redirect(url_for('event.events'))


@bp.route('event_deletar/<int:evento_id>')
@login_required
def event_deletar(evento_id):
    meu_token = session.get('token')
    print(meu_token)
    id = session.get('user_id')
    headers = {'content-type': 'application/json', 'token': meu_token}

    e = requests.delete(api_urls.url_events_all + str(evento_id), headers=headers)
    evento = e.json()

    if e.status_code != 200:
        return render_template('erros/erro.html', status=e.status_code, json=evento,
                               solicitacao=api_urls.url_events_all + str(evento_id))
    else:
        return redirect(url_for('event.events'))


@bp.route('atualizarevento/<int:evento_id>', methods=('GET', 'POST'))
@login_required
def atualizar_evento(evento_id):
    meu_token = session.get('token')
    headers = {'content-type': 'application/json', 'token': meu_token}
    evento = requests.get(api_urls.url_events_all + str(evento_id), headers=headers)
    if evento.status_code != 200:
        return render_template('erros/erro.html', status=evento.status_code, json=evento.json(),
                               solicitacao=api_urls.url_events_all + str(evento_id))
    evento = evento.json()

    title = evento['title']
    startDate = evento['startDate']
    street = evento['street']
    neighborhood = evento['neighborhood']
    city = evento['city']
    referencePoint = evento['referencePoint']
    description = evento['description']
    endDate = evento['endDate']

    meu_token = session.get('token')
    headers = {'content-type': 'application/json', 'token': meu_token}

    tipo_evento = requests.get(api_urls.url_event_type_all, headers=headers)
    tipo_evento = tipo_evento.json()

    if request.method == 'GET':
        return render_template('events/events_atualizar.html', feedback="Digite todos os campos", title=title,
                               startDate=startDate, street=street, neighborhood=neighborhood,
                               tipo_evento=tipo_evento, city=city, referencePoint=referencePoint,
                               description=description, endDate=endDate)

    if request.method == 'POST':

        title = request.form['title']
        street = request.form['street']
        neighborhood = request.form['neighborhood']
        referencePoint = request.form['referencePoint']
        description = request.form['description']
        city = str(request.form['city'])
        startDate = str(request.form['startDate'])
        tipo_evento_name = request.form['tipo_evento']
        endDate = str(request.form['endDate'])

        for p in tipo_evento:
            if p['name'] == tipo_evento_name:
                tipo_evento_name = p['id']

        print(tipo_evento_name)

        dados = {
            "startDate": startDate,
            "endDate": endDate,
            "title": title,
            "id": evento_id,
            "street": street,
            "neighborhood": neighborhood,
            "city": city,
            "referencePoint": referencePoint,
            "description": description,
            "eventTypeId": tipo_evento_name,
            "status": True
        }

        print(str(dados))
        evento = requests.put(api_urls.url_events_all, data=json.dumps(dados), headers=headers)
        if evento.status_code != 200:
            return render_template('erros/erro.html', status=evento.status_code, json=evento.json(),
                                   solicitacao=api_urls.url_events_all + str(evento_id))
        else:
            return redirect(url_for('event.events'))
