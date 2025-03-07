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

def matrix_mod_inverse(matrix):
    det = int(round(np.linalg.det(matrix))) % ALPHABET_SIZE
    inv_det = mod_inverse(det, ALPHABET_SIZE)
    if inv_det == -1:
        raise ValueError("La matrice n'est pas inversible modulo 26")
    adjugate = np.round(np.linalg.inv(matrix) * np.linalg.det(matrix)).astype(int)
    return (adjugate * inv_det) % ALPHABET_SIZE

def text_to_vector(text, size):
       
    initial_length = len(text)
    text = text.upper().replace(" ", "")
    while len(text) % size != 0:
        text += 'X'
    if len(text) > initial_length:  # Si on a ajouté des 'X'
        print(f"\n[INFO] Un ou plusieurs caractères 'X' ont été ajoutés pour compléter le bloc ({len(text) - initial_length} ajouté(s)).")
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

def saisir_matrice():
    while True:
        try:
            # Demander la taille de la matrice
            taille = int(input("Entrez la taille de la matrice (2 ou 3) : "))
            if taille not in [2, 3]:
                print("La taille doit être 2 ou 3.")
                continue

            # Saisie de la matrice
            matrice = []
            print(f"Entrez les {taille}x{taille} éléments de la matrice (valeurs entre 0 et 25) :")
            for i in range(taille):
                ligne = input(f"Ligne {i+1} (séparés par des espaces) : ").split()
                ligne = [int(x) % 26 for x in ligne]
                if len(ligne) != taille:
                    print(f"Vous devez entrer exactement {taille} éléments.")
                    break
                matrice.append(ligne)
            else:
                # Convertir en numpy array et vérifier l'inversibilité
                np_matrice = np.array(matrice)
                if is_inversible(np_matrice):
                    return np_matrice
                else:
                    print("La matrice n'est pas inversible modulo 26. Réessayez.")
        except ValueError:
            print("Entrée invalide. Utilisez des nombres entiers.")

def main():
    while True:
        # Menu principal
        print("\n--- Chiffrement de Hill ---")
        print("1. Chiffrer un message")
        print("2. Déchiffrer un message")
        print("3. Quitter")
        
        choix = input("Votre choix (1-3) : ")
        
        if choix == '3':
            break
        
        if choix not in ['1', '2']:
            print("Choix invalide.")
            continue
        
        # Saisie de la matrice de clé
        print("\nSaisie de la matrice de clé :")
        key = saisir_matrice()
        print("\nMatrice de clé :")
        print(key)
        
        # Saisie du message
        message = input("\nEntrez le message (lettres majuscules uniquement) : ").upper()
        
        try:
            if choix == '1':
                # Chiffrement
                message_chiffre = encrypt(message, key)
                print(f"\nMessage chiffré : {message_chiffre}")
            else:
                # Déchiffrement
                message_dechiffre = decrypt(message, key)
                print(f"\nMessage déchiffré : {message_dechiffre}")
        
        except Exception as e:
            print(f"Erreur : {e}")

if __name__ == "__main__":
    main()

