import re
from collections import Counter
from itertools import cycle

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def preprocess_text(text):
    """Enlève les caractères non alphabétiques et met en majuscules."""
    return re.sub(r'[^A-Z]', '', text.upper())

def vigenere_encrypt(text, key):
    """Chiffre un texte avec Vigenère."""
    text, key = preprocess_text(text), preprocess_text(key)
    encrypted = ''.join(ALPHABET[(ALPHABET.index(t) + ALPHABET.index(k)) % 26] 
                        for t, k in zip(text, cycle(key)))
    return encrypted

def vigenere_decrypt(text, key):
    """Déchiffre un texte avec Vigenère."""
    text, key = preprocess_text(text), preprocess_text(key)
    decrypted = ''.join(ALPHABET[(ALPHABET.index(t) - ALPHABET.index(k)) % 26] 
                        for t, k in zip(text, cycle(key)))
    return decrypted

def kasiski_test(ciphertext, min_length=3):
    """Trouve les répétitions dans le texte chiffré et estime la longueur de la clé."""
    ciphertext = preprocess_text(ciphertext)
    sequences = {}
    
    for i in range(len(ciphertext) - min_length):
        seq = ciphertext[i:i+min_length]
        if seq in sequences:
            sequences[seq].append(i)
        else:
            sequences[seq] = [i]

    distances = []
    for seq, positions in sequences.items():
        if len(positions) > 1:
            for j in range(1, len(positions)):
                distances.append(positions[j] - positions[j-1])
    
    if not distances:
        return []

    factors = Counter()
    for d in distances:
        for f in range(2, d + 1):
            if d % f == 0:
                factors[f] += 1

    probable_lengths = [k for k, v in factors.most_common(5)]
    return probable_lengths

def index_of_coincidence(text):
    """Calcule l'indice de coïncidence du texte."""
    text = preprocess_text(text)
    n = len(text)
    freqs = Counter(text)
    return sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1)) if n > 1 else 0

def guess_key_length(ciphertext):
    """Tente de deviner la longueur de la clé en combinant Kasiski et IC."""
    possible_lengths = kasiski_test(ciphertext)
    
    if not possible_lengths:
        print("Aucune longueur de clé trouvée via Kasiski. Essai avec l'indice de coïncidence...")
        for l in range(1, 21):  # Tester différentes longueurs de clé
            segments = [''.join(ciphertext[i::l]) for i in range(l)]
            avg_ic = sum(index_of_coincidence(seg) for seg in segments) / l
            if 0.06 <= avg_ic <= 0.08:  # Intervalle typique du français et de l'anglais
                possible_lengths.append(l)

    return possible_lengths[:3]  # On garde les 3 longueurs les plus probables

def frequency_analysis(segment):
    """Identifie le décalage du chiffre de César dans un segment basé sur l'analyse fréquentielle."""
    freq_french = "ETAOINSHRDLCUMWFGYPBVKJXQZ"  # Ordre des lettres les plus fréquentes en français
    counts = Counter(segment)
    most_common_letter = counts.most_common(1)[0][0] if counts else 'E'
    
    shift = (ALPHABET.index(most_common_letter) - ALPHABET.index('E')) % 26
    return ALPHABET[shift]

def vigenere_break(ciphertext):
    """Essaye de casser le chiffre de Vigenère sans clé."""
    ciphertext = preprocess_text(ciphertext)
    key_lengths = guess_key_length(ciphertext)

    if not key_lengths:
        print("Impossible de déterminer la longueur de la clé.")
        return []

    results = []
    for key_length in key_lengths:
        key_guess = ''.join(frequency_analysis(ciphertext[i::key_length]) for i in range(key_length))
        decrypted_text = vigenere_decrypt(ciphertext, key_guess)
        results.append((key_guess, decrypted_text))

    return results

# Exemple d'utilisation :
if __name__ == "__main__":
    message = "LE MESSAGE SECRET EST CACHE ICI"
    key = "CLE"

    encrypted = vigenere_encrypt(message, key)
    print(f"🔒 Texte chiffré : {encrypted}")

    decrypted = vigenere_decrypt(encrypted, key)
    print(f"🔓 Texte déchiffré : {decrypted}")

    print("\n🔍 Cryptanalyse en cours...")
    probable_keys = vigenere_break(encrypted)

    print("\n🔑 Résultats probables :")
    for k, d in probable_keys:
        print(f"Clé : {k} → {d}")
