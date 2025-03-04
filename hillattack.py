import numpy as np
from collections import Counter
import itertools

# --- Étape 1 : Définir les paramètres de la langue (fréquences) ---
# Digrammes les plus fréquents en français
frequent_digrams = ["ES", "DE", "LE", "EN", "RE", "ET", "LA"]

# --- Étape 2 : Fonction d'encodage des lettres en nombres ---
def letter_to_number(text):
    return [ord(char) - ord('A') for char in text]

def number_to_letter(numbers):
    return ''.join(chr(n + ord('A')) for n in numbers)

# --- Étape 3 : Analyser la fréquence des digrammes ---
def find_frequent_digrams(ciphertext):
    digrams = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    return Counter(digrams).most_common(5)

# --- Étape 4 : Résoudre l'équation matricielle ---
# Inversion modulaire (mod 26)
def mod_inverse_matrix(matrix, mod):
    det = int(round(np.linalg.det(matrix)))
    det_inv = pow(det, -1, mod)  # Inverse modulaire du déterminant
    adjugate = np.round(det * np.linalg.inv(matrix)).astype(int) % mod
    return (det_inv * adjugate) % mod

# --- Étape 5 : Déchiffrement avec une matrice ---
def decrypt_hill(ciphertext, key_matrix):
    plaintext = []
    ciphertext_numbers = letter_to_number(ciphertext)

    for i in range(0, len(ciphertext_numbers), len(key_matrix)):
        block = np.array(ciphertext_numbers[i:i+len(key_matrix)])
        decrypted_block = np.dot(mod_inverse_matrix(key_matrix, 26), block) % 26
        plaintext.extend(decrypted_block)

    return number_to_letter(plaintext)

# --- Étape 6 : Brute-force des digrammes ---
def attack_hill(ciphertext):
    cipher_digrams = find_frequent_digrams(ciphertext)
    print(f"Digrammes fréquents : {cipher_digrams}")

    for digram_pair in itertools.permutations(frequent_digrams, 2):
        print(f"Test avec : {digram_pair}")
        try:
            P = np.array([letter_to_number(digram_pair[0]),
                          letter_to_number(digram_pair[1])]).T
            C = np.array([letter_to_number(cipher_digrams[0][0]),
                          letter_to_number(cipher_digrams[1][0])]).T

            key_matrix = np.dot(C, mod_inverse_matrix(P, 26)) % 26
            print(f"Matrice candidate : \n{key_matrix}")

            plaintext = decrypt_hill(ciphertext, key_matrix)
            print(f"Tentative : {plaintext}")

        except Exception as e:
            continue

# --- Exemple d'utilisation ---
ciphertext = "GZATZXJIHVBREOSU"
attack_hill(ciphertext)
