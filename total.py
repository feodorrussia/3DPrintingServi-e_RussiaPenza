from flask import Flask, url_for, session, redirect, render_template, request, jsonify, \
    make_response, \
    request
import os
from db import DB
from login import LoginForm
from user import UsersModel

db = DB()
app = Flask(__name__)
app.secret_key = 'any random string'
UPLOAD_FOLDER = "Загрузки"
UsersModel(db.get_connection()).init_table()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
            if exists[1] == 4:
                return redirect("/index_admin")
            return redirect("/index")
    return render_template('loginform.html', title='Авторизация', form=form)


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return render_template('title_out.html', text1=open('text_init.txt').read())
    return render_template('title_in.html', text1=open('text_init.txt').read(), username=session['username'])


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
        return render_template('upload_file.html', filament='Сайт на доработке',
                               text=open("Описание_заказа.txt").read() + "\n")
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('loginform.html', title='Зарегистрироваться', form=form)
    elif request.method == 'POST':
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        user_model.insert(user_name, password)
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/index")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
