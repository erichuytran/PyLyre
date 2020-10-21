from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, json

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SECRET_KEY"] = "IPI"

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("pylyre.sqlite")
    except sqlite3.Error as e:
        print(e)
    return conn


def chekUser(email, password):
    conn = db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        sql = """ SELECT * FROM users WHERE email=? AND password=?  """
        cursor = cur.execute(sql, (email, password))
        users = cursor.fetchall()

        if users:
            return "true"



        else:
            return "false"




@app.route('/', methods=['GET', 'POST'])
def index():
    conn = db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        if chekUser(email, password) == "true":
            sql = """ SELECT * FROM users WHERE email=? AND password=?  """
            cursor = cur.execute(sql, (email, password))
            users = cursor.fetchall()
            session["user"] = users[0]
            return render_template("index.html")
        else:
            return render_template("index.html", notexise="desole")
    else:
        return render_template("index.html")

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
        password_hash = generate_password_hash(password)
        sql = """ INSERT INTO users(first_name, last_name,pseudo, email, password)
                VALUES(?,?, ?, ?, ?)"""
        cursor = cur.execute(sql, (name, lastname, pseudo, email, password_hash))
        conn.commit()
        return f"USER: {cursor.lastrowid}", 201
    else:
        return render_template("signUp.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")
