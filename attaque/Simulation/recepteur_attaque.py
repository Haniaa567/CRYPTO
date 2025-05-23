'''''
import socket
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, dsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend

# Fonctions RSA
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def key_to_base64(key, is_private=False):
    if is_private:
        key_bytes = key.private_bytes(encoding=serialization.Encoding.DER, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    else:
        key_bytes = key.public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return base64.b64encode(key_bytes).decode('utf-8')

def decrypt_with_rsa(ciphertext, private_key):
    return private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

# Fonction AES
def decrypt_message(ciphertext, key):
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(padded_message) + unpadder.finalize()

# Générer les clés RSA
private_key_b, public_key_b = generate_keys()
public_key_b_b64 = key_to_base64(public_key_b)

# Écouter sur port 54321
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 54321))
s.listen(1)
print("En attente de connexion...")

conn, addr = s.accept()
print(f"Connecté à {addr}")

# Envoyer la clé publique RSA de B (via l'attaquant)
conn.send(public_key_b_b64.encode())

# Recevoir la longueur des données
data_len = int.from_bytes(conn.recv(4), byteorder='big')
data = b""
while len(data) < data_len:
    packet = conn.recv(data_len - len(data))
    if not packet:
        break
    data += packet

# Extraire les composants
encrypted_aes_key, ciphertext, signature, dsa_public_key_bytes = data.split(b"||")

# Déchiffrer la clé AES
aes_key = decrypt_with_rsa(encrypted_aes_key, private_key_b)

# Charger la clé publique DSA
dsa_public_key = serialization.load_der_public_key(dsa_public_key_bytes, backend=default_backend())

# Vérifier la signature
try:
    dsa_public_key.verify(signature, ciphertext, hashes.SHA256())
    print("Signature valide.")
except Exception as e:
    print(f"Signature invalide : {e}")
    conn.close()
    s.close()
    exit()

# Déchiffrer le message
plaintext = decrypt_message(ciphertext, aes_key)
print(f"Message déchiffré : {plaintext.decode()}")

conn.close()
s.close()
'''
import socket
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, dsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend

# Fonctions RSA
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def key_to_base64(key, is_private=False):
    if is_private:
        key_bytes = key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    else:
        key_bytes = key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    return base64.b64encode(key_bytes).decode('utf-8')

def decrypt_with_rsa(ciphertext, private_key):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Fonction AES pour déchiffrement
def decrypt_message(ciphertext, key):
    try:
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_message = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(padded_message) + unpadder.finalize()
    except Exception as e:
        print(f"Erreur lors du déchiffrement : {e}")
        raise

# Étape 1 : Génération des clés RSA
print("Étape 1 : Génération des clés privée et publique RSA pour B...")
private_key_b, public_key_b = generate_keys()
print("Étape 1 : Clés RSA générées avec succès.")

# Étape 2 : Conversion de la clé publique en base64
print("Étape 2 : Conversion de la clé publique RSA en format base64...")
public_key_b_b64 = key_to_base64(public_key_b)
print("Étape 2 : Clé publique convertie avec succès.")

# Étape 3 : Démarrage du serveur
print("Étape 3 : Démarrage du serveur sur 127.0.0.1:12345...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 12345))
s.listen(1)
print("Étape 3 : Serveur démarré avec succès.")

# Étape 4 : Attente de connexion
print("Étape 4 : En attente de connexion avec l'émetteur...")
conn, addr = s.accept()
print(f"Étape 4 : Connecté à {addr} avec succès.")

# Étape 5 : Envoi de la clé publique RSA
print("Étape 5 : Envoi de la clé publique RSA de B à l'émetteur...")
conn.send(public_key_b_b64.encode())
print("Étape 5 : Clé publique envoyée avec succès.")

# Étape 6 : Réception de la longueur des données
print("Étape 6 : Réception de la longueur des données chiffrées...")
data_len = int.from_bytes(conn.recv(4), byteorder='big')
print(f"Étape 6 : Longueur des données reçue avec succès : {data_len} octets.")

# Étape 7 : Réception des données
print("Étape 7 : Réception des données chiffrées...")
data = b""
while len(data) < data_len:
    chunk = conn.recv(data_len - len(data))
    if not chunk:
        raise ValueError("Connexion interrompue pendant la réception.")
    data += chunk
print("Étape 7 : Données reçues avec succès.")

# Étape 8 : Séparation des composants
print("Étape 8 : Séparation des données en clé AES chiffrée, message, signature et clé publique DSA...")
try:
    encrypted_aes_key, ciphertext, signature, dsa_public_key_bytes = data.split(b"||")
    print(f"Étape 8 : Composants séparés avec succès.")
    print(f"Longueur encrypted_aes_key : {len(encrypted_aes_key)}")
    print(f"Longueur ciphertext : {len(ciphertext)}")
    print(f"Longueur signature : {len(signature)}")
    print(f"Longueur dsa_public_key_bytes : {len(dsa_public_key_bytes)}")
except ValueError as e:
    print(f"Étape 8 : Erreur lors de la séparation des données : {e}")
    conn.close()
    s.close()
    exit()

# Étape 9 : Déchiffrement de la clé AES
print("Étape 9 : Déchiffrement de la clé AES avec la clé privée RSA de B...")
try:
    aes_key = decrypt_with_rsa(encrypted_aes_key, private_key_b)
    print("Étape 9 : Clé AES déchiffrée avec succès.")
except Exception as e:
    print(f"Étape 9 : Erreur lors du déchiffrement de la clé AES : {e}")
    conn.close()
    s.close()
    exit()

# Étape 10 : Chargement de la clé publique DSA
print("Étape 10 : Chargement de la clé publique DSA...")
try:
    dsa_public_key = serialization.load_der_public_key(dsa_public_key_bytes, backend=default_backend())
    print("Étape 10 : Clé publique DSA chargée avec succès.")
except Exception as e:
    print(f"Étape 10 : Erreur lors du chargement de la clé publique DSA : {e}")
    conn.close()
    s.close()
    exit()

# Étape 11 : Vérification de la signature
print("Étape 11 : Vérification de la signature avec la clé publique DSA...")
try:
    dsa_public_key.verify(signature, ciphertext, hashes.SHA256())
    print("Étape 11 : Signature valide.")
except Exception as e:
    print(f"Étape 11 : Signature invalide (attendue dans un scénario d'attaque) : {e}")
    conn.close()
    s.close()
    exit()

# Étape 12 : Déchiffrement du message
print("Étape 12 : Déchiffrement du message avec la clé AES...")
try:
    plaintext = decrypt_message(ciphertext, aes_key)
    print(f"Étape 12 : Message déchiffré avec succès : {plaintext.decode()}")
except Exception as e:
    print(f"Étape 12 : Erreur lors du déchiffrement (peut-être due à une corruption par l'attaquant) : {e}")
    conn.close()
    s.close()
    exit()

# Étape 13 : Fermeture des connexions
print("Étape 13 : Fermeture de la connexion avec l'émetteur...")
conn.close()
print("Étape 13 : Connexion avec l'émetteur fermée.")

print("Étape 13 : Fermeture du serveur...")
s.close()
print("Étape 13 : Serveur fermé avec succès.")