import sqlite3
from contextlib import nullcontext
from urllib.parse import urlencode
import jwt
from flask import redirect, url_for
import requests
from datetime import datetime, timedelta

class Client:

    _next_id = 1

    def __init__(self, name, clientSecret, redirectURI, authEndpoint, tokenEndpoint):
        self.clientID = Client._next_id
        Client._next_id += 1
        self.name = name
        self.clientSecret = clientSecret
        self.redirectURI = redirectURI
        self.grantType = 'code'
        self.scope = 'profile'
        self.tokenExpiryDate = (datetime.now() + timedelta(seconds=20)).strftime('%Y-%m-%d %H:%M:%S')
        self.authEndpoint = authEndpoint
        self.tokenEndpoint = tokenEndpoint

def insertClient(client):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('''
                   INSERT INTO Client (clientID, name, grantType, scope, tokenExpiryDate, clientSecret, redirectURI, authEndpoint, tokenEndpoint)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (client.clientID, client.name, client.grantType, client.scope, client.tokenExpiryDate, client.clientSecret, client.redirectURI, client.authEndpoint, client.tokenEndpoint))
                connection.commit()

                print("Dati client inseriti nel database con successo!")

        except sqlite3.Error as e:
            return f"Errore nel database: {e}"
        return nullcontext


def get_authorization_url(self):
    return f"{self.authEndpoint}?response_type=code&client_id={self.clientID}&&redirect_uri={self.redirectURI}&scope={self.scope}"

def get_token_url(self, code):
    return f"{self.tokenEndpoint}?grant_type=authorization_code&code={code}&redirect_uri={self.redirectURI}&client_id={self.clientID}&client_secret={self.clientSecret}"


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

    token = jwt.encode(payload, self.clientSecret, algorithm='HS256')

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
