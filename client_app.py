from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify
import requests

from AccessToken import validate_jwt, public_key, AccessToken
from AuthorizationCode import validate_authorization_code
from Client import Client, get_authorization_url, insertClient

app = Flask(__name__)

example_client = Client(
    'sitoQualsiasi',
    'http://localhost:5001/callback',
    'http://localhost:5000/authorize',
    'http://localhost:5000/token')

insertClient(example_client)

@app.route('/')
def index():
    authorization_url = get_authorization_url(example_client)
    print('authorization_url:', authorization_url)
    return render_template('homepage_sito.html',authorization_url=authorization_url)

@app.route('/callback') # rotta che viene dopo il tasto autorizza presente nell'authorization URL
def callback():
    code = request.args.get('code')

    token_url = (f"{example_client.tokenEndpoint}?grant_type=authorization_code&code={code}&redirect_uri={example_client.redirectURI}"
                 f"&client_id={example_client.clientID}")
    print('token_url:', token_url)

    if code:
        # Reindirizza alla pagina del token con il codice
        return redirect(token_url)
    return "Errore: codice di autorizzazione non trovato", 400

@app.route('/accesso_risorsa')
def accesso_risorsa():

    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith("Bearer "):
        jwt_token = auth_header.split(" ")[1]
    else:
        return jsonify({"message": "Token JWT mancante o formato errato"}), 401

    payload = validate_jwt(jwt_token, public_key)
    print(payload)

    return render_template('accesso_risorsa.html',user_name=payload.get('name'),email=payload.get('email'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)