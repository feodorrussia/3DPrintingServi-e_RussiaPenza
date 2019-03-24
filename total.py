from flask import Flask, url_for, session, redirect, render_template, request, jsonify, \
    make_response, \
    request
import os

app = Flask(__name__)
app.secret_key = 'any random string'
UPLOAD_FOLDER = "Загрузки"


@app.route('/')
@app.route('/index')
def index():
    return render_template('title.html', text1=open('text_init.txt').read())


@app.route('/lab')
def lab():
    return render_template('lab.html')


@app.route('/printers')
def printers():
    return render_template('printers.html')


@app.route('/PC')
def PC():
    return render_template('PC.html')


@app.route('/filament')
def filament():
    return render_template('filament.html', filament='Сайт на доработке')


@app.route('/staff')
def staff():
    return render_template('staff.html', staff='Сайт на доработке')


@app.route('/upload_file', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return render_template('upload_file.html', filament='Сайт на доработке')
    elif request.method == 'POST':
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        f = request.files['file']
        x = f.__repr__()
        tmp = f.read()
        n = open(UPLOAD_FOLDER + "/" + x[x.index("'") + 1:x.index("'", 15)], "wb")
        n.write(tmp)
        n.close()
        return "Ваш заказ ожидает обработки. <a href='/title'>Вернуться на главную</a>"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
