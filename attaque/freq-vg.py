import string
from collections import Counter
from itertools import product

# Alphabet en minuscules
alphabet = string.ascii_lowercase

# Fréquences relatives des lettres en anglais (pour le chi-carré)
english_frequencies = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228,
    0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025,
    0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987,
    0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
]
french_frequencies = [
    0.0764, 0.0090, 0.0326, 0.0367, 0.1472, 0.0106, 0.0110, 0.0074, 0.0759, 
    0.0061, 0.0005, 0.0546, 0.0297, 0.0712, 0.0576, 0.0252, 0.0136, 0.0669, 
    0.0795, 0.0724, 0.0631, 0.0183, 0.0004, 0.0042, 0.0028, 0.0012
]


################################
# 1) PRÉTRAITEMENT & CHIFFRES  #
################################

def preprocess(text):
    """
    Met le texte en minuscules et enlève tout caractère non-alpha.
    """
    return ''.join(ch.lower() for ch in text if ch.isalpha())

def encrypt_vigenere(plaintext, key):
    cipher = []
    key_len = len(key)
    for i, p in enumerate(plaintext):
        shift = ord(key[i % key_len]) - ord('a')
        c = (ord(p) - ord('a') + shift) % 26
        cipher.append(chr(c + ord('a')))
    return ''.join(cipher)

def decrypt_vigenere(ciphertext, key):
    plain = []
    key_len = len(key)
    for i, c in enumerate(ciphertext):
        shift = ord(key[i % key_len]) - ord('a')
        p = (ord(c) - ord('a') - shift) % 26
        plain.append(chr(p + ord('a')))
    return ''.join(plain)

#######################################
# 2) DIVISION EN SOUS-TEXTES (CÉSAR)  #
#######################################

def split_into_subtexts(ciphertext, key_length):
    """
    Divise le texte en 'key_length' sous-textes, chacun chiffré par un décalage unique.
    """
    subtexts = ['' for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        subtexts[i % key_length] += char
    return subtexts

#############################################
# 3) ANALYSE FRÉQUENTIELLE & CALCUL CHI²    #
#############################################

def get_subtext_chi_scores(subtext):
    """
    Calcule le chi-carré pour chaque décalage possible (0 à 25) sur le sous-texte.
    Retourne une liste de tuples (shift, chi_value).
    """
    length = len(subtext)
    if length == 0:
        # Si le sous-texte est vide, on renvoie chi = 9999 pour tous, ou 0
        return [(shift, 9999.0) for shift in range(26)]

    # Compter la fréquence de chaque lettre du sous-texte
    count = Counter(subtext)
    observed = [count.get(chr(i + ord('a')), 0) for i in range(26)]

    results = []
    for shift in range(26):
        # Appliquer le décalage inverse 'shift' pour simuler un déchiffrement
        # puis comparer la distribution obtenue avec english_frequencies
        # => Observed freq of letter 'a' correspond à subtext letter = (a + shift) mod 26
        # On reconstruit la distribution
        # freq[i] => freq de la lettre i (0=a,1=b,...)
        freq = [0] * 26
        for i in range(26):
            # i = plaintext letter
            # (i + shift) % 26 = subtext letter
            sub_letter_index = (i + shift) % 26
            freq[i] = observed[sub_letter_index]

        # On normalise pour comparer aux english_frequencies
        chi = 0.0
        for i in range(26):
            expected = english_frequencies[i] * length  # * length => on compare nb occurrences, pas pourcentage
            diff = freq[i] - expected
            # Pour éviter la division par 0, on ajoute un epsilon
            chi += (diff * diff) / (expected + 1e-9)
        results.append((shift, chi))

    return results  # liste (shift, chi)

def get_top_shifts_for_subtext(subtext, top_n=5):
    """
    Retourne les top_n décalages (shift) les plus probables pour un sous-texte,
    triés par chi croissant.
    """
    scores = get_subtext_chi_scores(subtext)
    scores.sort(key=lambda x: x[1])  # tri par chi
    return scores[:top_n]

#############################################
# 4) GÉNÉRER TOUTES LES CLÉS & LEUR SCORE   #
#############################################

def get_all_keys_with_score(ciphertext, key_length, top_n=5):
    """
    Pour chaque position (0..key_length-1), on récupère les top_n shifts les plus probables.
    Puis on génère toutes les combinaisons (produit cartésien).
    Pour chaque clé candidate, on calcule un 'score total' = somme des chi des positions.
    Retourne une liste de (key, total_chi, plaintext).
    """
    # 1) Découper en sous-textes
    subtexts = split_into_subtexts(ciphertext, key_length)

    # 2) Récupérer top_n shifts par sous-texte
    top_shifts_per_position = []
    for sub in subtexts:
        best_shifts = get_top_shifts_for_subtext(sub, top_n=top_n)
        top_shifts_per_position.append(best_shifts)  # liste de (shift, chi)

    # 3) Générer toutes les combinaisons
    # product(*top_shifts_per_position) => ex. [ ( (shiftA, chiA), (shiftB, chiB), ... ), ... ]
    all_keys = []
    for combo in product(*top_shifts_per_position):
        # combo est un tuple de (shift, chi) pour chaque position
        # On calcule la somme des chi
        total_chi = sum(pair[1] for pair in combo)
        # On reconstruit la clé
        shifts = [pair[0] for pair in combo]
        key = ''.join(chr(s + ord('a')) for s in shifts)

        # On décrypte
        plain = decrypt_vigenere(ciphertext, key)
        all_keys.append((key, total_chi, plain))

    return all_keys

###################################
# 5) EXEMPLE D'UTILISATION (CLI)  #
###################################

def main():
    # Exemple: on prend un texte chiffré
    ciphertext = input("Entrez le texte chiffré (lettres uniquement) : ").strip()
    ciphertext = preprocess(ciphertext)

    # Suppose qu'on a déjà estimé la longueur de la clé (par ex. 5)
    key_length = int(input("Longueur de la clé (ex: 5) : "))

    # On veut 5 lettres par position => top_n=5
    # On va ensuite afficher seulement 5 meilleurs combos finaux => top_results=5
    top_n = 5
    top_results = 10

    # On récupère toutes les clés possibles + leur score + plaintext
    candidates = get_all_keys_with_score(ciphertext, key_length, top_n=top_n)

    # On trie par total_chi croissant (plus c'est petit, plus c'est proche de l'anglais)
    candidates.sort(key=lambda x: x[1])

    # 1) Afficher la clé la plus probable
    best_key, best_score, best_plain = candidates[0]
    print(f"\n=== Meilleure clé trouvée ===")
    print(f"Clé : {best_key}")
    print(f"Score (chi²) : {best_score:.2f}")
    print(f"Texte déchiffré : {best_plain}")

    # 2) Afficher un tableau des top_results
    print(f"\n=== Top {top_results} clés les plus proches de l'anglais ===")
    print(f"{'Clé':<15} | {'Chi²':<10} | Texte déchiffré")
    print("-"*60)
    for i in range(min(top_results, len(candidates))):
        k, sc, pl = candidates[i]
        print(f"{k:<15} | {sc:<10.2f} | {pl}")

if __name__ == "__main__":
    main()
