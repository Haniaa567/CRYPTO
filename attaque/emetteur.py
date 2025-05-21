import socket
import base64
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, dsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend

# Fonctions RSA
def key_to_base64(key, is_private=False):
    if is_private:
        key_bytes = key.private_bytes(encoding=serialization.Encoding.DER, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    else:
        key_bytes = key.public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return base64.b64encode(key_bytes).decode('utf-8')

def base64_to_public_key(b64_key):
    key_bytes = base64.b64decode(b64_key.encode('utf-8'))
    return serialization.load_der_public_key(key_bytes, backend=default_backend())

def encrypt_with_rsa(message, public_key):
    return public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

# Fonctions AES
def pad_message(message):
    padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
    return padder.update(message) + padder.finalize()

def encrypt_message(message, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_message = pad_message(message)
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return iv + ciphertext

# Générer les clés DSA
dsa_private_key = dsa.generate_private_key(key_size=2048, backend=default_backend())
dsa_public_key = dsa_private_key.public_key()

# Générer une clé AES
aes_key = os.urandom(32)

# Se connecter à l'attaquant (port 12345)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Tentative de connexion à l'attaquant...")
s.connect(('127.0.0.1', 12345))
print("Connecté à l'attaquant.")

# Recevoir la clé publique RSA de B (via l'attaquant)
public_key_b_b64 = s.recv(4096).decode()
public_key_b = base64_to_public_key(public_key_b_b64)

# Chiffrer la clé AES
encrypted_aes_key = encrypt_with_rsa(aes_key, public_key_b)

# Message à envoyer
message = input("Entrez votre message à chiffrer : ").encode('utf-8')

# Chiffrer le message
ciphertext = encrypt_message(message, aes_key)

# Signer le message
signature = dsa_private_key.sign(ciphertext, hashes.SHA256())

# Préparer et envoyer les données
data = encrypted_aes_key + b"||" + ciphertext + b"||" + signature + b"||" + dsa_public_key.public_bytes(
    encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo
)
s.send(len(data).to_bytes(4, byteorder='big') + data)
print("Message envoyé à l'attaquant.")

s.close()
