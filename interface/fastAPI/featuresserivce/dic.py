from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Connexion à MongoDB
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient("mongodb+srv://aknouchechaima00:iq0wZXoopwoS8rFQ@pinkcells.ppfpp.mongodb.net/",ssl=True,tlsAllowInvalidCertificates=True)
db = client["password_testing"]
collection = db["dictionaries"]

def import_large_dictionary(file_path, batch_size=1000):
    """
    Importe un dictionnaire volumineux dans MongoDB par petits lots.

    Args:
    - file_path (str): Chemin vers le fichier dictionnaire.
    - batch_size (int): Taille des lots pour l'insertion.
    """
    try:
        batch = []
        total_count = 0
        with open(file_path, "r") as file:
            for line in file:
                batch.append({"password": line.strip()})
                if len(batch) >= batch_size:
                    collection.insert_many(batch)
                    total_count += len(batch)
                    batch = []
                    print(f"{total_count} mots importés...")
            if batch:  # Insertion des mots restants
                collection.insert_many(batch)
                total_count += len(batch)
        print(f"Dictionnaire importé avec succès : {total_count} mots.")
    except Exception as e:
        print(f"Erreur lors de l'importation : {e}")

# Chemin du fichier dictionnaire
file_path = "liste.txt"

if os.path.exists(file_path):
    import_large_dictionary(file_path)
else:
    print(f"Le fichier '{file_path}' est introuvable.")
