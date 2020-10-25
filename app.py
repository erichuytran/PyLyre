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
        sqlGetPasswordHash = """ SELECT password FROM users WHERE email=? """
        try:
            cursor = cur.execute(sqlGetPasswordHash, (email,))
            passwordHash = cursor.fetchall()
            if check_password_hash(passwordHash[0][0], password) == True:
                sql = """ SELECT * FROM users WHERE email=? AND password=? """
                cursor = cur.execute(sql, (email, passwordHash[0][0]))
                users = cursor.fetchall()
                if users:
                    session["user"] = users[0]
                    return "true"
                else:
                    return "false"
            else:
                return "false"

        except IndexError as e:
            print(e)
            return "false"
        

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        print(password)
        if chekUser(email, password) == "true":
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
        password_hash = generate_password_hash(password, method='sha1', salt_length=8)

        try:
            sql = """ INSERT INTO users(first_name, last_name,pseudo, email, password)
                    VALUES(?,?, ?, ?, ?) """
            cursor = cur.execute(sql, (name, lastname, pseudo, email, password_hash))       
            conn.commit()     
        except sqlite3.Error as e:
            print(e)
            return render_template('signUpError.html')

        return f"USER: {cursor.lastrowid}", 201
    else:
        return render_template("signUp.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")
