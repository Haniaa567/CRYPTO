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
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(padded_message) + unpadder.finalize()

# Générer les clés RSA pour B
private_key_b, public_key_b = generate_keys()
public_key_b_b64 = key_to_base64(public_key_b)

# Créer un socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 12345))
s.listen(1)
print("En attente de connexion...")

conn, addr = s.accept()
print(f"Connecté à {addr}")

# Envoyer la clé publique RSA de B à A
conn.send(public_key_b_b64.encode())

# Recevoir la longueur des données
data_len = int.from_bytes(conn.recv(4), byteorder='big')
data = b""
while len(data) < data_len:
    data += conn.recv(data_len - len(data))

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
