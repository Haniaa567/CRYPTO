import hashlib
from models.fncts import PasswordFeature
from fastapi import APIRouter, HTTPException

def hash_password(password: str, algorithm: str) -> str:
    """
    Hache un mot de passe en utilisant l'algorithme spécifié.
    """
    try:
        if algorithm == "sha1":
            return hashlib.sha1(password.encode()).hexdigest()
        elif algorithm == "md5":
            return hashlib.md5(password.encode()).hexdigest()
        elif algorithm == "sha256":
            return hashlib.sha256(password.encode()).hexdigest()
        else:
            raise ValueError("Algorithme non supporté")
    except Exception as e:
        raise ValueError(f"Erreur lors du hachage : {str(e)}")



"""""
async def find_matching_feature(password: str, algorithm: str) -> dict:

    # Recherche pour MtH (Mapping Texte → Hash)
    mth_match = await PasswordFeature.find_one(
        {"type": "MtoH", "sortie": password, "methode": algorithm}
    )
    if mth_match:
        return {
            "type": "MtoH",
            "matched_functionality": mth_match.nom,
            "original_input": mth_match.entree,
        }

    # Recherche pour HtM (Hash → Texte)
    htm_match = await PasswordFeature.find_one(
        {"type": "HtoM", "entree": password, "methode": algorithm}
    )
    if htm_match:
        return {
            "type": "HtoM",
            "matched_functionality": htm_match.nom,
            "hash_output": htm_match.sortie,
        }

    # Si aucune correspondance trouvée
    raise ValueError("No match found for the provided input and algorithm.")

"""
async def find_matching_feature(attaque: str, algorithme: str, id_utilisateur: str) -> dict:
    """
    Recherche une fonctionnalité correspondant à l'attaque, l'algorithme et l'utilisateur donné.
    """
    # Attendre la résolution de la requête
    fonctionnalite = await PasswordFeature.find_one(
        {
            "id_utilisateur": id_utilisateur,
            "$or": [
                {"type": "MtoH", "sortie": attaque, "methode": algorithme},
                {"type": "HtoM", "entree": attaque, "methode": algorithme}
            ]
        }
    )

    if fonctionnalite:
        # Accès direct aux attributs car Beanie retourne un objet
        if fonctionnalite.type == "MtoH":
            return {
                "type": "MtoH",
                "matched_functionality": fonctionnalite.nom,
                "original_input": fonctionnalite.entree
            }
        elif fonctionnalite.type == "HtoM":
            return {
                "type": "HtoM",
                "matched_functionality": fonctionnalite.nom,
                "output": fonctionnalite.sortie
            }

    return None
