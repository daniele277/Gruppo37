import secrets
import sqlite3
import uuid
from datetime import datetime, timedelta


class AuthorizationCode:
    def __init__(self, client_id, user_id):
        self.code = secrets.token_urlsafe(16)
        self.client_id = client_id
        self.user_id = user_id
        self.token_expiry_date = datetime.utcnow() + timedelta(minutes=10)  # Scadenza in 10 minuti

    def generate_code(self, client_id, user_id):
        code = str(uuid.uuid4())  # Genera un codice unico
        expiration_time = datetime.utcnow() + timedelta(minutes=10)  # Imposta la scadenza del codice a 10 minuti

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            query = '''
                INSERT INTO AuthorizationCode (codeID, tokenExpiryDate, clientID, userID)
                VALUES (?, ?, ?, ?)
            '''
            cursor.execute(query, (code, expiration_time.strftime('%Y-%m-%d %H:%M:%S'), client_id, user_id))

        return code

    @staticmethod
    def validate_code(code_id):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    SELECT codeID, tokenExpiryDate FROM AuthorizationCode
                    WHERE codeID = ?
                ''', (code_id,))
                result = cursor.fetchone()

                if result:
                    expiration = datetime.strptime(result[1], '%Y-%m-%d %H:%M:%S')
                    return datetime.utcnow() <= expiration

        except sqlite3.Error as e:
            print(f"Errore nel database: {e}")

        return False