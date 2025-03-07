import numpy as np
from sympy import Matrix, mod_inverse
import itertools
import json
ALPHABET_SIZE = 26

def pgcd(a: int, b: int) -> int:
    """Calcule le plus grand commun diviseur (PGCD) de deux nombres."""
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a: int, m: int) -> int:
    """Calcule l'inverse modulaire de a modulo m."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("L'inverse modulaire n'existe pas.")

def is_inversible(matrix: np.ndarray) -> bool:
    """Vérifie si une matrice est inversible modulo 26."""
    det = int(round(np.linalg.det(matrix))) % ALPHABET_SIZE
    return pgcd(det, ALPHABET_SIZE) == 1

def is_invertible_mod26(matrix):
    """Vérification rigoureuse de l'inversibilité modulo 26"""
    m = Matrix(matrix)
    det = m.det()
    try:
        mod_inverse(int(det) % 26, 26)
        return True
    except ValueError:
        return False

def matrix_mod_inverse(matrix: np.ndarray) -> np.ndarray:
    """Calcule l'inverse d'une matrice modulo 26."""
    det = int(round(np.linalg.det(matrix))) % ALPHABET_SIZE
    inv_det = mod_inverse(det, ALPHABET_SIZE)
    adjugate = np.round(np.linalg.inv(matrix) * np.linalg.det(matrix)).astype(int)
    return (adjugate * inv_det) % ALPHABET_SIZE

def parse_matrix(matrix_list: list) -> np.ndarray:
    """Convertit une liste en matrice numpy et vérifie l'inversibilité."""
    matrix = np.array(matrix_list)
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("La matrice doit être carrée (2x2 ou 3x3).")
    if not is_inversible(matrix):
        raise ValueError("La matrice n'est pas inversible modulo 26.")
    return matrix

def text_to_vector(text: str, size: int) -> list:
    """Convertit un texte en vecteur numérique."""
    text = text.upper().replace(" ", "")
    while len(text) % size != 0:
        text += 'X'
    return [ord(char) - ord('A') for char in text]

def vector_to_text(vector: list) -> str:
    """Convertit un vecteur numérique en texte."""
    return ''.join(chr(v + ord('A')) for v in vector)

def encrypt_message_hill(plaintext: str, matrix_list: list) -> str:
    """
    Chiffre un message en utilisant l'algorithme de Hill Cipher.
    """
    key = parse_matrix(matrix_list)
    size = key.shape[0]
    plaintext_vector = text_to_vector(plaintext, size)
    encrypted_vector = []

    for i in range(0, len(plaintext_vector), size):
        block = np.array(plaintext_vector[i:i+size])
        encrypted_block = np.dot(key, block) % ALPHABET_SIZE
        encrypted_vector.extend(encrypted_block)

    return vector_to_text(encrypted_vector)

def decrypt_message_hill(ciphertext: str, matrix_list: list) -> str:
    """
    Déchiffre un message en utilisant l'algorithme de Hill Cipher.
    """
    key = parse_matrix(matrix_list)
    size = key.shape[0]
    inverse_key = matrix_mod_inverse(key)
    ciphertext_vector = text_to_vector(ciphertext, size)
    decrypted_vector = []

    for i in range(0, len(ciphertext_vector), size):
        block = np.array(ciphertext_vector[i:i+size])
        decrypted_block = np.dot(inverse_key, block) % ALPHABET_SIZE
        decrypted_vector.extend(decrypted_block)

    return vector_to_text(decrypted_vector)
