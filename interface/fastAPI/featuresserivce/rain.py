from pymongo import MongoClient
import os
import re

# Connexion à MongoDB
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("L'environnement variable 'MONGO_URI' n'est pas définie.")

client = MongoClient(mongo_uri)
db = client["password_testing"]#??
collection = db["dictionaries"]

def import_hashed_dictionary(file_path, batch_size=1000):
    """
    Importe un dictionnaire avec des hachages dans MongoDB par petits lots.

    Args:
    - file_path (str): Chemin vers le fichier dictionnaire.
    - batch_size (int): Taille des lots pour l'insertion.
    """
    try:
        batch = []
        total_count = 0
        # Expression régulière pour extraire les trois champs
        regex = r"([a-f0-9]{40}):\s([^\s]+)\s->\s([a-f0-9]{40})"
        
        with open(file_path, "r") as file:
            for line in file:
                match = re.match(regex, line.strip())
                if match:
                    hash_1 = match.group(1)
                    password = match.group(2)
                    hash_2 = match.group(3)
                    batch.append({"hash_1": hash_1, "password": password, "hash_2": hash_2})

                    if len(batch) >= batch_size:
                        collection.insert_many(batch)
                        total_count += len(batch)
                        batch = []
                        print(f"{total_count} entrées importées...")

            if batch:  # Insertion des derniers lots
                collection.insert_many(batch)
                total_count += len(batch)

        print(f"Dictionnaire importé avec succès : {total_count} entrées.")
    
    except Exception as e:
        print(f"Erreur lors de l'importation : {e}")

# Chemin du fichier dictionnaire
file_path = "dictionnaire.txt"

if os.path.exists(file_path):
    import_hashed_dictionary(file_path)
else:
    print(f"Le fichier '{file_path}' est introuvable.")
