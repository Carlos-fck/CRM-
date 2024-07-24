from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from collections import Counter
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('intro'))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


REGISTROS_DIR = os.path.join(app.static_folder, 'rex')
REGISTROS_in_DIR = os.path.join(app.static_folder, 'rin')

os.makedirs(REGISTROS_DIR, exist_ok=True)
os.makedirs(REGISTROS_in_DIR, exist_ok=True)


def contar_atendimentos():
    assigned_to_counts = Counter()

    # Contar em registros_ex
    for filename in os.listdir(REGISTROS_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(REGISTROS_DIR, filename), 'r') as file:
                lines = file.readlines()
                assigned_to = lines[-1].strip().split(': ')[1]
                assigned_to_counts[assigned_to] += 1

    # Contar em registros_in
    for filename in os.listdir(REGISTROS_in_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(REGISTROS_in_DIR, filename), 'r') as file:
                lines = file.readlines()
                assigned_to = lines[-1].strip().split(': ')[1]
                assigned_to_counts[assigned_to] += 1

    return assigned_to_counts


@app.route('/dados_atendimentos')
@login_required
def dados_atendimentos():
    atendimentos = contar_atendimentos()
    return jsonify(atendimentos)


@app.route('/registros_ex')
@login_required
def listar_registros_ex():
    registros = []

    for filename in os.listdir(REGISTROS_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(REGISTROS_DIR, filename), 'r') as file:
                lines = file.readlines()
                user = lines[0].strip().split(': ')[1]
                model = lines[1].strip().split(': ')[1]
                sn = lines[2].strip().split(': ')[1]
                assigned_to = lines[-2].strip().split(': ')[1]

                registro = {
                    'file': filename,
                    'user': user,
                    'model': model,
                    'sn': sn,
                    'assigned_to': assigned_to
                }
                registros.append(registro)

    return render_template('registros.html', registros=registros)

@app.route('/registros_in')
@login_required
def listar_registros_in():
    registros = []

    for filename in os.listdir(REGISTROS_in_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(REGISTROS_in_DIR, filename), 'r') as file:
                lines = file.readlines()
                user = lines[0].strip().split(': ')[1]
                model = lines[1].strip().split(': ')[1]
                sn = lines[2].strip().split(': ')[1]
                assigned_to = lines[-2].strip().split(': ')[1]

                registro = {
                    'file': filename,
                    'user': user,
                    'model': model,
                    'sn': sn,
                    'assigned_to': assigned_to
                }
                registros.append(registro)

    return render_template('registros.html', registros=registros)



@app.route('/detalhes/<filename>')
@login_required
def detalhes_crm(filename):
    file_path = os.path.join(REGISTROS_DIR, filename)
    detalhes = ''

    with open(file_path, 'r') as file:
        detalhes = file.read()

    return render_template('detalhes_crm.html', detalhes=detalhes)


def proximo_numero_crm_ex():
    """Função para determinar o próximo número de CRM a ser utilizado."""
    numero = 1
    while True:
        nome_arquivo = f"ex-crm#{numero}.txt"
        caminho_arquivo = os.path.join(REGISTROS_DIR, nome_arquivo)
        if not os.path.exists(caminho_arquivo):
            return numero
        numero += 1


def proximo_numero_crm_in():
    """Função para determinar o próximo número de CRM a ser utilizado."""
    numero = 1
    while True:
        nome_arquivo = f"in-crm#{numero}.txt"
        caminho_arquivo = os.path.join(REGISTROS_in_DIR, nome_arquivo)
        if not os.path.exists(caminho_arquivo):
            return numero
        numero += 1


@app.route('/')
@login_required
def intro():
    return render_template('intro.html')

"""
@app.route('/register_crm', methods=['GET', 'POST'])
@login_required
def register_crm():
    if request.method == 'POST':
        print("entrei errado")
        user = request.form['user']
        model = request.form['model']
        sn = request.form['sn']
        description = request.form['description']
        assigned_to = request.form['assigned_to']

        crm_content = f"Usuário: {user}\nModelo: {model}\nSN: {sn}\nDescrição: {description}\nAtribuído Para: {assigned_to}"

        numero_crm = proximo_numero_crm_ex()

        file_name = f"ex-crm#{numero_crm}.txt"

        file_path = os.path.join(REGISTROS_DIR, file_name)

        with open(file_path, 'w') as file:
            file.write(crm_content)

        return redirect(url_for('intro'))

    return render_template('index.html')
"""
#parei aq
def registro_teste():
    filenamet = f"crm teste"
    filepath = os.path.join(REGISTROS_in_DIR, filenamet)
    with open(filepath, 'w') as file:
        file.write(crm_content1)
#parei aq



@app.route('/in', methods=['GET', 'POST'])
@login_required
def register_in_crm():
    print('a')
    if request.method == 'POST':
        print("post da funcao in")
        user = request.form['user']
        model = request.form['model']
        sn = request.form['sn']
        description = request.form['description']
        assigned_to = request.form['assigned_to']

        crm_content1 = f"Usuário: {user}\nModelo: {model}\nSN: {sn}\nDescrição: {description}\nAtribuído Para: {assigned_to}"
        print(crm_content1)
        numero_crm1 = proximo_numero_crm_in()

        file_name = f"in-crm#{numero_crm1}.txt"

        file_path = os.path.join(REGISTROS_in_DIR, file_name)

        with open(file_path, 'w') as file:
            file.write(crm_content1)

        return redirect(url_for('intro'))

    return render_template('index_in.html')


@app.route('/grafico')
@login_required
def grafico():
    return render_template('grafico.html')


if __name__ == '__main__':
    app.run(debug=True)
