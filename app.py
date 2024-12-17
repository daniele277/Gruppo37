import re #Gestione delle regular expression nelle condizioni di inserimento della password
import string
import random
import requests
from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify
import bcrypt
from flask_mail import Mail, Message
from AccessToken import generate_jwt
from User import User, printData, insertUser, find_user_by_email
from AuthorizationCode import generate_authorization_code, validate_authorization_code

app = Flask(__name__)

app.secret_key = 'chiave_segreta_per_la_sessione'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False  # Deve essere False se stai usando TLS
app.config['MAIL_USERNAME'] = 'idiot.proof44@gmail.com'  # Sostituisci con la tua email
app.config['MAIL_PASSWORD'] = 'fuxs jeab hayh gwlq'  # Sostituisci con la tua password o una password app-specifica

mail = Mail(app)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# Funzione per inviare OTP via email
def send_otp_email(user_email, otp):
    print(user_email)
    msg = Message("Il tuo OTP per l'autenticazione 2FA", sender="idiot.proof44@gmail.com", recipients=[user_email])
    msg.body = f"Il tuo codice OTP è: {otp}"
    try:
        mail.send(msg)
        print("OTP inviato via email!")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")
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

@app.route('/authorize')
def authorize(): #dopo il tasto "accesso riservato con IDP"
    session['redirect_uri'] = request.args.get('redirect_uri')
    session['client_id'] = request.args.get('client_id')
    session['state'] = request.args.get('state')
    session['scope'] = request.args.get('scope')
    session['response_type'] = request.args.get('response_type')

    return render_template('authorize.html')

def validate_password(password):
    if (len(password) < 8 or
            not re.search(r"[A-Z]", password) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True

@app.route('/login_IDP', methods=['GET', 'POST'])
def login_IDP():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verifica dei criteri della password
        if not validate_password(password):
            flash('La password deve contenere almeno 8 caratteri, una lettera maiuscola e un carattere speciale.')
            print('La password non soddisfa i criteri di sicurezza.')
            return render_template('login_IDP.html')

        # Continua con la logica di login
        password = password.encode('UTF-8')

        print(email, password)

        # Trova l'utente dal database usando l'email
        user = find_user_by_email(email)

        if user is not None and bcrypt.checkpw(password, user.hashPassword):
            print('utente trovato')
            # Se l'utente esiste e la password è corretta
            session['user_id'] = user.userID # Salva l'ID dell'utente nella sessione
            otp = generate_otp()
            session['otp'] = otp
            send_otp_email(email,otp)

            return redirect(url_for('verifica_otp'))  # Reindirizza all'autorizzazione

        else:
            print('Email o password errati. Riprova.')
            flash('Email o password errati. Riprova.')

    return render_template('login_IDP.html')

@app.route('/verifica_otp', methods=['GET', 'POST'])
def verifica_otp():

    if request.method == 'POST':

        otp = request.form['otp']
        print('otp: ',otp)

        if otp == session.get('otp'):
            return redirect(url_for('autorizza'))
        else:
            return redirect(url_for('login_IDP'))

    return render_template('verifica_otp.html')
@app.route('/autorizza')
def autorizza():
    code = generate_authorization_code(session.get('client_id'),session.get('user_id'))
    callback_url = f"{session.get('redirect_uri')}?code={code.code}&state={session.get('state')}"
    return render_template('autorizza.html',callback_url=callback_url)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/token')
def token():

    code = request.args.get('code')

    validate_authorization_code(code, session.get('client_id'))

    access_token = generate_jwt(session.get('user_id'),session.get('client_id'), code)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get("http://localhost:5001/accesso_risorsa", headers=headers)


    if response.status_code == 200:

        try:
            data=response.json()

            return data
        except ValueError:

            print("Decodifica JSON fallita")

            return response.text

    else:
        return jsonify({"Errore": f"Errore {response.status_code}: {response.text}"}), response.status_code



   # accesso_url = (f"{'http://localhost:5001/accesso_risorsa'}?token={access_token}&user_id={session.get('user_id')}" )

    #return redirect(accesso_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)