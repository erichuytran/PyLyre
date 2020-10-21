from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__, template_folder='templates', static_folder='static')


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("pylyre.sqlite")
    except sqlite3.Error as e:
        print(e)
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    conn = db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form["name"]
        lastname = request.form["lastName"]
        pseudo = request.form["pseudo"]
        email = request.form["email"]
        password = request.form["password"]
        sql = """ INSERT INTO users(first_name, last_name,pseudo, email, password)
                VALUES(?,?, ?, ?, ?)"""
        cursor = cur.execute(sql, (name, lastname, pseudo, email, password))
        conn.commit()
        return f"USER: {cursor.lastrowid}", 201
    else:
        return render_template("signUp.html")
