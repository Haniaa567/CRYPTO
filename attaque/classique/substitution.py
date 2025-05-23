import random

# Déclaration globale de l'alphabet
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Fonction d'encodage (substitution)
def encode(message, key):
    message = message.upper()
    secret = ""

    for letter in message:
        spot = ALPHABET.find(letter)
        if spot >= 0:
            secret += key[spot]  # Remplace la lettre par celle de la clé
        else:
            secret += letter  # Garde les caractères non alphabétiques

    return secret

# Fonction de décodage (retrouver le texte original)
def decode(message, key):
    plaintext = ""

    for letter in message:
        spot = key.find(letter)  # Cherche la position de la lettre dans la clé
        if spot >= 0:
            plaintext += ALPHABET[spot]  # Remplace par la lettre d'origine
        else:
            plaintext += letter  # Garde les caractères non alphabétiques

    return plaintext

# Génération d'une clé basée sur un mot de passe
def generatePasswordKey(password=""):
    password = password.upper()
    key = ""

    for letter in password:
        if letter not in key:
            key += letter

    for letter in ALPHABET:
        if letter not in key:
            key += letter

    return key

# Génération d'une clé aléatoire
def generateRandomKey():
    alpha_list = list(ALPHABET)
    random.shuffle(alpha_list)
    return "".join(alpha_list)

# Fonction principale
def main():
    print("Méthode de Substitution Aléatoire\n")

    mode = input("Voulez-vous générer une clé aléatoire (A) ou avec un mot de passe (P) ? ").strip().upper()
    if mode == "A":
        key = generateRandomKey()
    elif mode == "P":
        password = input("Entrez un mot de passe pour générer la clé : ")
        key = generatePasswordKey(password)
    else:
        print("Choix invalide.")
        return

    print(f"\nClé générée : {key}\n")

    message = input("Entrez un message : ")
    
    secret = encode(message, key)
    print("Message chiffré :", secret)

    plaintext = decode(secret, key)
    print("Message déchiffré :", plaintext)

if __name__ == "__main__":
    main()
