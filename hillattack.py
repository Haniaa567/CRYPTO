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

def score_decryption(decrypted_text):
    """Scorer la qualité du déchiffrement basé sur la fréquence des lettres"""
    decrypted_freq = calculate_text_freq(decrypted_text)
    score = 0
    for char, freq in decrypted_freq.items():
        score += abs(freq - FRENCH_LETTER_FREQ.get(char, 0))
    return -score  # Score négatif pour minimiser la différence

def decrypt_Hill(ciphertext, key, block_size):
    """Déchiffrement avec la clé de Hill"""
    cipher_nums = np.array([letter_to_number(c) for c in ciphertext])
    cipher_nums = cipher_nums.reshape((len(cipher_nums) // block_size, block_size)).T
    
    key_inv = matrix_mod_inverse(key)
    
    decrypted_nums = (np.dot(key_inv, cipher_nums) % 26).T.flatten()
    
    decrypted_text = ''.join([number_to_letter(num) for num in decrypted_nums])
    
    return decrypted_text

def blind_attack_Hill(ciphertext, block_size=2, top_n=10):
    """Attaque aveugle du chiffrement de Hill avec les top N résultats"""
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
            score = score_decryption(decrypted_text)
            
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
    ciphertext ="XECLTZ"
    block_size = 2



    # Obtenir les 10 meilleures possibilités
    top_decryptions = blind_attack_Hill(ciphertext, block_size)
        
        # Afficher les résultats
    for i, result in enumerate(top_decryptions, 1):
            print(f"\nPossibilité {i} (Score : {result['score']:.4f}):")
            print("Clé :")
            print(result['key'])
            print("Texte déchiffré :", result['decrypted_text'])

if __name__ == "__main__":
    main()