import string
from collections import Counter

# Fréquences moyennes des lettres en anglais
FREQ_EN = "etaoinshrdlcumwfgypbvkjxqz"
COMMON_WORDS = ["the", "and", "that", "have", "for", "not", "with", "you", "this", "but"]

def analyse_frequentielle(texte):
    """Analyse fréquentielle avec ajustement basé sur digrammes et trigrammes."""
    
    texte = texte.upper()
    texte = ''.join(c for c in texte if c in string.ascii_uppercase)  # Filtrer les lettres
    nb_total = len(texte)
    
    # Calcul des fréquences des lettres dans le texte chiffré
    compteur = Counter(texte)
    frequences = {lettre: compteur[lettre] / nb_total for lettre in compteur}
    
    # Trier les lettres du texte chiffré par ordre décroissant de fréquence
    lettres_triees = sorted(frequences, key=frequences.get, reverse=True)
    
    # Création du dictionnaire de correspondance initial
    substitution = {chiffre: clair for chiffre, clair in zip(lettres_triees, FREQ_EN)}
    
    # Génération d'un texte partiellement déchiffré
    texte_dechiffre = ''.join(substitution.get(c, c) for c in texte)
    
    # Ajustement basé sur les mots courants
    for mot in COMMON_WORDS:
        if mot in texte_dechiffre:
            continue
        for chiffre, clair in substitution.items():
            if clair in mot and chiffre not in texte_dechiffre:
                texte_dechiffre = texte_dechiffre.replace(chiffre, clair)
    
    return texte_dechiffre, substitution

# ========== TEST ==========
texte_chiffre = input("Entrez le texte chiffré : ")
dechiffre, correspondances = analyse_frequentielle(texte_chiffre)

print("\n Texte partiellement déchiffré :")
print(dechiffre)
print("\n Correspondances initiales :")
for chif, clair in correspondances.items():
    print(f"{chif} → {clair}", end="  ")
print("\n")
