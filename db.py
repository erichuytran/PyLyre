import sqlite3

conn = sqlite3.connect("pylyre.sqlite")

cursor = conn.cursor()

sql_query = """ CREATE TABLE users(
           id integer PRIMARY KEY,
           first_name String(120),
           last_name String(120),
           pseudo String(120),
           email String(120) UNIQUE,
           password String(120),
           date_last_login TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
           
) """

cursor.execute(sql_query)
