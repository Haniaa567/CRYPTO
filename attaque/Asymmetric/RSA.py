from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64

def generate_keys():
    """Génère une paire de clés RSA"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def key_to_base64(key, is_private=False):
    """Convertit une clé RSA en Base64"""
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

def base64_to_private_key(b64_key):
    """Convertit une clé privée Base64 en objet clé RSA"""
    key_bytes = base64.b64decode(b64_key.encode('utf-8'))
    return serialization.load_der_private_key(key_bytes, password=None, backend=default_backend())

def base64_to_public_key(b64_key):
    """Convertit une clé publique Base64 en objet clé RSA"""
    key_bytes = base64.b64decode(b64_key.encode('utf-8'))
    return serialization.load_der_public_key(key_bytes, backend=default_backend())

def encrypt(message, public_key):
    """Chiffre un message avec la clé publique RSA"""
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt(ciphertext, private_key):
    """Déchiffre un message avec la clé privée RSA"""
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

while True:
    choice = input("Choisissez une option (g pour générer des clés, c pour chiffrer, d pour déchiffrer, q pour quitter) : ").lower()
    
    if choice == 'g':
        private_key, public_key = generate_keys()
        private_key_b64 = key_to_base64(private_key, is_private=True)
        public_key_b64 = key_to_base64(public_key)
        print(f"Clé publique (Base64) : {public_key_b64}")
        print(f"Clé privée (Base64) : {private_key_b64}")
        
    elif choice == 'c':
        message = input("Entrez le message à chiffrer : ").encode()
        public_key_b64 = input("Entrez la clé publique (en Base64) : ")
        public_key = base64_to_public_key(public_key_b64)
        ciphertext = encrypt(message, public_key)
        print(f"Texte chiffré : {ciphertext.hex()}")
        
    elif choice == 'd':
        ciphertext_hex = input("Entrez le texte chiffré (en hexadécimal) : ")
        ciphertext = bytes.fromhex(ciphertext_hex)
        private_key_b64 = input("Entrez la clé privée (en Base64) : ")
        private_key = base64_to_private_key(private_key_b64)
        plaintext = decrypt(ciphertext, private_key)
        print(f"Texte déchiffré : {plaintext.decode()}")
        
    elif choice == 'q':
        break
        
    else:
        print("Option invalide. Veuillez réessayer.")