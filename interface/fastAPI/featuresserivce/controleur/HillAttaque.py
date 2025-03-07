from fastapi import HTTPException
from services.hillAttaque import blind_attack_Hill, is_valid_ciphertext
from models.hillModel import HillAttackRequest,HillRequest
from services.hillAttaque2 import attack_Hill, decrypt_Hill
import numpy as np

async def handle_attack_hill(request: HillAttackRequest) -> dict:
    """Traite la requête d'attaque par force brute du Hill Cipher."""
    try:
        # Validation du ciphertext
        if not is_valid_ciphertext(request.ciphertext, request.block_size):
            raise HTTPException(status_code=400, detail="Le texte chiffré contient des caractères invalides.")

        # Validation de la taille des blocs (2 ou 3 uniquement)
        if request.block_size not in [2, 3]:
            raise HTTPException(status_code=400, detail="La taille du bloc doit être 2 ou 3.")

        # Exécution de l'attaque
        results = blind_attack_Hill(request.ciphertext, request.block_size, request.top_n, request.language)

        if not results:
            raise HTTPException(status_code=404, detail="Aucun résultat trouvé pour cette attaque.")

        # "Entrer" dans chaque objet de la liste et sérialiser correctement
        results_serialized = []
        for result in results:
            # Assurez-vous de traiter chaque champ de l'objet dans la liste
            key_serialized = result['key'].tolist() if isinstance(result['key'], np.ndarray) else result['key']
            decrypted_text = result['decrypted_text']  # C'est déjà une chaîne, donc rien à changer
            score = result['score']  # C'est un entier ou un flottant, donc rien à changer

            # Ajoutez l'objet sérialisé à la liste
            results_serialized.append({
                "key": key_serialized,
                "decrypted_text": decrypted_text,
                "score": score
            })

        return {"results": results_serialized}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'attaque : {str(e)}")




async def handle_attack_hill2(request: HillRequest):
    """Traite la requête d'attaque Hill"""
    try:
        # Appel du service pour attaquer Hill et retrouver la clé
        key = attack_Hill(request.plaintext, request.ciphertext, request.block_size)
        
        # Appel du service pour déchiffrer le texte avec la clé trouvée
        decrypted_text = decrypt_Hill(request.ciphertext, key, request.block_size)
        
        return {"key": key.tolist(), "decrypted_text": decrypted_text}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
