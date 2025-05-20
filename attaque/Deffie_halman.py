from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Générer les paramètres Diffie-Hellman
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

def generate_private_key():
    """Génère une clé privée Diffie-Hellman"""
    private_key = parameters.generate_private_key()
    return private_key

def generate_public_key(private_key):
    """Génère une clé publique Diffie-Hellman"""
    public_key = private_key.public_key()
    return public_key

def generate_shared_key(private_key, peer_public_key):
    """Génère une clé partagée Diffie-Hellman"""
    shared_key = private_key.exchange(peer_public_key)
    # Utiliser HKDF pour dériver une clé de 32 bytes (256 bits) pour AES
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'dh key exchange',
        backend=default_backend()
    ).derive(shared_key)
    return derived_key

def encrypt(message, key):
    """Chiffre un message avec AES"""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return iv + ciphertext

def decrypt(ciphertext, key):
    """Déchiffre un message avec AES"""
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

# Générer les clés privées et publiques pour deux parties
private_key1 = generate_private_key()
public_key1 = generate_public_key(private_key1)

private_key2 = generate_private_key()
public_key2 = generate_public_key(private_key2)

# Échanger les clés publiques et générer la clé partagée
shared_key1 = generate_shared_key(private_key1, public_key2)
shared_key2 = generate_shared_key(private_key2, public_key1)

# Vérifier que les clés partagées sont les mêmes
assert shared_key1 == shared_key2

# Chiffrer et déchiffrer un message
message = b"Bonjour, ceci est un message secret."
ciphertext = encrypt(message, shared_key1)
print(f"Texte chiffré : {ciphertext.hex()}")

plaintext = decrypt(ciphertext, shared_key2)
print(f"Texte déchiffré : {plaintext.decode()}")
