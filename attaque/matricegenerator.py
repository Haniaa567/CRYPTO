import numpy as np
from sympy import Matrix, mod_inverse
import itertools
import json

def is_invertible_mod26(matrix):
    """Vérification rigoureuse de l'inversibilité modulo 26"""
    m = Matrix(matrix)
    det = m.det()
    try:
        mod_inverse(int(det) % 26, 26)
        return True
    except ValueError:
        return False

def generate_valid_hill_matrices(block_size=3, num_matrices=1000, output_file='hill_matrices.json'):
    """
    Génère des matrices de Hill valides de taille block_size x block_size
    
    Args:
    - block_size (int): Taille des matrices carrées (défaut: 3)
    - num_matrices (int): Nombre de matrices à générer (défaut: 1000)
    - output_file (str): Fichier de sortie pour stocker les matrices
    
    Returns:
    - list: Liste des matrices valides
    """
    valid_matrices = []
    
    # Nombre total de combinaisons possibles
    total_combinations = 26 ** (block_size * block_size)
    
    # Limite pour éviter une boucle infinie
    max_attempts = min(total_combinations, 1_000_000)
    
    attempts = 0
    while len(valid_matrices) < num_matrices and attempts < max_attempts:
        # Générer une matrice aléatoire
        key_values = np.random.randint(0, 26, size=(block_size, block_size))
        
        # Vérifier l'inversibilité de la matrice
        if is_invertible_mod26(key_values):
            # Convertir numpy array en liste pour sérialisation JSON
            valid_matrices.append(key_values.tolist())
        
        attempts += 1
    
    # Sauvegarder les matrices dans un fichier JSON
    with open(output_file, 'w') as f:
        json.dump(valid_matrices, f)
    
    print(f"Généré {len(valid_matrices)} matrices valides et sauvegardé dans {output_file}")
    return valid_matrices

def load_hill_matrices(input_file='hill_matrices.json'):
    """
    Charge les matrices de Hill à partir d'un fichier JSON
    
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
    # Générer des matrices de Hill valides de taille 3x3
    generate_valid_hill_matrices(block_size=3, num_matrices=10000)
    
    # Charger et utiliser les matrices
    matrices = load_hill_matrices()
    print(f"Nombre de matrices chargées : {len(matrices)}")
    
    # Exemple d'utilisation d'une matrice
    if matrices:
        print("Première matrice chargée :")
        print(matrices[0])

if __name__ == "__main__":
    main()