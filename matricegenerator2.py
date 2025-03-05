import numpy as np
from sympy import Matrix, mod_inverse
import json
import os

def is_invertible_mod26(matrix):
    """Vérification rigoureuse de l'inversibilité modulo 26"""
    m = Matrix(matrix)
    det = m.det()
    try:
        mod_inverse(int(det) % 26, 26)
        return True
    except ValueError:
        return False

def generate_valid_2x2_hill_matrices(num_matrices=1000, output_file='hill_matrices_2x2.json'):
    """
    Génère des matrices de Hill valides de taille 2x2
    
    Args:
    - num_matrices (int): Nombre de matrices à générer (défaut: 1000)
    - output_file (str): Fichier de sortie pour stocker les matrices
    
    Returns:
    - list: Liste des matrices valides
    """
    valid_matrices = []
    
    # Nombre total de combinaisons possibles
    total_combinations = 26 ** 4
    
    # Limite pour éviter une boucle infinie
    max_attempts = min(total_combinations, 1_000_000)
    
    attempts = 0
    while len(valid_matrices) < num_matrices and attempts < max_attempts:
        # Générer une matrice 2x2 aléatoire
        key_values = np.random.randint(0, 26, size=(2, 2))
        
        # Vérifier l'inversibilité de la matrice
        if is_invertible_mod26(key_values):
            # Convertir numpy array en liste pour sérialisation JSON
            valid_matrices.append(key_values.tolist())
        
        attempts += 1
    
    # Sauvegarder les matrices dans un fichier JSON
    with open(output_file, 'w') as f:
        json.dump(valid_matrices, f)
    
    print(f"Généré {len(valid_matrices)} matrices 2x2 valides et sauvegardé dans {output_file}")
    return valid_matrices

def load_2x2_hill_matrices(input_file='hill_matrices_2x2.json'):
    """
    Charge les matrices de Hill 2x2 à partir d'un fichier JSON
    
    Args:
    - input_file (str): Fichier contenant les matrices
    
    Returns:
    - list: Liste des matrices chargées
    """
    try:
        with open(input_file, 'r') as f:
            matrices = json.load(f)
        return [np.array(matrix) for matrix in matrices]
    except FileNotFoundError:
        print(f"Fichier {input_file} non trouvé. Générez d'abord les matrices.")
        return []

def main():
    # Générer des matrices 2x2
    generate_valid_2x2_hill_matrices(num_matrices=50000)
    
    # Charger et afficher quelques matrices
    matrices = load_2x2_hill_matrices()
    print(f"\nMatrices 2x2 chargées :")
    print(f"Nombre de matrices : {len(matrices)}")
    
    # Afficher les 3 premières matrices si disponibles
    for i, matrix in enumerate(matrices[:3], 1):
        print(f"\nMatrice {i} :")
        print(matrix)

def verify_matrices():
    """Vérification supplémentaire des matrices générées"""
    matrices = load_2x2_hill_matrices()
    
    print("\nVérification des matrices 2x2")
    invalid_count = 0
    
    for matrix in matrices:
        if not is_invertible_mod26(matrix):
            invalid_count += 1
            print(f"Matrice invalide trouvée :\n{matrix}")
    
    print(f"Nombre de matrices invalides : {invalid_count}")
    print(f"Nombre total de matrices : {len(matrices)}")

if __name__ == "__main__":
    main()
    # Décommentez pour vérification détaillée
    # verify_matrices()