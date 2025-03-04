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
    key = generate_random_matrix(block_size)

    print("Matrice de clé utilisée :")
    print(key)

    message = "HELLOHILLLLL"

    encrypted_message = encrypt(message, key)
    print(f"Message chiffré : {encrypted_message}")

    decrypted_message = decrypt(encrypted_message, key)
    print(f"Message déchiffré : {decrypted_message}")
