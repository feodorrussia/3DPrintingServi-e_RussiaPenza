from flask import *
from db import *
from news import NewsModel
from user import UsersModel

db = DB()
app = Flask(__name__)
app.secret_key = 'subscribe to pewdiepie'


@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        if 'username' not in session:
            return redirect('/login')
        news = NewsModel(db.get_connection()).get_all(session['user_id'])
        return render_template('index.html', username=session['username'],
                               news=sorted(news, key=(lambda x: x[1].lower())))
    elif request.method == 'POST':
        print(request.form.get(""))

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
