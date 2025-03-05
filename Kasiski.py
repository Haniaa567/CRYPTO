import re
from collections import Counter

def preprocess_text(text):
    """Nettoie le texte et ne garde que les lettres majuscules."""
    return re.sub(r'[^A-Z]', '', text.upper())

def find_repeated_sequences(ciphertext, min_length=3):
    """Trouve les séquences répétées et leurs positions dans le texte chiffré."""
    sequences = {}
    for i in range(len(ciphertext) - min_length):
        seq = ciphertext[i:i+min_length]
        if seq in sequences:
            sequences[seq].append(i)
        else:
            sequences[seq] = [i]

    return {seq: positions for seq, positions in sequences.items() if len(positions) > 1}

def kasiski_test(ciphertext, min_length=3):
    """Applique le test de Kasiski pour estimer la longueur de la clé."""
    ciphertext = preprocess_text(ciphertext)
    repeated_sequences = find_repeated_sequences(ciphertext, min_length)

    distances = []
    for positions in repeated_sequences.values():
        for j in range(1, len(positions)):
            distances.append(positions[j] - positions[j-1])

    if not distances:
        print("❌ Aucune séquence répétée trouvée. Le test de Kasiski ne fonctionne pas.")
        return []

    # Comptage des facteurs des distances
    factors = Counter()
    for d in distances:
        for f in range(2, d + 1):  # On commence à 2 car 1 n'est pas un facteur utile
            if d % f == 0:
                factors[f] += 1

    # Retourne les longueurs de clé les plus probables
    probable_lengths = [k for k, v in factors.most_common(5)]
    return probable_lengths

# Exemple d'utilisation :
if __name__ == "__main__":
    texte_chiffre = "XPOJSVVGJZDUKSIYIUMZIESIXXZUWLQSXGMTLHATLWFLTFRVXJVLJIZJHPMJYYINSUFSUEPZTFUIIOPMWJHYGZBNTEHGSMCJIGKJMIJLBTPRSIRINJZDUKSIYIUMZIOVLJWEI"  # Exemple chiffré
    resultats = kasiski_test(texte_chiffre)

    print("\n🔍 Longueurs de clé probables :", resultats)

