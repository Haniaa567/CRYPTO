'''''
import numpy as np
from sympy import Matrix, mod_inverse
import itertools

# Fréquences des lettres en français
FRENCH_LETTER_FREQ = {
    'E': 0.1772, 'A': 0.0812, 'I': 0.0729, 'N': 0.0691, 'R': 0.0643,
    'S': 0.0630, 'O': 0.0632, 'T': 0.0696, 'L': 0.0496, 'U': 0.0628,
    'D': 0.0350, 'C': 0.0318, 'M': 0.0261, 'P': 0.0246, 'G': 0.0127,
    'B': 0.0119, 'V': 0.0111, 'H': 0.0110, 'F': 0.0110, 'Q': 0.0065,
    'W': 0.0018, 'Z': 0.0016, 'X': 0.0037, 'J': 0.0034, 'Y': 0.0024, 
    'K': 0.0008
}

# Fréquences des lettres en anglais
ENGLISH_LETTER_FREQ = {
    'E': 0.127, 'T': 0.0906, 'A': 0.0817, 'O': 0.0751, 'I': 0.0697,
    'N': 0.0675, 'S': 0.0633, 'H': 0.0609, 'R': 0.0599, 'D': 0.0425,
    'L': 0.0403, 'C': 0.0278, 'U': 0.0276, 'M': 0.0241, 'W': 0.0236,
    'F': 0.0223, 'G': 0.0202, 'Y': 0.0197, 'P': 0.0193, 'B': 0.0149,
    'V': 0.0098, 'K': 0.0077, 'J': 0.0015, 'X': 0.0015, 'Q': 0.0009,
    'Z': 0.0007
}

def letter_to_number(letter):
    return ord(letter.upper()) - ord('A')

def number_to_letter(number):
    return chr(number % 26 + ord('A'))

def is_invertible_mod26(matrix):
    """Vérification rigoureuse de l'inversibilité modulo 26"""
    m = Matrix(matrix)
    det = m.det()
    try:
        mod_inverse(int(det) % 26, 26)
        return True
    except ValueError:
        return False

def matrix_mod_inverse(matrix, modulus=26):
    """Calcul de l'inverse modulaire d'une matrice"""
    m = Matrix(matrix)
    det = m.det()

    det_mod = int(det) % modulus
    det_inv = mod_inverse(det_mod, modulus)
    adj = m.adjugate()

    inv = (det_inv * adj) % modulus
    return np.array(inv).astype(int)

def calculate_text_freq(text):
    """Calculer la fréquence des lettres dans un texte"""
    total = len(text)
    freq = {}
    for char in text.upper():
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1 / total
    return freq

def score_decryption(decrypted_text, language='fr'):  # Ajout d'une option de langue
    """Scorer la qualité du déchiffrement basé sur la fréquence des lettres"""
    decrypted_freq = calculate_text_freq(decrypted_text)
    if language == 'en':
        letter_freq = ENGLISH_LETTER_FREQ
    else:
        letter_freq = FRENCH_LETTER_FREQ

    score = 0
    for char, freq in decrypted_freq.items():
        score += abs(freq - letter_freq.get(char, 0))
    return -score  # Score négatif pour minimiser la différence

def decrypt_Hill(ciphertext, key, block_size):
    """Déchiffrement avec la clé de Hill"""
    cipher_nums = np.array([letter_to_number(c) for c in ciphertext])
    cipher_nums = cipher_nums.reshape((len(cipher_nums) // block_size, block_size)).T

    key_inv = matrix_mod_inverse(key)

    decrypted_nums = (np.dot(key_inv, cipher_nums) % 26).T.flatten()

    decrypted_text = ''.join([number_to_letter(num) for num in decrypted_nums])

    return decrypted_text

def blind_attack_Hill(ciphertext, block_size=2, top_n=3, language='fr'):
    """Attaque aveugle du chiffrement de Hill avec les top N résultats"""

    # Vérifier si la taille du texte est compatible avec le bloc
    if len(ciphertext) % block_size != 0:
        raise ValueError("La taille du texte chiffré doit être un multiple de la taille du bloc.")

    possible_decryptions = []

    # Générer des clés potentielles
    for key_values in itertools.product(range(26), repeat=block_size*block_size):
        key = np.array(key_values).reshape((block_size, block_size))

        # Vérifier l'inversibilité de la clé
        if not is_invertible_mod26(key):
            continue

        try:
            # Déchiffrer avec la clé
            decrypted_text = decrypt_Hill(ciphertext, key, block_size)

            # Scorer le déchiffrement
            score = score_decryption(decrypted_text, language)

            # Stocker le résultat
            possible_decryptions.append({
                'key': key,
                'decrypted_text': decrypted_text,
                'score': score
            })

        except Exception:
            continue

    # Trier les déchiffrements par score
    possible_decryptions.sort(key=lambda x: x['score'], reverse=True)

    return possible_decryptions[:top_n]

def main():
    # Liste des ciphertexts à tester
    ciphertext ="KZGNVXCHQWMY"
    block_size = 3

    try:
        # Obtenir les 10 meilleures possibilités
        top_decryptions = blind_attack_Hill(ciphertext, block_size, language='en')

        # Afficher les résultats
        for i, result in enumerate(top_decryptions, 1):
            print(f"\nPossibilité {i} (Score : {result['score']:.4f}):")
            print("Clé :")
            print(result['key'])
            print("Texte déchiffré :", result['decrypted_text'])
    except ValueError as e:
        print("Erreur :", e)

if __name__ == "__main__":
    main()

'''
import numpy as np
from sympy import Matrix, mod_inverse
import itertools
import json

# Fréquences des lettres en français
FRENCH_LETTER_FREQ = {
    'E': 0.1772, 'A': 0.0812, 'I': 0.0729, 'N': 0.0691, 'R': 0.0643,
    'S': 0.0630, 'O': 0.0632, 'T': 0.0696, 'L': 0.0496, 'U': 0.0628,
    'D': 0.0350, 'C': 0.0318, 'M': 0.0261, 'P': 0.0246, 'G': 0.0127,
    'B': 0.0119, 'V': 0.0111, 'H': 0.0110, 'F': 0.0110, 'Q': 0.0065,
    'W': 0.0018, 'Z': 0.0016, 'X': 0.0037, 'J': 0.0034, 'Y': 0.0024, 
    'K': 0.0008
}

# Fréquences des lettres en anglais
ENGLISH_LETTER_FREQ = {
    'E': 0.127, 'T': 0.0906, 'A': 0.0817, 'O': 0.0751, 'I': 0.0697,
    'N': 0.0675, 'S': 0.0633, 'H': 0.0609, 'R': 0.0599, 'D': 0.0425,
    'L': 0.0403, 'C': 0.0278, 'U': 0.0276, 'M': 0.0241, 'W': 0.0236,
    'F': 0.0223, 'G': 0.0202, 'Y': 0.0197, 'P': 0.0193, 'B': 0.0149,
    'V': 0.0098, 'K': 0.0077, 'J': 0.0015, 'X': 0.0015, 'Q': 0.0009,
    'Z': 0.0007
}
'''''
def load_hill_matrices(input_file='hill_matrices.json'):
    """
    Charge les matrices de Hill à partir d'un fichier JSON
    
    Args:
    - input_file (str): Fichier contenant les matrices
    
    Returns:
    - list: Liste des matrices chargées
    """
    try:
        with open(input_file, 'r') as f:
            matrices = json.load(f)
        return [np.array(matrix) for matrix in matrices]
    except FileNotFoundError:
        print(f"Fichier {input_file} non trouvé. Générez d'abord les matrices.")
        return []
'''
def letter_to_number(letter):
    return ord(letter.upper()) - ord('A')

def number_to_letter(number):
    return chr(number % 26 + ord('A'))

def is_invertible_mod26(matrix):
    """Vérification rigoureuse de l'inversibilité modulo 26"""
    m = Matrix(matrix)
    det = m.det()
    try:
        mod_inverse(int(det) % 26, 26)
        return True
    except ValueError:
        return False

def matrix_mod_inverse(matrix, modulus=26):
    """Calcul de l'inverse modulaire d'une matrice"""
    m = Matrix(matrix)
    det = m.det()

    det_mod = int(det) % modulus
    det_inv = mod_inverse(det_mod, modulus)
    adj = m.adjugate()

    inv = (det_inv * adj) % modulus
    return np.array(inv).astype(int)

def calculate_text_freq(text):
    """Calculer la fréquence des lettres dans un texte"""
    total = len(text)
    freq = {}
    for char in text.upper():
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1 / total
    return freq

def score_decryption(decrypted_text, language='fr'):
    """Scorer la qualité du déchiffrement basé sur la fréquence des lettres"""
    decrypted_freq = calculate_text_freq(decrypted_text)
    if language == 'en':
        letter_freq = ENGLISH_LETTER_FREQ
    else:
        letter_freq = FRENCH_LETTER_FREQ

    score = 0
    for char, freq in decrypted_freq.items():
        score += abs(freq - letter_freq.get(char, 0))
    return -score

def decrypt_Hill(ciphertext, key, block_size):
    """Déchiffrement avec la clé de Hill"""
    cipher_nums = np.array([letter_to_number(c) for c in ciphertext])
    cipher_nums = cipher_nums.reshape((len(cipher_nums) // block_size, block_size)).T

    key_inv = matrix_mod_inverse(key)

    decrypted_nums = (np.dot(key_inv, cipher_nums) % 26).T.flatten()

    decrypted_text = ''.join([number_to_letter(num) for num in decrypted_nums])

    return decrypted_text

'''''
def blind_attack_Hill(ciphertext, block_size=2, top_n=20, language='fr'):
    """Attaque aveugle du chiffrement de Hill avec les top N résultats"""

    # Vérifier si la taille du texte est compatible avec le bloc
    if len(ciphertext) % block_size != 0:
        raise ValueError("La taille du texte chiffré doit être un multiple de la taille du bloc.")

    possible_decryptions = []

    # Pour les blocs de taille 3, utiliser les matrices précalculées
    if block_size == 3:
        matrices = load_hill_matrices()
        if not matrices:
            # Revenir à la génération de matrices si le fichier n'est pas trouvé
            key_generation = itertools.product(range(26), repeat=block_size*block_size)
    else:
        # Pour les blocs de taille 2, utiliser la méthode originale
        key_generation = itertools.product(range(26), repeat=block_size*block_size)
        matrices = None

    # Sélectionner la source de clés
    if matrices:
        key_generation = matrices
    
    # Générer des clés potentielles
    for key_values in key_generation:
        key = np.array(key_values).reshape((block_size, block_size))

        # Vérifier l'inversibilité de la clé
        if not is_invertible_mod26(key):
            continue

        try:
            # Déchiffrer avec la clé
            decrypted_text = decrypt_Hill(ciphertext, key, block_size)

            # Scorer le déchiffrement
            score = score_decryption(decrypted_text, language)

            # Stocker le résultat
            possible_decryptions.append({
                'key': key,
                'decrypted_text': decrypted_text,
                'score': score
            })

        except Exception:
            continue

    # Trier les déchiffrements par score
    possible_decryptions.sort(key=lambda x: x['score'], reverse=True)

    return possible_decryptions[:top_n]
'''
def load_hill_matrices(block_size=3):
    """
    Charge les matrices de Hill à partir d'un fichier JSON
    
    Args:
    - block_size (int): Taille du bloc (2 ou 3)
    
    Returns:
    - list: Liste des matrices chargées
    """
    # Choisir le fichier en fonction de la taille du bloc
    if block_size == 3:
        input_file = 'hill_matrices.json'
    elif block_size == 2:
        input_file = 'hill_matrices_2x2.json'
    else:
        print("Taille de bloc non supportée. Utilisez 2 ou 3.")
        return []

    try:
        with open(input_file, 'r') as f:
            matrices = json.load(f)
        return [np.array(matrix) for matrix in matrices]
    except FileNotFoundError:
        print(f"Fichier {input_file} non trouvé. Veuillez générer les matrices.")
        return []

def blind_attack_Hill(ciphertext, block_size=2, top_n=20, language='fr'):
    """Attaque aveugle du chiffrement de Hill avec les top N résultats"""

    # Vérifier si la taille du texte est compatible avec le bloc
    if len(ciphertext) % block_size != 0:
        raise ValueError("La taille du texte chiffré doit être un multiple de la taille du bloc.")

    possible_decryptions = []

    # Charger les matrices spécifiques à la taille du bloc
    matrices = load_hill_matrices(block_size)
    
    # Si pas de matrices chargées, revenir à la génération de clés
    if not matrices:
        key_generation = itertools.product(range(26), repeat=block_size*block_size)
    else:
        key_generation = matrices
    
    # Générer des clés potentielles
    for key_values in key_generation:
        key = np.array(key_values).reshape((block_size, block_size))

        # Vérifier l'inversibilité de la clé
        if not is_invertible_mod26(key):
            continue

        try:
            # Déchiffrer avec la clé
            decrypted_text = decrypt_Hill(ciphertext, key, block_size)

            # Scorer le déchiffrement
            score = score_decryption(decrypted_text, language)

            # Stocker le résultat
            possible_decryptions.append({
                'key': key,
                'decrypted_text': decrypted_text,
                'score': score
            })

        except Exception:
            continue

    # Trier les déchiffrements par score
    possible_decryptions.sort(key=lambda x: x['score'], reverse=True)

    return possible_decryptions[:top_n]
def main():
    # Liste des ciphertexts à tester
    #ciphertext ="KZGNVXCHQWMY"
    #block_size = 3
    ciphertext = "XIYVCWUM"
    block_size = 2
    try:
        # Obtenir les 10 meilleures possibilités
        top_decryptions = blind_attack_Hill(ciphertext, block_size, language='fr')

        # Afficher les résultats
        for i, result in enumerate(top_decryptions, 1):
            print(f"\nPossibilité {i} (Score : {result['score']:.4f}):")
            print("Clé :")
            print(result['key'])
            print("Texte déchiffré :", result['decrypted_text'])
    except ValueError as e:
        print("Erreur :", e)

if __name__ == "__main__":
    main()