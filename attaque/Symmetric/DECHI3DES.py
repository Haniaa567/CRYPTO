from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

def unpad_message(padded_message):
    unpadder = padding.PKCS7(algorithms.TripleDES.block_size).unpadder()
    message = unpadder.update(padded_message) + unpadder.finalize()
    return message

def decrypt_message(ciphertext, key):
    
    iv = ciphertext[:8]  # DES utilise un IV de 8 octets
    actual_ciphertext = ciphertext[8:]
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(actual_ciphertext) + decryptor.finalize()
    message = unpad_message(padded_message)
    return message

def main():
    encoded_ciphertext = input("Entrez le texte chiffré (en base64): ")
    encoded_key = input("Entrez la clé (en base64): ")

    ciphertext = base64.b64decode(encoded_ciphertext)
    key = base64.b64decode(encoded_key)

    plaintext = decrypt_message(ciphertext, key)
    print("Texte déchiffré:", plaintext.decode('utf-8'))

if __name__ == "__main__":
    main()