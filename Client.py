import sqlite3
from urllib.parse import urlencode
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from flask import redirect, url_for
import requests
from datetime import datetime, timedelta

from AccessToken import password, load_encrypted_private_key


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


# Carica la chiave privata crittografata
private_key_loaded = load_encrypted_private_key("encrypted_private_key.pem", password)
print("Chiave privata caricata e decrittografata con successo.")

def exchange_code_for_token(self, code):

    if not code:
        raise ValueError("Il codice di autorizzazione non può essere vuoto.")
    payload = {
        'client_id': self.clientID,
        'code': code,
        'name': self.name,
        'scope': self.scope,
        'client_secret': self.clientSecret,
        'exp': datetime.utcnow() + timedelta(minutes=5)  # Durata token 5 minuti
    }

    token = jwt.encode(payload, private_key_loaded , algorithm='RS256')

    return token

def refresh_token(self, refresh_token):
    """
    Usa il refresh token per ottenere un nuovo access token.
    """
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': self.clientID,
        'client_secret': self.clientSecret,
    }
    response = requests.post(self.tokenEndpoint, data=data)
    if response.status_code == 200:
        token_info = response.json()
        return token_info
    else:
        raise Exception(f"Errore nel refresh del token: {response.status_code} {response.text}")
