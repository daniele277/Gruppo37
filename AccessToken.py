from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
import os
import jwt

from User import find_user_by_id


def generate_rsa_keypair():

# Genera la chiave privata RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  # Dimensione della chiave in bit
        backend=default_backend()
    )

# Estrae la chiave pubblica

    public_key = private_key.public_key()

    return private_key, public_key


class AccessToken:
    pass

def save_encrypted_private_key(private_key, filename, password):

    #Salva una chiave privata crittografata con una password.

    # Usa BestAvailableEncryption per crittografare la chiave con una password

    encrypted_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
        )

    with open(filename, 'wb') as f:
        f.write(encrypted_pem) #salvataggio della chiave all'interno del file

def save_public_key(public_key, filename):

    #Salva la chiave pubblica in formato PEM su file.

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as f:
        f.write(pem)

def load_encrypted_private_key(filename, password):
    # Funzione che definisce il caricamento della chiave privata dal file
    with open(filename, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=password.encode('utf-8'),
            backend=default_backend()
        )
    return private_key


def load_public_key(filename):

# Caricamento della chiave pubblica associata alla chiave privata dal file

    with open(filename, "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    return public_key

password = 'prova'

private_key_file = "encrypted_private_key.pem"

public_key_file = "public_key.pem"

# Controlla se le chiavi esistono già
if not (os.path.exists(private_key_file) and os.path.exists(public_key_file)):
    # Genera e salva una nuova coppia di chiavi
    private_key, public_key = generate_rsa_keypair()

    save_encrypted_private_key(private_key, private_key_file, password)

    save_public_key(public_key, public_key_file)
else:
    # Carica le chiavi già esistenti dai file

    private_key = load_encrypted_private_key(private_key_file, password)

    public_key = load_public_key(public_key_file)

print("Chiave privata crittografata",private_key," e chiave pubblica", public_key)

# Carica la chiave privata crittografata

private_key_loaded = load_encrypted_private_key("encrypted_private_key.pem", password)

print("Chiave privata caricata e decrittografata con successo.")

#Funzione che genera un token univoco per ogni user esistente

def generate_jwt(user_id,client_id, code):

    user = find_user_by_id(user_id)

    if not code:
        raise ValueError("Il codice di autorizzazione non può essere vuoto.")
    payload = {

            'user_id': user.userID,
            'name': user.name,
            'surname':user.surname,
            'email': user.email,
            'client_id': client_id,
            'code': code,
            'address': user.address,
            'city': user.city,
            'state': user.state
    }

    token = jwt.encode(payload, private_key_loaded , algorithm='RS256')

    return token

def validate_jwt(token, public_key):

        # Valida un JWT usando la chiave pubblica.

        try:
            decoded_token = jwt.decode(token, public_key, algorithms=["RS256"])
            print("Token valido:", decoded_token)
            return decoded_token
        except jwt.InvalidTokenError as e:
            print("Token non valido:", str(e))