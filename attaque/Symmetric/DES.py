import pyDes
import os

# Fonction pour chiffrer un texte en utilisant DES
def encrypt_des(plain_text, key):
    # Créer un objet DES en mode ECB
    cipher = pyDes.des(key, pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)
    # Chiffrer le texte en clair (encodé en bytes)
    encrypted_text = cipher.encrypt(plain_text.encode())
    return encrypted_text

# Fonction pour déchiffrer un texte chiffré en utilisant DES
def decrypt_des(encrypted_text, key):
    # Créer un objet DES en mode ECB
    cipher = pyDes.des(key, pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)
    # Déchiffrer le texte chiffré
    decrypted_text = cipher.decrypt(encrypted_text)
    return decrypted_text.decode()

# Exemple d'utilisation
key = os.urandom(8)  # Générer une clé DES de 8 octets (64 bits)
plain_text = "hello123"

# Chiffrer le texte en clair
encrypted_text = encrypt_des(plain_text, key)
print("Texte chiffré:", encrypted_text)

# Déchiffrer le texte chiffré
decrypted_text = decrypt_des(encrypted_text, key)
print("Texte déchiffré:", decrypted_text)