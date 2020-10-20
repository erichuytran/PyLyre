from flask import Flask , render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("pylyre.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/add', methods=['GET', 'POST'])
def add():
    conn = db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form["name"]
        lastname = request.form["lastname"]
        pseudo = request.form["pseudo"]
        email = request.form["email"]
        password = request.form["password"]
        sql = """ INSERT INTO users(first_name, last_name,pseudo, email, password)
                VALUES(?,?, ?, ?, ?)"""
        cursor = cur.execute(sql, (name, lastname, pseudo, email, password))
        conn.commit()
        return f"USER: {cursor.lastrowid}", 201
    else:
        return render_template("add.html")
