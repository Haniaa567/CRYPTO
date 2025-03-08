import string

def indice_de_coincidence(texte):
    """Calcule l'Indice de Coïncidence d'un texte."""
    texte = [c for c in texte.upper() if c in string.ascii_uppercase]  # Filtrer lettres majuscules
    nb = len(texte)
    
    if nb <= 1:
        return 0.0  # Éviter la division par zéro
    
    # Fréquences des lettres
    frequences = {c: 0 for c in string.ascii_uppercase}
    for lettre in texte:
        frequences[lettre] += 1
    
    # Calcul de l'IC
    IC = sum(f * (f - 1) for f in frequences.values()) / (nb * (nb - 1))
    return round(IC, 5)  # Arrondi à 5 décimales

def trouver_taille_cle(texte, max_taille=40):
    """Estime la taille de la clé en utilisant l'IC sur différents blocs."""
    texte = ''.join([c for c in texte.upper() if c in string.ascii_uppercase])  # Filtrer lettres
    
    if not texte:
        print("Erreur : le texte ne contient pas de lettres valides.")
        return []
    
    IC_global = indice_de_coincidence(texte)  # IC global du texte chiffré
    print("\nIndice de Coïncidence du texte :", IC_global)
    
    ic_values = {}
    for taille in range(1, max_taille + 1):
        blocs = ['' for _ in range(taille)]
        
        # Séparer le texte en blocs
        for i, c in enumerate(texte):
            blocs[i % taille] += c
        
        # Calcul de l'IC moyen des blocs
        ic_moyen = sum(indice_de_coincidence(bloc) for bloc in blocs) / taille
        ic_values[taille] = round(ic_moyen, 5)  # Arrondi à 5 décimales
        print(f"IC moyen pour taille {taille}: {ic_values[taille]:.5f}")
    
    # Détermination des tailles possibles
    moyenne_ic = sum(ic_values.values()) / len(ic_values)
    ecart_type = (sum((v - moyenne_ic) ** 2 for v in ic_values.values()) / len(ic_values)) ** 0.5
    seuil = moyenne_ic + ecart_type  # Seuil dynamique basé sur l'écart-type
    
    tailles_filtres = [k for k, v in ic_values.items() if v > seuil]
    
    # Filtre additionnel pour garder au moins 3 valeurs
    if len(tailles_filtres) < 3:
        tailles_filtres = sorted(ic_values, key=ic_values.get, reverse=True)[:3]
    
    return tailles_filtres

# ====================== TEST ======================
texte_chiffre = input("Entrez le texte chiffré : ").strip()

tailles = trouver_taille_cle(texte_chiffre)
print("\nTaille(s) possible(s) de la clé :", tailles)
