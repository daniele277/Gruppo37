import secrets
import sqlite3
from datetime import datetime, timedelta


class AuthorizationCode:
    def __init__(self, clientID, userID):
        self.code = secrets.token_urlsafe(16) #Genera un token casuale sicuro codificato in base64
        self.clientID = clientID
        self.userID = userID
        self.tokenExpiryDate = datetime.utcnow() + timedelta(minutes=1)  # Scadenza in 1 minut0

def store_authorization_code(self, clientID, userID):
    expires_at = datetime.utcnow() + timedelta(minutes=1)  # Codice valido per 1 minuto

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

def generate_authorization_code(clientID, userID):
    code = AuthorizationCode(clientID, userID)
    store_authorization_code(code, clientID, userID)

    return code

def validate_authorization_code(code, clientID):
    try:
        with sqlite3.connect('database.db') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM AuthorizationCode WHERE code = ? AND clientID = ?
               ''', (code, clientID))
            result = cursor.fetchone()

            print(result)

            if result and result['codeExpiryDate'] > datetime.utcnow():
                return True
            else:
                return False

    except sqlite3.Error as e:
        return f"Errore nel database: {e}"