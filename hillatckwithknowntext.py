import numpy as np
from sympy import Matrix, mod_inverse

def letter_to_number(letter):
    return ord(letter.upper()) - ord('A')

def number_to_letter(number):
    return chr(number % 26 + ord('A'))

def pad_message(message, block_size):
    while len(message) % block_size != 0:
        message += 'X'
    return message

def is_invertible_mod26(matrix):
    """Vérification rigoureuse de l'inversibilité modulo 26"""
    m = Matrix(matrix)
    det = m.det()
    try:
        # Vérifier si le déterminant a un inverse modulaire
        mod_inverse(int(det) % 26, 26)
        return True
    except ValueError:
        return False

def matrix_mod_inverse(matrix, modulus=26):
    """Calcul de l'inverse modulaire d'une matrice"""
    m = Matrix(matrix)
    det = m.det()
    
    # Calcul du déterminant modulaire
    det_mod = int(det) % modulus
    
    # Calcul de l'inverse modulaire du déterminant
    det_inv = mod_inverse(det_mod, modulus)
    
    # Calcul de l'adjugate
    adj = m.adjugate()
    
    # Calcul de l'inverse modulaire de la matrice
    inv = (det_inv * adj) % modulus
    
    return np.array(inv).astype(int)

def attack_Hill(plaintext, ciphertext, m):
    """Attaque du chiffrement de Hill"""
    # Conversion des chaînes en tableaux numériques
    plaintext_nums = np.array([letter_to_number(c) for c in plaintext])
    ciphertext_nums = np.array([letter_to_number(c) for c in ciphertext])

    # Ajustement en matrice (bloc)
    plaintext_matrix = plaintext_nums.reshape((len(plaintext_nums) // m, m)).T
    ciphertext_matrix = ciphertext_nums.reshape((len(ciphertext_nums) // m, m)).T

    # Tester différentes sous-matrices jusqu'à trouver une inversible
    for i in range(len(plaintext_matrix[0])):
        for j in range(i+1, len(plaintext_matrix[0])):
            # Extraire une sous-matrice potentielle
            p_subset = plaintext_matrix[:, [i, j]]
            c_subset = ciphertext_matrix[:, [i, j]]

            # Vérifier l'inversibilité
            if is_invertible_mod26(p_subset):
                # Calculer l'inverse modulaire
                inv_p_subset = matrix_mod_inverse(p_subset)
                
                # Calculer la clé potentielle
                key = (np.dot(c_subset, inv_p_subset) % 26).astype(int)
                
                # Vérifier la clé
                if is_invertible_mod26(key):
                    return key

    raise Exception("Impossible de trouver une clé inversible")

def decrypt_Hill(ciphertext, key, m):
    """Déchiffrement avec la clé de Hill"""
    # Conversion du texte chiffré en nombres
    cipher_nums = np.array([letter_to_number(c) for c in ciphertext])
    cipher_nums = cipher_nums.reshape((len(cipher_nums) // m, m)).T
    
    # Calcul de l'inverse de la clé
    key_inv = matrix_mod_inverse(key)
    
    # Déchiffrement
    decrypted_nums = (np.dot(key_inv, cipher_nums) % 26).T.flatten()
    
    # Conversion en lettres
    decrypted_text = ''.join([number_to_letter(num) for num in decrypted_nums])
    
    return decrypted_text

# Exemple d'utilisation
def main():
    #plaintext = "HELLO"
    #ciphertext = "XECLTZ"
    plaintext="ATTACK"
    ciphertext="FTPAWK"
    

    block_size = 2

    # Padding des messages
    plaintext = pad_message(plaintext, block_size)
    ciphertext = pad_message(ciphertext, block_size)

    try:
        key = attack_Hill(plaintext, ciphertext, block_size)
        print("Clé retrouvée :")
        print(key)
        
        # Vérification du déchiffrement
        decrypted = decrypt_Hill(ciphertext, key, block_size)
        print("\nTexte déchiffré :", decrypted)
        print("Texte original  :", plaintext)
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()