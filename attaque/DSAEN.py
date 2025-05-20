
''''
import hashlib
import random

def generate_keys(q_bytes=20):
    q = random.randbytes(q_bytes)
    q = int.from_bytes(q, byteorder='big')
    
    p = q
    while True:
        p = next_prime(2*p + 1)
        if (p-1) % q == 0:
            break
            
    h = calculate_h(p, q)
    g = pow(h, (p-1)//q, p)
    
    x = random.randint(1, q-1)
    y = pow(g, x, p)
    
    return p, q, g, x, y

def sign(message, p, q, g, x):
    h = hashlib.sha256(message.encode()).hexdigest()
    h = int(h, 16)
    
    while True:
        k = random.randint(1, q-1)
        r = pow(g, k, p) % q
        if r > 0:
            break
            
    s = (inverse_mod(k, q) * (h + x*r)) % q
    
    return r, s

# Fonctions utilitaires
def next_prime(N):
    # Trouver le plus petit nombre premier >= N
    while True:
        if is_prime(N):
            return N
        N += 1

def is_prime(n):
    # Test de primalité simple
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def calculate_h(p, q):
    # Calculer h = un nombre aléatoire dans [2, p-2]
    while True:
        h = random.randint(2, p-2)
        # Vérifier si h^((p-1)/q) mod p != 1
        if pow(h, (p-1)//q, p) != 1:
            return h
        
def inverse_mod(a, m):
    # Calcule l'inverse modulaire de a modulo m
    # Algorithme étendu d'Euclide
    m0 = m
    x0 = 0
    x1 = 1
    
    if m == 1:
        return 0
    
    while a > 1:
        # q est le quotient
        q = a // m
        
        # Mettre à jour les valeurs
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
        
    # Ordre final
    if x1 < 0:
        x1 += m0
        
    return x1

# Demander à l'utilisateur d'entrer une phrase
phrase = input("Entrez une phrase : ")

# Générer les clés
p, q, g, x, y = generate_keys()

# Afficher les clés
print(f"Clé publique (p, q, g, y) : ({p}, {q}, {g}, {y})")
print(f"Clé privée (x) : {x}")

# Générer la signature
r, s = sign(phrase, p, q, g, x)

# Afficher la signature
print(f"Signature numérique (r, s) pour '{phrase}' : ({r}, {s})")
'''
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa, rsa
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES

# Génération des clés DSA
dsa_private_key = dsa.generate_private_key(key_size=2048, backend=default_backend())
dsa_public_key = dsa_private_key.public_key()

# Génération des clés RSA
rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
rsa_public_key = rsa_private_key.public_key()

# Entrer le message
message = input("Entrez le message à chiffrer et signer: ").encode()

# Chiffrement avec RSA
cipher = rsa_public_key.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

# Signature avec DSA
signature = dsa_private_key.sign(cipher, algorithm=hashes.SHA256())

# Envoyer le message chiffré et la signature
print(f"Message chiffré: {cipher.hex()}")
print(f"Signature DSA: {signature.hex()}")

# Côté destinataire
decrypted_message = rsa_private_key.decrypt(cipher, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

try:
    dsa_public_key.verify(signature, decrypted_message, algorithm=hashes.SHA256())
    print(f"Message déchiffré: {decrypted_message.decode()}")
    print("La signature est valide.")
except Exception as e:
    print(f"La signature n'est pas valide: {e}")