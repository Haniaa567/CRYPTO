'''''
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
'''
import socket
import base64
import os
import time
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
    try:
        key_bytes = base64.b64decode(b64_key.encode('utf-8'))
        return serialization.load_der_public_key(key_bytes, backend=default_backend())
    except Exception as e:
        print(f"Erreur lors du décodage de la clé publique : {e}")
        return None

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

# Étape 1 : Génération des clés DSA
print("Étape 1 : Génération de la clé privée DSA...")
dsa_private_key = dsa.generate_private_key(key_size=2048, backend=default_backend())
print("Étape 1 : Clé privée DSA générée avec succès.")

# Étape 2 : Génération de la clé publique DSA
print("Étape 2 : Génération de la clé publique DSA à partir de la clé privée...")
dsa_public_key = dsa_private_key.public_key()
print("Étape 2 : Clé publique DSA générée avec succès.")

# Étape 3 : Génération de la clé AES
print("Étape 3 : Génération de la clé AES (32 octets)...")
aes_key = os.urandom(32)
print("Étape 3 : Clé AES générée avec succès.")

# Étape 4 : Connexion à l'attaquant
print("Étape 4 : Tentative de connexion à l'attaquant sur 127.0.0.1:54321...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)  # Timeout de 10 secondes
for attempt in range(5):  # 5 tentatives
    try:
        s.connect(('127.0.0.1', 54321))
        print("Étape 4 : Connecté à l'attaquant avec succès.")
        break
    except socket.timeout:
        print(f"Étape 4 : Tentative {attempt + 1}/5 - Timeout lors de la connexion. Attente 2 secondes...")
        time.sleep(2)
    except ConnectionRefusedError:
        print(f"Étape 4 : Tentative {attempt + 1}/5 - Connexion refusée. Attente 2 secondes...")
        time.sleep(2)
else:
    print("Étape 4 : Échec de la connexion à l'attaquant après 5 tentatives. Vérifiez que l'attaquant est en cours sur 54321.")
    exit()

# Étape 5 : Réception de la clé publique RSA de B
print("Étape 5 : Réception de la clé publique RSA de B via l'attaquant...")
try:
    public_key_b_b64 = s.recv(4096).decode()
    if not public_key_b_b64:
        raise ValueError("Aucune donnée reçue.")
    public_key_b = base64_to_public_key(public_key_b_b64)
    if public_key_b is None:
        raise ValueError("Clé publique invalide.")
    print("Étape 5 : Clé publique RSA de B reçue et décodée avec succès.")
except (socket.timeout, ValueError) as e:
    print(f"Étape 5 : Erreur lors de la réception de la clé publique : {e}")
    s.close()
    exit()

# Étape 6 : Chiffrement de la clé AES
print("Étape 6 : Chiffrement de la clé AES avec la clé publique RSA de B...")
try:
    encrypted_aes_key = encrypt_with_rsa(aes_key, public_key_b)
    print("Étape 6 : Clé AES chiffrée avec succès.")
except Exception as e:
    print(f"Étape 6 : Erreur lors du chiffrement : {e}")
    s.close()
    exit()

# Étape 7 : Saisie du message
print("Étape 7 : Demande de saisie du message à chiffrer...")
message = input("Entrez votre message à chiffrer : ").encode('utf-8')
print("Étape 7 : Message saisi avec succès.")

# Étape 8 : Chiffrement du message avec AES
print("Étape 8 : Chiffrement du message avec AES en mode CBC...")
ciphertext = encrypt_message(message, aes_key)
print("Étape 8 : Message chiffré avec succès.")

# Étape 9 : Signature du message
print("Étape 9 : Signature du message chiffré avec la clé privée DSA...")
signature = dsa_private_key.sign(ciphertext, hashes.SHA256())
print("Étape 9 : Signature générée avec succès.")

# Étape 10 : Préparation et envoi des données
print("Étape 10 : Préparation des données (clé AES chiffrée, message, signature, clé publique DSA)...")
data = encrypted_aes_key + b"||" + ciphertext + b"||" + signature + b"||" + dsa_public_key.public_bytes(
    encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo
)
s.send(len(data).to_bytes(4, byteorder='big') + data)
print("Étape 10 : Données envoyées à l'attaquant avec succès.")

# Étape 11 : Fermeture de la connexion
print("Étape 11 : Fermeture de la connexion avec l'attaquant...")
s.close()
print("Étape 11 : Connexion fermée avec succès.")