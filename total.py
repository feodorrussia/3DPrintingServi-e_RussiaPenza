from flask import Flask, url_for, session, redirect, render_template, request, jsonify, \
    make_response, \
    request

app = Flask(__name__)
app.secret_key = 'any random string'


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
