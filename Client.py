import sqlite3

class Client:

    _next_id = 1

    def __init__(self, name, redirectURI, authEndpoint, tokenEndpoint):
        self.clientID = Client._next_id
        Client._next_id += 1
        self.name = name
        self.redirectURI = redirectURI
        self.grantType = 'code'
        self.scope = 'profile'
        self.authEndpoint = authEndpoint
        self.tokenEndpoint = tokenEndpoint

#       self.insertClient()  -> modificare insertClient in modo che abbia come parametro solo self

def insertClient(client):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('''
                   INSERT INTO Client (clientID, name, grantType, scope, redirectURI, authEndpoint, tokenEndpoint)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ''', (client.clientID, client.name, client.grantType, client.scope, client.redirectURI, client.authEndpoint, client.tokenEndpoint))
                connection.commit()

                print("Dati client inseriti nel database con successo!")

        except sqlite3.Error as e:
            return f"Errore nel database: {e}"
        return None


def get_authorization_url(self):
    return f"{self.authEndpoint}?response_type=code&client_id={self.clientID}&&redirect_uri={self.redirectURI}&scope={self.scope}"

def get_token_url(self, code):
    return f"{self.tokenEndpoint}?grant_type=authorization_code&code={code}&redirect_uri={self.redirectURI}&client_id={self.clientID}&client_secret={self.clientSecret}"


@staticmethod
def getClientByID(clientID):
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
               SELECT * FROM Client WHERE clientID = ?
               ''', (clientID,))
            result = cursor.fetchone()
            if result:
                print(f"Client trovato: {result}")
                return result
            else:
                print("Client non trovato.")
                return None

    except sqlite3.Error as e:
        raise Exception(f"Errore nel database: {e}")
