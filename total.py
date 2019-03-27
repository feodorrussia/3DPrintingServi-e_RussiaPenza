from flask import Flask, url_for, session, redirect, render_template, request, jsonify, \
    make_response, \
    request
import os
from db import DB
from login import LoginForm
from user import UsersModel
from orders import OrdersModel
from chat import ChatModel
from delivery import DeliveryModel
import datetime
from json import load

db = DB()
app = Flask(__name__)
app.secret_key = 'any random string'
UPLOAD_FOLDER = "Загрузки"
UsersModel(db.get_connection()).init_table()
OrdersModel(db.get_connection()).init_table()
ChatModel(db.get_connection()).init_table()
DeliveryModel(db.get_connection()).init_table()
delivery = {'Курьером(по г.Пенза)': 1, 'Почта России': 2, 'DPD': 3}


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
            global i
            i = False
            if exists[1] == 1:
                return redirect("/title_admin")
            return redirect("/title")
    return render_template('loginform.html', title='Авторизация', form=form)


i = True


@app.route('/')
@app.route('/title')
def title():
    global i
    if 'username' not in session or i:
        return render_template('title_out.html', text1=open('text_init.txt').read())
    if session['user_id'] == 1:
        return redirect("/title_admin")
    return render_template('title_in.html', text1=open('text_init.txt').read(),
                           username=session['username'])


@app.route('/out')
def out():
    global i
    i = True
    return render_template('title_out.html', text1=open('text_init.txt').read())


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
    return render_template('filament.html', filament=load(open('filament.json')))


@app.route('/staff')
def staff():
    return render_template('staff.html', staff='Сайт на доработке')


@app.route('/upload_file', methods=['POST', 'GET'])
def sample_file_upload():
    global i
    if 'username' not in session or i:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('upload_file.html', text=open("Описание_заказа.txt").read() + "\n")
    elif request.method == 'POST':
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        name = request.form.get('order')
        t = request.form.get('about')
        f = request.files['file']
        x = f.__repr__()
        tmp = f.read()
        FILE_NAME = x[x.index("'") + 1:x.index("'", 15)]
        n = open(UPLOAD_FOLDER + "/" + FILE_NAME, "wb")
        n.write(tmp)
        n.close()
        order_model = OrdersModel(db.get_connection())
        order_model.insert(name, t, FILE_NAME, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                           session['user_id'], 'Заказ на обработке', 1)
        return redirect("/title")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    global i
    i = False
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
        return redirect("/title")


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route("/myorders")
def myorders():
    orders = OrdersModel(db.get_connection()).get(session['user_id'])
    return render_template('myorders.html', username=session['username'],
                           news=sorted(orders, key=(lambda x: x[0]), reverse=True))


@app.route('/delete_order/<int:news_id>', methods=['GET'])
def delete_order(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = OrdersModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/myorders")


@app.route("/chat/<int:id_user2>", methods=['GET', 'POST'])
def chat(id_user2):
    if request.method == 'GET':
        chat = ChatModel(db.get_connection()).get_all(session['user_id'], id_user2)
        chat += ChatModel(db.get_connection()).get_all(id_user2, session['user_id'])
        chat = sorted(chat, key=lambda x: x[0], reverse=True)
        if session['user_id'] == 1:
            orders = OrdersModel(db.get_connection()).get_all()
        else:
            orders = OrdersModel(db.get_connection()).get(session['user_id'])
        return render_template('chat.html', username=session['username'],
                               message=chat, user_id=session['user_id'], orders=orders)
    elif request.method == 'POST':
        message = request.form['message']
        order_name = request.form.get('order')
        chat_model = ChatModel(db.get_connection())
        chat_model.insert(session['user_id'], message, order_name, id_user2)
        return redirect(f"/chat/{str(id_user2)}")


@app.route("/order/<int:item>")
def order(item):
    orders = OrdersModel(db.get_connection())
    delivery = DeliveryModel(db.get_connection()).get(item)
    return render_template('order.html', item=orders.get_order(item), delivery=delivery)


@app.route('/title_admin')
def title_admin():
    return render_template('title_admin.html', username=session['username'])


@app.route('/processed_orders')
def processed_orders():
    orders1 = OrdersModel(db.get_connection()).get_status(1)
    orders = []
    for i in orders1:
        z = []
        user = UsersModel(db.get_connection()).get(i[7])
        z.append(user[1])
        z.append(user[0])
        z.append(i[1])
        z.append(i[6])
        z.append(i[0])
        orders.append(z)
    return render_template('processed_orders.html', username=session['username'], orders=sorted(orders, key=(lambda x: x[4]), reverse=True))


@app.route('/delivery_orders')
def delivery_orders():
    orders1 = OrdersModel(db.get_connection()).get_status(2)
    orders = []
    for i in orders1:
        z = []
        user = UsersModel(db.get_connection()).get(i[7])
        z.append(user[1])
        z.append(user[0])
        z.append(i[1])
        z.append(i[6])
        z.append(i[0])
        orders.append(z)
    return render_template('delivery_orders.html', username=session['username'],
                           orders=sorted(orders, key=(lambda x: x[4]), reverse=True))


@app.route("/sending/<int:order_id>", methods=['GET', 'POST'])
def sending(order_id):
    if request.method == 'GET':
        order = OrdersModel(db.get_connection()).get_order(order_id)
        return render_template('sending.html', username=session['username'], order=order)
    elif request.method == 'POST':
        global delivery
        order1 = OrdersModel(db.get_connection())
        order = OrdersModel(db.get_connection()).get_order(order_id)
        type = request.form['type']
        cod_type = delivery[type]
        cod = request.form.get('cod')
        price = request.form['price']
        delivery_model = DeliveryModel(db.get_connection())
        order1.update(2, 'Доставка заказа', order_id)
        delivery_model.insert(type, cod_type, cod, order[0], order[1], price, order[6])
        return redirect("/title_admin")


@app.route("/parsed/<int:order_id>")
def parsed(order_id):
    orders = OrdersModel(db.get_connection())
    orders.update(3, 'Заказ доставлен', order_id)
    return redirect("/myorders")


@app.route("/parsed_orders")
def parsed_orders():
    orders = OrdersModel(db.get_connection())
    row = orders.get_status(3)
    return render_template("parsed_orders.html", row=row)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
