from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

REGISTROS_DIR = os.path.join(app.static_folder, 'registros_ex')
REGISTROS_in_DIR = os.path.join(app.static_folder, 'registros_in')


@app.route('/registros_ex')
def listar_registros_ex():
    registros = []

    for filename in os.listdir(REGISTROS_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(REGISTROS_DIR, filename), 'r') as file:
                lines = file.readlines()
                user = lines[0].strip().split(': ')[1]
                model = lines[1].strip().split(': ')[1]
                sn = lines[2].strip().split(': ')[1]
                assigned_to = lines[-1].strip().split(': ')[1]

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
def listar_registros_in():
    registros = []

    for filename in os.listdir(REGISTROS_in_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(REGISTROS_in_DIR, filename), 'r') as file:
                lines = file.readlines()
                user = lines[0].strip().split(': ')[1]
                model = lines[1].strip().split(': ')[1]
                sn = lines[2].strip().split(': ')[1]
                assigned_to = lines[-1].strip().split(': ')[1]

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
def intro():
    return render_template('intro.html')


@app.route('/register_crm', methods=['GET', 'POST'])
def register_crm():
    if request.method == 'POST':
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


@app.route('/register_in_crm', methods=['GET', 'POST'])
def register_in_crm():
    if request.method == 'POST':
        user = request.form['user']
        model = request.form['model']
        sn = request.form['sn']
        description = request.form['description']
        assigned_to = request.form['assigned_to']

        crm_content = f"Usuário: {user}\nModelo: {model}\nSN: {sn}\nDescrição: {description}\nAtribuído Para: {assigned_to}"

        numero_crm = proximo_numero_crm_in()

        file_name = f"in-crm#{numero_crm}.txt"

        file_path = os.path.join(REGISTROS_in_DIR, file_name)

        with open(file_path, 'w') as file:
            file.write(crm_content)

        return redirect(url_for('intro'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
