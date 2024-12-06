from flask import Flask, request, redirect, url_for, render_template, session, flash
import bcrypt

import AccessToken
from User import User, printData, insertUser, find_user_by_email
from Client import Client, insertClient, get_authorization_url, exchange_code_for_token, get_token_url

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

client1 = Client('sitoQualsiasi',
         'segreto1',
         'http://localhost:5000/callback',
         'http://localhost:5000/authorize',
         'http://localhost:5000/token'
        )

insertClient(client1)

@app.route('/')
def index():
    return render_template('homepage_IDP.html')

@app.route('/registrazione_IDP', methods=['GET', 'POST'])
def registrazione_IDP():

    if request.method == 'POST':
        email = request.form['email']
        result = find_user_by_email(email)

        if result is not None:
            flash('Email già presente nel sistema, inserire una email diversa.')
            return redirect(url_for('registrazione_IDP'))

        newUser = User(request.form['name'],
                       request.form['surname'],
                       request.form['email'],
                       bcrypt.hashpw(request.form['password'].encode('UTF-8'), bcrypt.gensalt()),
                       request.form['address'],
                       request.form['city'],
                       request.form['state'],
                       request.form['zip']
                       )

        printData(newUser)

        insertUser(newUser)

        return redirect(url_for('registrazione_completata'))

    return render_template('registrazione_IDP.html')

@app.route('/registrazione_completata')
def registrazione_completata():
    return render_template('registrazione_completata.html')

@app.route('/homepage_sito')
def homepage_sito():
    authorization_url = get_authorization_url(client1)
    print('authorization_url:', authorization_url)
    return render_template('homepage_sito.html',authorization_url=authorization_url)

@app.route('/authorize')
def authorize(): #dopo il tasto "accesso riservato con IDP"
     # Reindirizza l'utente all'URL di autorizzazione
    return render_template('authorize.html')

@app.route('/login_IDP', methods=['GET', 'POST'])
def login_IDP():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('UTF-8')

        print(email, password)

        # Trova l'utente dal database usando l'email
        user = find_user_by_email(email)

        if user is not None and bcrypt.checkpw(password, user.hashPassword) == True:
            print('utente trovato')
            # Se l'utente esiste e la password è corretta
            session['user_id'] = user.userID  # Salva l'ID dell'utente nella sessione
            return redirect(url_for('autorizza'))  # Reindirizza all'autorizzazione

        else:
            print('Email o password errati. Riprova.')

    return render_template('login_IDP.html')

@app.route('/autorizza')
def autorizza():
    code=12
    callback_url = f"{client1.redirectURI}?code={code}"
    return render_template('autorizza.html',callback_url=callback_url)

@app.route('/callback') # rotta che viene dopo il tasto autorizza presente nell'authorization URL
def callback():
    code = request.args.get('code')
    print('code preso dallURL:', code)

    token_url = url_for('token', grant_type='authorization_code', code=code, redirect_uri=client1.redirectURI, client_id=client1.clientID, )
    print('token_url:', token_url)

    if code:
        # Reindirizza alla pagina del token con il codice
        return redirect(token_url)
    return "Errore: codice di autorizzazione non trovato", 400

@app.route('/token')
def token():
    code = request.args.get('code')
    access_token = exchange_code_for_token(client1, code)

    return render_template('token.html', access_token=access_token)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/accesso_risorsa')
def accesso_risorsa():
    code=request.args.get('code')
    access_token_validato = AccessToken.validate_jwt(exchange_code_for_token(client1,code), AccessToken.public_key)

    return render_template(accesso_risorsa.html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)