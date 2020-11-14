from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3, json

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SECRET_KEY"] = "IPI"

def isLoggedIn():
    if not session:
        print("SESSION : EMPTY, REDIRECTION")
        return False
    else:
        return True

# fonction de connection à la bdd
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("pylyre.sqlite")
    except sqlite3.Error as e:
        print(e)
    return conn

# fonction permettant de regarder si un utilisateur est déjà présent dans la bdd affin d'éviter les doublons
def chekUser(email, password):
    conn = db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        # récupération du mot de passe
        sqlGetPasswordHash = """ SELECT password FROM users WHERE email=? """
        try:
            cursor = cur.execute(sqlGetPasswordHash, (email,))
            passwordHash = cursor.fetchall()
            if check_password_hash(passwordHash[0][0], password) == True:
                # le mot de passe donné correspond à celui de l'utilisateur :
                sql = """ SELECT * FROM users WHERE email=? AND password=? """
                cursor = cur.execute(sql, (email, passwordHash[0][0]))
                users = cursor.fetchall()
                if users:
                    # création d'une session
                    session["user"] = users[0]
                    return "true"
                else:
                    return "false"
            else:
                return "false"

        except IndexError as e:
            print(e)
            return "false"
        
# page d'accueil
@app.route('/', methods=['GET', 'POST'])
def index():
    # action si l'utilisateur à appuyé sur le bouton de connection
    if request.method == 'POST':
        # récupération des champs du formulaire
        email = request.form["email"]
        password = request.form["password"]
        if chekUser(email, password) == "true":
            # si l'utilisateur s'est connecté avec succès, on affiche main_page
            return render_template("main_page.html")
        else:
            # si non, on redirige vers la page d'accueil et on affiche un message d'erreur
            return render_template("index.html", failedLogin=True)
    else:
        return render_template("index.html")

# page d'inscription
@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    conn = db_connection()
    cur = conn.cursor()

    # actions si l'utilisateur à soumis le formulaire d'inscription
    if request.method == 'POST':
        # récupération des champs du formulaire
        name = request.form["name"]
        lastname = request.form["lastName"]
        pseudo = request.form["pseudo"]
        email = request.form["email"]
        password = request.form["password"]
        # génération du mot de passe crypté
        password_hash = generate_password_hash(password, method='sha1', salt_length=8)

        try:
            # mise à jour de la bdd avec les données d'inscription du nouvel utilisateur
            sql = """ INSERT INTO users(first_name, last_name,pseudo, email, password)
                    VALUES(?,?, ?, ?, ?) """
            cur.execute(sql, (name, lastname, pseudo, email, password_hash))       
            conn.commit() 

        # gestion d'erreur
        except sqlite3.Error as e:
            print(e)
            # redirection vers la page d'inscription avec affichage d'un message d'échec d'inscription
            return render_template("signUp.html", auth=False)

        # affichage d'une page de confirmation d'inscription
        return render_template("account_created.html")
    else:
        return render_template("signUp.html")

# route de déconnexion
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    conn = db_connection()
    cur = conn.cursor()
    id_user = session["user"][0]
    date = datetime.utcnow()

    sql = """ UPDATE users  SET date_last_login = ?  WHERE id = ? """

    cur.execute(sql, (date, id_user))
    conn.commit()
    session.clear()
    #redirection vers la page d'accueil après la déconnexion
    return redirect("/")

# page principale
@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    # check de l'etat de connection de l'utilisateur
    if isLoggedIn() == False:
        return redirect("/")
        
    conn = db_connection()
    cur = conn.cursor()
    id_user = session["user"][0]

    trakLike = """  SELECT id_track  FROM tracks_liked  WHERE id_user = ? """
    curLikeTrak = cur.execute(trakLike, (id_user,))
    TrackLikes = [item[0] for item in curLikeTrak.fetchall()]

    dateTrack = """ SELECT * FROM tracks INNER JOIN artists ON tracks.id_artist = artists.id INNER JOIN albums ON tracks.id_album = albums.id """
    cursor = cur.execute(dateTrack )
    dateTracks = cursor.fetchall()

    dateConne = """ SELECT * FROM users WHERE id = ? """
    cursorDateConn = cur.execute(dateConne, (id_user,))
    dateC = cursorDateConn.fetchall()

    return render_template("main_page.html", dateC=dateC, dateTracks=dateTracks, TrackLikes=TrackLikes, id_user=id_user)

# page de selection d'albums
@app.route('/albums_page/<int:id_artist>', methods=['GET', 'POST'])
def albums_page(id_artist):
    # check de l'etat de connection de l'utilisateur
    if isLoggedIn() == False:
        return redirect("/")

    conn = db_connection()
    cur = conn.cursor()

    # si id_artist = 0, cela veut dire qu'aucun artiste n'a été selectionné. On affiche alors tous les albums.
    if id_artist == 0:
        sql = """ SELECT * FROM albums """
        cursor = cur.execute(sql)
        album = cursor.fetchall()
        return render_template("albums_page.html", albums=album)

    # si non, on affiche les albums de l'artiste séléctionné (dépend de artists_page)
    else:
        sql = """ SELECT * FROM albums WHERE id_artist = ? """
        cursor = cur.execute(sql, (id_artist,))
        album = cursor.fetchall()
        return render_template("albums_page.html", albums=album)

# page d'album selectionné
@app.route('/album_selected/<int:albumId>', methods=['GET', 'POST'])
def album_selected(albumId):
    # check de l'etat de connection de l'utilisateur
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


# page d'affichage des musiques
@app.route('/tracks_page', methods=['GET', 'POST'])
def tracks_page():
    # check de l'etat de connection de l'utilisateur
    if isLoggedIn() == False:
        return redirect("/")

    # récupération de l'argument 'liked' permettant de savoir si l'on doit afficher toutes les musiques ou seulement celles aimées par l'utilisateur
    liked = request.args.get('liked', False)

    conn = db_connection()
    cur = conn.cursor()
    id_user = session["user"][0]

    # affichage de toutes les musiques
    if liked == False:
        sql = """ SELECT * FROM tracks INNER JOIN artists ON tracks.id_artist = artists.id INNER JOIN albums ON tracks.id_album = albums.id """
        cursor = cur.execute(sql)
        track = cursor.fetchall()
        return render_template("tracks_page.html", tracks=track, likePage=False)
    
    # affichage des musiques likées
    else:
        sql = """ SELECT * FROM tracks INNER JOIN artists ON tracks.id_artist = artists.id INNER JOIN albums ON tracks.id_album = albums.id INNER JOIN tracks_liked ON tracks.id = tracks_liked.id_track WHERE id_user = ? """
        cursor = cur.execute(sql, (id_user,))
        track = cursor.fetchall()
        return render_template("tracks_page.html", tracks=track, likePage=True)
      
# page de selection d'artistes
@app.route('/artists_page', methods=['GET', 'POST'])
def artists_page():
    # check de l'etat de connection de l'utilisateur
    if isLoggedIn() == False:
        return redirect("/")

    # récupération de l'argument 'liked' permettant de savoir si l'on doit afficher tous les artistes ou seulement ceux aimés par l'utilisateur
    liked = request.args.get('liked', False)

    conn = db_connection()
    cur = conn.cursor()

    # adaptation de la requette en fonction de la valeur de 'liked'
    if liked == False:
        sql = """ SELECT * FROM artists """
    else:
        sql = """  """

    sql = """ SELECT * FROM artists """
    cursor = cur.execute(sql)
    artist = cursor.fetchall()
    return render_template("artists_page.html", artists=artist)

# route d'ajout d'une musique aux favoris
@app.route('/favtrack/<int:id>', methods=['GET', 'POST'])
def add_favtrack(id):
    # check de l'etat de connection de l'utilisateur
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

