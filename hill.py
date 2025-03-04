
# Chiffrement de Hill avec taille de bloc variable
import numpy as np

# Paramètre global
ALPHABET_SIZE = 26

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1

def is_inversible(matrix):
    det = int(round(np.linalg.det(matrix))) % ALPHABET_SIZE
    return pgcd(det, ALPHABET_SIZE) == 1

def generate_random_matrix(size):
    while True:
        matrix = np.random.randint(0, ALPHABET_SIZE, (size, size))
        if is_inversible(matrix):
            return matrix

def matrix_mod_inverse(matrix):
    det = int(round(np.linalg.det(matrix))) % ALPHABET_SIZE
    inv_det = mod_inverse(det, ALPHABET_SIZE)
    if inv_det == -1:
        raise ValueError("La matrice n'est pas inversible modulo 26")
    adjugate = np.round(np.linalg.inv(matrix) * np.linalg.det(matrix)).astype(int)
    return (adjugate * inv_det) % ALPHABET_SIZE

def text_to_vector(text, size):
    text = text.upper().replace(" ", "")
    while len(text) % size != 0:
        text += 'X'
    return [ord(char) - ord('A') for char in text]

def vector_to_text(vector):
    return ''.join(chr(v + ord('A')) for v in vector)

def encrypt(plaintext, key):
    size = key.shape[0]
    plaintext_vector = text_to_vector(plaintext, size)
    encrypted_vector = []

    for i in range(0, len(plaintext_vector), size):
        block = np.array(plaintext_vector[i:i+size])
        encrypted_block = np.dot(key, block) % ALPHABET_SIZE
        encrypted_vector.extend(encrypted_block)

    return vector_to_text(encrypted_vector)

def decrypt(ciphertext, key):
    size = key.shape[0]
    ciphertext_vector = text_to_vector(ciphertext, size)
    decrypted_vector = []

    inverse_key = matrix_mod_inverse(key)

    for i in range(0, len(ciphertext_vector), size):
        block = np.array(ciphertext_vector[i:i+size])
        decrypted_block = np.dot(inverse_key, block) % ALPHABET_SIZE
        decrypted_vector.extend(decrypted_block)

    return vector_to_text(decrypted_vector)

if __name__ == "__main__":
    block_size = 4 # Taille du bloc (modifiable)
    #key = generate_random_matrix(block_size)
    key=[[7,15],[24,15]]
    print("Matrice de clé utilisée :")
    print(key)

    message = "LAETYUZPXBXP"

    encrypted_message = encrypt(message, key)
    print(f"Message chiffré : {encrypted_message}")

    decrypted_message = decrypt(encrypted_message, key)
    print(f"Message déchiffré : {decrypted_message}")
'''
import numpy as np
from math import gcd

# Vérifier l'inversibilité
def is_invertible(matrix, mod=26):
    det = int(round(np.linalg.det(matrix))) % mod
    return gcd(det, mod) == 1

# Convertir texte en nombres (A=0, ..., Z=25)
def letter_to_number(text):
    return [ord(char) - ord('A') for char in text]

# Convertir nombres en texte
def number_to_letter(numbers):
    return ''.join(chr(n + ord('A')) for n in numbers)

# Chiffrer avec Hill
def encrypt(message, key):
    n = len(key)
    message = message.upper().replace(" ", "")
    # Compléter le message si nécessaire
    while len(message) % n != 0:
        message += 'X'

    message_numbers = letter_to_number(message)
    encrypted_numbers = []

    for i in range(0, len(message_numbers), n):
        block = np.array(message_numbers[i:i + n])
        encrypted_block = np.dot(key, block) % 26
        encrypted_numbers.extend(encrypted_block)

    return number_to_letter(encrypted_numbers)

# Déchiffrer avec Hill
def decrypt(ciphertext, key):
    n = len(key)
    key_inv = np.linalg.inv(key) * round(np.linalg.det(key))
    key_inv = np.round(key_inv).astype(int) % 26
    det_inv = pow(int(round(np.linalg.det(key))) % 26, -1, 26)
    key_inv = (det_inv * key_inv) % 26

    ciphertext_numbers = letter_to_number(ciphertext)
    decrypted_numbers = []

    for i in range(0, len(ciphertext_numbers), n):
        block = np.array(ciphertext_numbers[i:i + n])
        decrypted_block = np.dot(key_inv, block) % 26
        decrypted_numbers.extend(decrypted_block)

    return number_to_letter(decrypted_numbers)

if __name__ == "__main__":
    block_size = 2
    key = [[7, 15], [24, 15]]

    if not is_invertible(key):
        print("⚠️ La matrice clé n'est pas inversible modulo 26.")
        exit()

    print("Matrice de clé utilisée :")
    print(np.array(key))

    message = "LAETYUZPXBXP"

    encrypted_message = encrypt(message, key)
    print(f"Message chiffré : {encrypted_message}")

    decrypted_message = decrypt(encrypted_message, key)
    print(f"Message déchiffré : {decrypted_message}")
'''