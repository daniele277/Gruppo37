import sqlite3
# Classe che consente la connessione al nostro DB

connection = sqlite3.connect('database.db')

with open('registrazione_IDP.sql') as f:
    connection.executescript(f.read())
    connection.commit()
    connection.close()