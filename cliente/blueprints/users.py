
import functools

from flask import (Blueprint, flash, g, make_response, redirect,
                   render_template, request, session, url_for)

from util import api_urls
import requests
import json

__autor__ = "Leonardo Augusto Cavichia Cotovicz"

bp = Blueprint('user', __name__, url_prefix='/user')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/')
@login_required
def users():
    username = session.get('username')
    email = session.get('email')
    sex = session.get('sex')
    birthdate = session.get('birthdate')
    meu_token = session.get('token')

    return render_template('pages/index.html', username=username, sex=sex, birthdate=birthdate, email=email,
                           meu_token=meu_token)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        username = str(request.form['login'])
        password = str(request.form['senha'])

        logins = {'email': username, 'password': password}

        r = requests.post(api_urls.url_login, data=json.dumps(logins), headers=api_urls.headers)

        if r.status_code == 400:
            return render_template('auth/login.html', feedback="Não foi possivel fazer login: " + str(r.status_code))

        elif r.status_code == 200:
            r = r.json()
            session.clear()
            session['user_id'] = r['user']['id']
            session['username'] = r['user']['username']
            session['sex'] = r['user']['sex']
            session['email'] = r['user']['email']
            session['birthdate'] = r['user']['birthdate']
            session['token'] = r['token']
            session['password'] = password
            return redirect(url_for('user.users'))

        else:
            return render_template('auth/login.html', feedback="Status code não esperado: " + str(r.status_code))

    return render_template('auth/login.html', feedback="")


@bp.route('/deletar', methods=('GET', 'POST'))
def deletar():
    try:
        username = session.get('username')
        email = session.get('email')
        sex = session.get('sex')
        birthdate = session.get('birthdate')
        meu_token = session.get('token')
        id = session['user_id']
    except:
        return redirect(url_for('user.login'))
    if request.method == 'GET':
        return render_template('auth/deletar.html', feedback="", username=username, sex=sex, birthdate=birthdate,
                               email=email,
                               meu_token=meu_token)
    if request.method == 'POST':
        headers = {'content-type': 'application/json', 'token': meu_token}

        r = requests.delete(api_urls.url_user + str(id), headers=headers)
        if r.status_code == 200:
            return redirect(url_for('user.login'))
        else:
            return render_template('auth/deletar.html', feedback="Status code não esperado: " + str(r.status_code),
                                   username=username, sex=sex, birthdate=birthdate, email=email,
                                   meu_token=meu_token)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':

        username = str(request.form['username'])
        password = str(request.form['password'])
        email = str(request.form['email'])
        birthdate = str(request.form['birthdate'])
        sexo = str(request.form['sexo'])

        birthdate = birthdate + "T00:00:00.000Z"

        dados = {'username': username,
                 'password': password,
                 'email': email,
                 'birthdate': birthdate,
                 'sex': sexo}

        headers = {'content-type': 'application/json'}

        r = requests.post(api_urls.url_user, data=json.dumps(dados), headers=headers)
        if r.status_code == 400:
            return render_template('auth/register.html',
                                   feedback=str(r.json()) + ": " + str(r.status_code))
        elif r.status_code == 200:
            return render_template('auth/register.html', feedback="Cadastrado com sucesso: " + str(r.status_code))
        else:
            return render_template('auth/register.html', feedback="Status code não esperado: " + str(r.status_code))

    return render_template('auth/register.html', feedback="Todos os campos devem ser preenchidos!")


@bp.route('/atualizar', methods=('GET', 'POST',))
@login_required
def atualizar():
    try:
        meu_token = session.get('token')
        headers = {'content-type': 'application/json', 'token': meu_token}
        id = session.get('user_id')
        usuario = requests.get(api_urls.url_user + str(id), headers=headers)
        if usuario.status_code != 200:
            return render_template('erros/erro.html', status=str(usuario.status_code), json=str(usuario.json()),
                                   solicitacao=api_urls.url_user + str(id))
        usuario = usuario.json()
        username = usuario['username']
        email = usuario['email']
        sex = usuario['sex']
        birthdate = usuario['birthdate']
        password = session.get('password')

    except:
        return redirect(url_for('user.login'))

    if request.method == 'GET':
        return render_template('auth/update.html', feedback="Digite todos os campos para atualizar!", username=username,
                               email=email, sex=sex, birthdate=birthdate, password=password, id=id)

    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        email = str(request.form['email'])
        birthdate = str(request.form['birthdate'])
        sex = str(request.form['sex'])

        dados = {'username': username,
                 'password': password,
                 'email': email,
                 'birthdate': birthdate,
                 'sex': sex,
                 'id': id
                 }

        headers = {'content-type': 'application/json', 'token': meu_token}

        r = requests.put(api_urls.url_user, data=json.dumps(dados), headers=headers)
        a = r.json()
        if r.status_code == 400:
            return render_template('auth/update.html',
                                   feedback="Não foi possivel alterar" + str(r.json()) + ": " + str(r.status_code),
                                   username=username,
                                   email=email, sex=sex, birthdate=birthdate, password=password, id=id)

        elif r.status_code == 200:
            session['user_id'] = a['id']
            session['username'] = a['username']
            session['sex'] = a['sex']
            session['email'] = a['email']
            session['birthdate'] = a['birthdate']
            session['password'] = password

            try:
                id = session.get('user_id')
                username = session.get('username')
                email = session.get('email')
                sex = session.get('sex')
                birthdate = session.get('birthdate')
                password = session.get('password')
                meu_token = session.get('token')
            except:
                return redirect(url_for('user.login'))
            return render_template('auth/update.html',
                                   feedback="Alterado com sucesso: " + str(r.json()) + ": " + str(r.status_code),
                                   username=username,
                                   email=email, sex=sex, birthdate=birthdate, password=password, id=id)
        else:
            return render_template('auth/update.html',
                                   feedback="Status code não esperado: " + str(r.json()) + ": " + str(r.status_code),
                                   username=username,
                                   email=email, sex=sex, birthdate=birthdate, password=password, id=id)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = user_id


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))
