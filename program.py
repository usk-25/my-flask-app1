from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        req1 = request.form['toDoInput']
        req2 = request.form['toDoDate']
        return f'POST受け取りました: {req1} {req2}'


@app.route('/list', methods=['GET', 'POST'])
def list():
    if request.method == 'GET':
        return render_template('list.html')


# @app.route('/edit')
# def add():
#     return render_template('edit.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
