import secrets
import sqlite3
import uuid
from datetime import datetime, timedelta


class AuthorizationCode:
    def __init__(self, clientID, userID):
        self.code = secrets.token_urlsafe(16)
        self.clientID = clientID
        self.userID = userID
        self.tokenExpiryDate = datetime.utcnow() + timedelta(minutes=10)  # Scadenza in 10 minuti

    def store_authorization_code(self, clientID, userID):
        expires_at = datetime.utcnow() + timedelta(minutes=10)  # Codice valido per 10 minuti

        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('''
                   INSERT INTO AuthorizationCode (code, codeExpiryDate, clientID, userID)
                   VALUES (?, ?, ?, ?)
                   ''', (self, expires_at, clientID, userID))
                connection.commit()

                print("Dati code inseriti nel database con successo!")

        except sqlite3.Error as e:
            return f"Errore nel database: {e}"
        return None

    def generate_authorization_code(self,clientID, userID):
        code = secrets.token_urlsafe(32)
        code.store_authorization_code(code, clientID, userID)

        return code


    def validate_authorization_code(self, clientID):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('''SELECT * FROM AuthorizationCode WHERE code = (?) AND clientID = (?)
                   ''', (self, clientID))
                connection.commit()

                print("Dati code inseriti nel database con successo!")

        except sqlite3.Error as e:
            return f"Errore nel database: {e}"
        return None
        query = "SELECT * FROM AuthorizationCodes WHERE code = %s AND client_id = %s"
        values = (self, clientID)
        result = db.fetch_one(query, values)

        if not result:
            return False  # Codice non valido
        if result['expires_at'] < datetime.utcnow():
            return False  # Codice scaduto

        return result