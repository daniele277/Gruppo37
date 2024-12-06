from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
import os
import jwt

def generate_rsa_keypair():

# Genera la chiave privata RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  # Dimensione della chiave in bit
        backend=default_backend()
    )

# Estrai la chiave pubblica
    public_key = private_key.public_key()

    return private_key, public_key


class AccessToken:
    pass

def save_encrypted_private_key(private_key, filename, password):
    """
    Salva una chiave privata crittografata con una password.
    """
    # Usa BestAvailableEncryption per crittografare la chiave con una password
    encrypted_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
        )

    with open(filename, 'wb') as f:
        f.write(encrypted_pem)

def save_public_key(public_key, filename):
    """
    Salva la chiave pubblica in formato PEM su file.
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as f:
        f.write(pem)

# Genera una coppia di chiavi RSA
private_key, public_key = generate_rsa_keypair()

# Definisci una password per crittografare la chiave privata
password = 'prova'

# Salva la chiave privata crittografata
save_encrypted_private_key(private_key, "encrypted_private_key.pem", password)

# Salva la chiave pubblica
save_public_key(public_key, "public_key.pem")

print("Chiave privata crittografata e chiave pubblica salvate su file.")

def load_public_key(filename):
    """
    Carica la chiave pubblica da un file PEM.
    """
    with open(filename, "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    return public_key

public_key = load_public_key("public_key.pem")

def validate_jwt(token, public_key):
        """
        Valida un JWT usando la chiave pubblica.
        """
        try:
            decoded_token = jwt.decode(token, public_key, algorithms=["RS256"])
            print("Token valido:", decoded_token)
        except jwt.InvalidTokenError as e:
            print("Token non valido:", str(e))
