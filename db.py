import sqlite3

conn = sqlite3.connect("pylyre.sqlite")

cursor = conn.cursor()

sql_query = """ CREATE TABLE tracks_liked(
           id integer PRIMARY KEY,
           id_user integer,
           id_track integer
           
) """

cursor.execute(sql_query)
