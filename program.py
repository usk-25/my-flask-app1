import sqlite3
from flask import Flask, render_template, request, g

app = Flask(__name__)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('my_flask_app1.db')
        return g.db


@app.route('/')
def index():

    # アプリケーション起動時になければテーブルを作成する。
    con = get_db()
    cur = con.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='todolist';")
    for row in cur:
        if row[0] == 0:
            cur.execute("CREATE TABLE todolist(ID INTEGER PRIMARY KEY AUTOINCREMENT, TODO STRING(255), LIMITDATE DATETIME, CREATED_AT DATETIME NOT NULL DEFAULT 'DATETIME.NOW', UPDATED_AT DATETIME NOT NULL DEFAULT 'DATETIME.NOW');")

    con.close()
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        toDo = request.form['toDoInput']
        limitDate = request.form['toDoDate']

        # DBコネクション
        con = get_db()

        # 登録処理
        sql = "INSERT INTO todolist(TODO, LIMITDATE, CREATED_AT, UPDATED_AT) VALUES('{}','{}',datetime('now', 'localtime'), datetime('now', 'localtime'));".format(
            toDo, limitDate)
        con.execute(sql)
        con.commit()

        # データの再読み込み
        cur = con.execute(
            "SELECT ID, TODO, LIMITDATE FROM todolist ORDER BY ID")
        data = cur.fetchall()
        con.close()

        return render_template('list.html', data=data)


@app.route('/list')
def list():
    con = get_db()
    cur = con.execute("SELECT ID, TODO, LIMITDATE FROM todolist ORDER BY ID")
    data = cur.fetchall()
    con.close()
    return render_template('list.html', data=data)


# @app.route('/list/<int:id>')
# def todo_delete(id):
#     return render_template('list.html')


# @app.route('/list/<int:id>/edit', methods=['POST'])
# def todo_edit(id):
#     return render_template('edit.html')

# @app.route('/edit')
# def add():
#     return render_template('edit.html')


if __name__ == '__main__':
    DEBUG = True
    app.run(host='localhost')
