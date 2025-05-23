import string

# Alphabet utilisé
ALPHABET = string.ascii_uppercase

# Définition des rotors (substitutions fixes)
ROTORS = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
    "BDFHJLCPRTXVZNYEIWGAKMUSQO"   # Rotor III
]

# Réflecteur (permutation des lettres)
REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Fonction pour faire tourner les rotors
def rotate_rotors(positions):
    positions[0] = (positions[0] + 1) % 26
    if positions[0] == 0:  # Si le premier rotor a fait un tour, on tourne le deuxième
        positions[1] = (positions[1] + 1) % 26
        if positions[1] == 0:  # Si le deuxième a fait un tour, on tourne le troisième
            positions[2] = (positions[2] + 1) % 26

# Fonction pour passer une lettre à travers un rotor
def pass_through_rotor(letter, rotor, position, reverse=False):
    index = ALPHABET.index(letter)
    if not reverse:
        shifted_index = (index + position) % 26
        substituted_letter = rotor[shifted_index]
        final_index = (ALPHABET.index(substituted_letter) - position) % 26
    else:
        shifted_index = (ALPHABET.index(letter) + position) % 26
        substituted_index = rotor.index(ALPHABET[shifted_index])
        final_index = (substituted_index - position) % 26
    
    return ALPHABET[final_index]

# Fonction de chiffrement/déchiffrement Enigma
def enigma(text, initial_positions):
    text = text.upper().replace(" ", "")  # On enlève les espaces
    result = ""
    positions = initial_positions[:]  # Copie des positions initiales pour ne pas modifier l'original

    for letter in text:
        if letter not in ALPHABET:
            result += letter  # On garde les caractères non alphabétiques
            continue
        
        # Faire tourner les rotors avant chaque lettre
        rotate_rotors(positions)

        # Passer par les rotors dans l'ordre
        for i in range(3):
            letter = pass_through_rotor(letter, ROTORS[i], positions[i])

        # Passer par le réflecteur
        letter = REFLECTOR[ALPHABET.index(letter)]

        # Passer par les rotors en sens inverse
        for i in range(2, -1, -1):
            letter = pass_through_rotor(letter, ROTORS[i], positions[i], reverse=True)

        result += letter

    return result

# Exemple d'utilisation avec positions initiales fixées
message = "HELLOENIGMA"
initial_positions = [0, 0, 0]  # Position initiale des rotors (clé secrète)

encrypted = enigma(message, initial_positions)
decrypted = enigma(encrypted, initial_positions)  # Réinitialisation correcte

print(f"Message original : {message}")
print(f"Message chiffré : {encrypted}")
print(f"Message déchiffré : {decrypted}")

