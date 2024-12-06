import sqlite3

class User:

    _next_id = 1

    def __init__(self, name, surname, email, hashPassword, address, city, state, zip):
        self.userID = User._next_id
        User._next_id += 1
        self.name = name
        self.surname = surname
        self.email = email
        self.hashPassword = hashPassword
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip

def printData(user):
    print(f"Dati ricevuti: {user.name}, {user.surname}, {user.email}, {user.hashPassword}, {user.address}, {user.city}, {user.state}, {user.zip}")

def insertUser(user):
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()

                cursor.execute('''
                   INSERT INTO User (userID, name, surname, email, hashPassword, address, city, state, zip)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (user.userID, user.name, user.surname, user.email, user.hashPassword.decode('utf-8'), user.address, user.city, user.state, user.zip))
                connection.commit()

                print("Dati user inseriti nel database con successo!")

        except sqlite3.Error as e:
            return f"Errore nel database: {e}"
        return None

def find_user_by_email(email):
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Cerca un utente che abbia la mail fornita
            cursor.execute('SELECT * FROM User WHERE email = ?', (email,))
            user_data = cursor.fetchone()

            if user_data:
                # Crea e restituisce un'istanza di User utilizzando i dati ottenuti
                user = User(
                    name=user_data[1],
                    surname=user_data[2],
                    email=user_data[3],
                    hashPassword=user_data[4].encode('utf-8'),  # Assicurati che sia in bytes
                    address=user_data[5],
                    city=user_data[6],
                    state=user_data[7],
                    zip=user_data[8]
                )
                user.userID = user_data[0]  # Assegna l'userID recuperato
                User._next_id = max(user.userID + 1, User._next_id)  # Gestisci l'incremento di ID
                return user
            else:
                print("Nessun utente trovato con questa email.")
                return None

    except sqlite3.Error as e:
        print(f"Errore nel database: {e}")
        return None

    except sqlite3.Error as e:
        print(f"Errore nel database: {e}")
        return f"Errore nel database: {e}"