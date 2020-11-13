from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, json

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SECRET_KEY"] = "IPI"

def isLoggedIn():
    if not session:
        print("SESSION : EMPTY, REDIRECTION")
        return False
    else:
        return True

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
        if chekUser(email, password) == "true":
            return render_template("main_page.html")
        else:
            return render_template("index.html", failedLogin=True)
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
            cur.execute(sql, (name, lastname, pseudo, email, password_hash))       
            conn.commit()     
        except sqlite3.Error as e:
            print(e)
            return render_template("signUp.html", auth=False)

        return render_template("account_created.html")
    else:
        return render_template("signUp.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")

@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if isLoggedIn() == False:
        return redirect("/")

    return render_template("main_page.html")


@app.route('/albums_page/<int:id_artist>', methods=['GET', 'POST'])
def albums_page(id_artist):
    if isLoggedIn() == False:
        return redirect("/")

    conn = db_connection()
    cur = conn.cursor()

    if id_artist == 0:
        sql = """ SELECT * FROM albums """
        cursor = cur.execute(sql)
        album = cursor.fetchall()
        return render_template("albums_page.html", albums=album)
    else:
        sql = """ SELECT * FROM albums WHERE id_artist = ? """
        cursor = cur.execute(sql, (id_artist,))
        album = cursor.fetchall()
        return render_template("albums_page.html", albums=album)

@app.route('/album_selected/<int:albumId>', methods=['GET', 'POST'])
def album_selected(albumId):
    if isLoggedIn() == False:
        return redirect("/")

    conn = db_connection()
    cur = conn.cursor()
    sqlTracks = """ SELECT * FROM tracks INNER JOIN artists ON tracks.id_artist = artists.id INNER JOIN albums ON tracks.id_album = albums.id WHERE id_album = ? """

    # get tracks
    cursor = cur.execute(sqlTracks, (albumId,))
    track = cursor.fetchall()
    
    # get album cover
    sqlAlbumCover = """ SELECT path_img FROM albums WHERE id = ? """
    cursor = cur.execute(sqlAlbumCover, (albumId,))
    albumCover = cursor.fetchone()
    return render_template("album_selected.html", tracks=track, albumCoverArt=albumCover)


@app.route('/tracks_page', methods=['GET', 'POST'])
def tracks_page():
    if isLoggedIn() == False:
        return redirect("/")

    liked = request.args.get('liked', False)

    conn = db_connection()
    cur = conn.cursor()
    id_user = session["user"][0]

    if liked == False:
        sql = """ SELECT * FROM tracks INNER JOIN artists ON tracks.id_artist = artists.id INNER JOIN albums ON tracks.id_album = albums.id """
        cursor = cur.execute(sql)
        track = cursor.fetchall()
        return render_template("tracks_page.html", tracks=track, likePage=False)
    else:
        sql = """ SELECT * FROM tracks INNER JOIN artists ON tracks.id_artist = artists.id INNER JOIN albums ON tracks.id_album = albums.id INNER JOIN tracks_liked ON tracks.id = tracks_liked.id_track WHERE id_user = ? """
        cursor = cur.execute(sql, (id_user,))
        track = cursor.fetchall()
        return render_template("tracks_page.html", tracks=track, likePage=True)
      

@app.route('/artists_page', methods=['GET', 'POST'])
def artists_page():
    if isLoggedIn() == False:
        return redirect("/")

    liked = request.args.get('liked', False)

    conn = db_connection()
    cur = conn.cursor()
    if liked == False:
        sql = """ SELECT * FROM artists """
    else:
        sql = """  """

    sql = """ SELECT * FROM artists """
    cursor = cur.execute(sql)
    artist = cursor.fetchall()
    return render_template("artists_page.html", artists=artist)

@app.route('/favtrack/<int:id>', methods=['GET', 'POST'])
def add_favtrack(id):
    if isLoggedIn() == False:
        return redirect("/")

    conn = db_connection()
    cur = conn.cursor()

    id_track = id
    id_user = session["user"][0]
 
    trackInfoSql = """ SELECT title FROM tracks WHERE id = ? """

    sqlAdd = """ INSERT INTO tracks_liked(id_user, id_track)
                    VALUES(?,?) """
    sqlCheck = """ SELECT id FROM tracks_liked WHERE id_user = ? AND id_track = ? """
    sqlDelete = """ DELETE FROM tracks_liked WHERE id = ? """


    sqlTracks = """ SELECT * FROM tracks INNER JOIN artists ON tracks.id_artist = artists.id INNER JOIN albums ON tracks.id_album = albums.id """
    cursorTracks = cur.execute(sqlTracks)
    tracks = cursorTracks.fetchall()

    #Requests if the track is already liked
    cursor = cur.execute(sqlCheck, (id_user, id_track))

    #res countains the id value of the selected row (already liked track)
    res = cursor.fetchall()

    cursorTrackInfo = cur.execute(trackInfoSql, (id_track,))
    trackInfo = cursorTrackInfo.fetchall()
    
    if not res:
        cur.execute(sqlAdd, (id_user, id_track))
        conn.commit()
        return render_template(("tracks_page.html"), track=tracks, trackName=trackInfo, isAdded=True)
    else:
        cur.execute(sqlDelete, (res[0][0],))
        conn.commit()
        return render_template(("tracks_page.html"), track=tracks, trackName=trackInfo, isAdded=False)

