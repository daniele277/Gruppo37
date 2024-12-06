from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import bcrypt

from User import User
from Client import Client, insertClient

app = Flask(__name__)

client1 = Client('segreto1',
         'sitoQualsiasi',
         'https://example1.com/redirect',
         'https://provider1.com/oauth/authorize',
         'https://provider1.com/oauth/token'
        )

insertClient(client1)

@app.route('/')
def index():
    return render_template('homepage_IDP.html')

@app.route('/registrazione_IDP', methods=['GET', 'POST'])
def registrazione_IDP():

    if request.method == 'POST':
        newUser = User(request.form['name'], request.form['email'], request.form['password'])
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']

        print(f"Dati ricevuti: {name}, {surname}, {email}, {password}, {address}, {city}, {state}, {zip}")

        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute('''
                INSERT INTO User (name, surname, email, password, address, city, state, zip)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, surname, email, hash_password.decode('utf-8'), address, city, state, zip))
                connection.commit()

                print("Dati inseriti nel database con successo!")

        except sqlite3.Error as e:
            return f"Errore nel database: {e}"
        return redirect(url_for('registrazione_completata'))

    return render_template('registrazione_IDP.html')



@app.route('/registrazione_completata')
def registrazione_completata():
    return render_template('registrazione_completata.html')

@app.route('/homepage_sito')
def homepage_sito():
    return render_template('homepage_sito.html')

@app.route('/login_IDP')
def login_IDP():
    return render_template('login_IDP.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)