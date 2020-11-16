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

    # récupération d'informations pour les notifications de nouvelles sorties
    # récupération des artistes likés
    artistLiked = """ SELECT id_artist FROM artists_liked WHERE id_user = ? """
    curLikeArtists = cur.execute(artistLiked, (id_user,))
    ArtistLiked = [item[0] for item in curLikeArtists.fetchall()]

    # récupération des informations d'albums
    albumInfo = """ SELECT * FROM albums INNER JOIN artists ON albums.id_artist = artists.id """
    cursor = cur.execute(albumInfo)
    albumInfo = cursor.fetchall()

    # récupération de la date de dernière connexion de l'utilisateur
    dateConne = """ SELECT * FROM users WHERE id = ? """
    cursorDateConn = cur.execute(dateConne, (id_user,))
    dateC = cursorDateConn.fetchall()

    return render_template("main_page.html", dateC=dateC, albumInfo=albumInfo, ArtistLiked=ArtistLiked, id_user=id_user)

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

    # si non, on affiche les albums de l'artiste séléctionné (dépend de artists_page)
    else:
        sql = """ SELECT * FROM albums INNER JOIN artists ON albums.id_artist = artists.id WHERE id_artist = ? """
        cursor = cur.execute(sql, (id_artist,))
        album = cursor.fetchall()

    return render_template("albums_page.html", albums=album, id_artist=id_artist)

# page d'album selectionné
@app.route('/album_selected/<int:albumId>', methods=['GET', 'POST'])
def album_selected(albumId):
    # check de l'etat de connection de l'utilisateur
    if isLoggedIn() == False:
        return redirect("/")

    conn = db_connection()
    cur = conn.cursor()

    # récupération des musiques associées à l'album
    sqlTracks = """ SELECT * FROM tracks INNER JOIN artists ON tracks.id_artist = artists.id INNER JOIN albums ON tracks.id_album = albums.id WHERE id_album = ? """
    cursor = cur.execute(sqlTracks, (albumId,))
    track = cursor.fetchall()
    
    # récupération de l'image de l'album
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

    # adaptation de la requette en fonction de la valeur de 'liked'
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
    # affichage de tous les artistes
    if liked == False:
        sql = """ SELECT * FROM artists """
        cursor = cur.execute(sql)
        artist = cursor.fetchall()
        return render_template("artists_page.html", artists=artist, likePage=False)
    
        #affichage des artistes likés
    else:
        sql = """ SELECT * FROM artists INNER JOIN artists_liked ON artists.id = id_artist """
        cursor = cur.execute(sql)   
        artist = cursor.fetchall()
        return render_template("artists_page.html", artists=artist, likePage=True)
    

# route d'ajout d'une musique aux favoris
@app.route('/favtrack/<int:id>', methods=['GET', 'POST'])
def add_favtrack(id):
    # check de l'etat de connection de l'utilisateur
    if isLoggedIn() == False:
        return redirect("/")

    conn = db_connection()
    cur = conn.cursor()

    # récupération des informations de l'utilisateur
    id_track = id
    id_user = session["user"][0]
 
    # requêtes d'ajout / suppression de musiques likées
    sqlAdd = """ INSERT INTO tracks_liked(id_user, id_track)
                    VALUES(?,?) """
    sqlDelete = """ DELETE FROM tracks_liked WHERE id = ? """


    sqlTracks = """ SELECT * FROM tracks INNER JOIN artists ON tracks.id_artist = artists.id INNER JOIN albums ON tracks.id_album = albums.id """
    cursorTracks = cur.execute(sqlTracks)
    track = cursorTracks.fetchall()

    # requête de check : si la musique est déjà likée
    sqlCheck = """ SELECT id FROM tracks_liked WHERE id_user = ? AND id_track = ? """
    cursor = cur.execute(sqlCheck, (id_user, id_track))

    # res contient l'id de la rangée selectionnée (musique déjà likée)
    # res countains the id value of the selected row (already liked track)
    res = cursor.fetchall()

    # récupération du titre de la musique pour l'affichage
    trackInfoSql = """ SELECT title FROM tracks WHERE id = ? """
    cursorTrackInfo = cur.execute(trackInfoSql, (id_track,))
    trackInfo = cursorTrackInfo.fetchall()
    
    # si la chanson n'est pas déjà likée : (ajout)
    if not res:
        cur.execute(sqlAdd, (id_user, id_track))
        conn.commit()
        return render_template(("tracks_page.html"), tracks=track, trackName=trackInfo, isAdded=True)
    # si la chanson est déjà likée (supression)
    else:
        cur.execute(sqlDelete, (res[0][0],))
        conn.commit()
        return render_template(("tracks_page.html"), tracks=track, trackName=trackInfo, isAdded=False)


# route d'ajout d'un artiste aux favoris
@app.route('/favartist/<int:id>', methods=['GET', 'POST'])
def add_favartist(id):
    # check de l'etat de connection de l'utilisateur
    if isLoggedIn() == False:
        return redirect("/")

    conn = db_connection()
    cur = conn.cursor()

    id_artist = id
    id_user = session["user"][0]

    sqlAdd = """ INSERT INTO artists_liked(id_user, id_artist)
                    VALUES(?,?) """
    sqlCheck = """ SELECT id FROM artists_liked WHERE id_user = ? AND id_artist = ? """
    sqlDelete = """ DELETE FROM artists_liked WHERE id = ? """

    sqlAlbum = """ SELECT * FROM albums INNER JOIN artists ON albums.id_artist = artists.id WHERE id_artist = ? """
    cursor = cur.execute(sqlAlbum, (id_artist,))
    album = cursor.fetchall()

    #Requests if the track is already liked
    cursor = cur.execute(sqlCheck, (id_user, id_artist))

    #res countains the id value of the selected row (already liked artist)
    res = cursor.fetchall()

    if not res:
        cur.execute(sqlAdd, (id_user, id_artist))
        conn.commit()
        return render_template(("albums_page.html"), id_artist=id_artist, albums=album, isAdded=True)
    else:
        cur.execute(sqlDelete, (res[0][0],))
        conn.commit()
        return render_template(("albums_page.html"), id_artist=id_artist, albums=album, isAdded=False)


