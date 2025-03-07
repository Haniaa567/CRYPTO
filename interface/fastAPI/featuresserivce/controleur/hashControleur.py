from fastapi import HTTPException
from services.servicesHash import hash_password
from services.servicesHash import find_matching_feature
def handle_hash_request(password: str, algorithm: str) -> dict:
    """
    Fonction contrôleur pour gérer la requête de hachage de mot de passe.
    Cette fonction interagit avec le service pour effectuer l'opération.
    """
    try:
        hashed_password = hash_password(password, algorithm)
        
        return {"algorithm": algorithm, "hashed_password": hashed_password}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




async def handle_hash_request_find(attaque: str, algorithme: str, id_utilisateur: str) -> dict:
    """
    Fonction contrôleur pour gérer la requête de hachage avec vérification utilisateur.
    """
    try:
        result =  await find_matching_feature(attaque, algorithme, id_utilisateur)
        if not result:
            raise HTTPException(status_code=404, detail="Aucune fonctionnalité correspondante trouvée pour cet utilisateur.")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))