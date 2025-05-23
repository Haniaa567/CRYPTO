from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

def pad_message(message):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message) + padder.finalize()
    return padded_message

def encrypt_message(message, encoded_key):
    iv = os.urandom(16)
    key=base64.b64decode(encoded_key)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_message = pad_message(message)
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return iv + ciphertext

def main():
    message = input("Entrez votre message à chiffrer : ").encode('utf-8')
    key = os.urandom(32)  # Utilisez une clé aléatoire de 32 octets
    
    encoded_key = base64.b64encode(key).decode('utf-8')
    ciphertext = encrypt_message(message, encoded_key)
    encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')


    print("Texte chiffré (base64):", encoded_ciphertext)
    print("Clé utilisée (base64):", encoded_key)

if __name__ == "__main__":
    main()