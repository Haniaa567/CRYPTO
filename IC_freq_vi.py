MAX_KEY_LENGTH_GUESS = 20
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# Tableau des fréquences relatives des lettres en anglais
english_frequences = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
]

def get_index_c(ciphertext):
    """
    Calcule l'Index de Coïncidence pour un segment de texte.
    """
    N = float(len(ciphertext))
    if N < 2:
        return 0.0
    frequency_sum = 0.0
    for letter in alphabet:
        frequency_sum += ciphertext.count(letter) * (ciphertext.count(letter) - 1)
    ic = frequency_sum / (N * (N - 1))
    return ic

def get_key_length(ciphertext):
    """
    Détermine la longueur de clé la plus probable en se basant sur l'Index de Coïncidence.
    Renvoie un seul entier (longueur de clé la plus probable).
    """
    ic_table = []

    for guess_len in range(MAX_KEY_LENGTH_GUESS):
        ic_sum = 0.0
        avg_ic = 0.0
        # On découpe le texte en sequences pour ce guess_len
        for i in range(guess_len):
            sequence = ""
            for j in range(0, len(ciphertext[i:]), guess_len):
                sequence += ciphertext[i + j]
            ic_sum += get_index_c(sequence)

        if guess_len != 0:
            avg_ic = ic_sum / guess_len

        ic_table.append(avg_ic)

    # Les 2 meilleurs indices de coïncidence
    sorted_ic = sorted(ic_table, reverse=True)
    best_guess = ic_table.index(sorted_ic[0])
    second_best_guess = ic_table.index(sorted_ic[1])

    # Évite la confusion entre ex: 3 et 6 (clé dupliquée)
    if best_guess != 0 and second_best_guess != 0 and best_guess % second_best_guess == 0:
        return second_best_guess
    else:
        return best_guess

def freq_analysis_all(sequence):
    """
    Retourne un classement de toutes les lettres possibles (a-z) pour ce segment,
    triées du chi-carré le plus faible (meilleure correspondance) au plus élevé (moins bonne).
    """
    all_chi = []
    length_seq = float(len(sequence))

    for i in range(26):
        # On décale chaque lettre de i
        shifted_seq = []
        for ch in sequence:
            shifted_seq.append(chr(((ord(ch) - 97 - i) % 26) + 97))

        # On compte la fréquence de chaque lettre
        freq = [0] * 26
        for c in shifted_seq:
            freq[ord(c) - ord('a')] += 1

        # On normalise
        for j in range(26):
            freq[j] /= length_seq if length_seq else 1

        # Calcul du chi-carré
        chi_squared_sum = 0.0
        for j in range(26):
            chi_squared_sum += ((freq[j] - english_frequences[j]) ** 2) / (english_frequences[j] + 1e-9)

        # (lettre_clé, chi²)
        all_chi.append((chr(i + 97), chi_squared_sum))

    # Tri par chi-carré croissant
    all_chi.sort(key=lambda x: x[1])
    return all_chi  # [(lettre, chi²), (lettre, chi²), ...]

def get_all_keys(ciphertext, key_length, top_n=20):
    """
    Retourne TOUTES les clés possibles en combinant les 'top_n' lettres
    les plus probables pour chaque position.
    """
    from itertools import product
    ciphertext = ''.join(ch for ch in ciphertext if ch.isalpha()).lower()

    positions_letters = []
    for i in range(key_length):
        sequence = ""
        for j in range(0, len(ciphertext[i:]), key_length):
            sequence += ciphertext[i + j]

        ranked_letters = freq_analysis_all(sequence)
        # On prend seulement les 'top_n' lettres les plus probables
        best_letters = [ranked_letters[k][0] for k in range(min(top_n, len(ranked_letters)))]
        positions_letters.append(best_letters)

    # Produit cartésien de toutes les lettres pour chaque position
    all_keys = []
    for combo in product(*positions_letters):
        all_keys.append(''.join(combo))
    return all_keys

def decrypt(ciphertext, key):
    cipher_ascii = [ord(letter) for letter in ciphertext]
    key_ascii = [ord(letter) for letter in key]
    plain_ascii = []
    for i in range(len(cipher_ascii)):
        plain_ascii.append(((cipher_ascii[i] - key_ascii[i % len(key)]) % 26) + 97)
    plaintext = ''.join(chr(i) for i in plain_ascii)
    return plaintext

def encrypt(plaintext, key):
    plain_ascii = [ord(letter) for letter in plaintext]
    key_ascii = [ord(letter) for letter in key]
    cipher_ascii = []
    for i in range(len(plain_ascii)):
        temp = plain_ascii[i] + key_ascii[i % len(key)] - 97
        if temp > 122:
            cipher_ascii.append(temp - 26)
        else:
            cipher_ascii.append(temp)
    ciphertext = ''.join(chr(i) for i in cipher_ascii)
    return ciphertext

def main():
    while True:
        mode = input("Enter e to encrypt, or d to decrypt: ").strip().lower()
        if mode == 'e':
            plaintext_unfiltered = input("Enter plaintext to encrypt: ")
            key_unfiltered = input("Enter key to encrypt with: ")
            plaintext = ''.join(x.lower() for x in plaintext_unfiltered if x.isalpha())
            key = ''.join(x.lower() for x in key_unfiltered if x.isalpha())

            ciphertext = encrypt(plaintext, key)
            print(f"Ciphertext: {ciphertext}")
            break

        elif mode == 'd':
            ciphertext_unfiltered = input("Enter ciphertext to decrypt: ")
            ciphertext = ''.join(x.lower() for x in ciphertext_unfiltered if x.isalpha())

            known_key = input("Do you know the key? (y/n) : ").strip().lower()
            if known_key == 'y':
                key_unfiltered = input("Enter key: ")
                key = ''.join(x.lower() for x in key_unfiltered if x.isalpha())
                plaintext = decrypt(ciphertext, key)
                print(f"Plaintext: {plaintext}")
            else:
                # On devine la longueur de la clé
                length_guess = get_key_length(ciphertext)
                print(f"Likely key length: {length_guess}")

                # On récupère toutes les clés possibles (top 5 lettres par position)
                possible_keys = get_all_keys(ciphertext, length_guess, top_n=5)

                # On enregistre dans un fichier au lieu d'afficher dans le terminal
                filename = "all_possible_keys.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for k in possible_keys:
                        plain = decrypt(ciphertext, k)
                        f.write(f"Key: {k}, Plaintext: {plain}\n")

                print(f"\nLes {len(possible_keys)} clés possibles ont été enregistrées dans '{filename}'.\n")

            break
        else:
            print("Invalid input, please enter 'e' or 'd'.")

if __name__ == "__main__":
    main()
