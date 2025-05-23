from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import os

def encrypt_message(message, encoded_key):
    nonce = os.urandom(16)  # Générer un nonce aléatoire de 16 octets
    key=base64.b64decode(encoded_key)
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return nonce + ciphertext

def decrypt_message(encoded_ciphertext, encoded_key):
    ciphertext = base64.b64decode(encoded_ciphertext)
    key = base64.b64decode(encoded_key)
    nonce = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def main():
    message = input("Entrez votre message à chiffrer : ").encode('utf-8')
    key = os.urandom(32)  # Générer une clé aléatoire de 32 octets
    encoded_key = base64.b64encode(key).decode('utf-8')
    ciphertext = encrypt_message(message, encoded_key)
    encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    

    print("Texte chiffré (base64):", encoded_ciphertext)
    print("Clé utilisée (base64):", encoded_key)

    decrypted_message = decrypt_message(encoded_ciphertext, encoded_key)
    print("Texte déchiffré:", decrypted_message.decode('utf-8'))

if __name__ == "__main__":
    main()