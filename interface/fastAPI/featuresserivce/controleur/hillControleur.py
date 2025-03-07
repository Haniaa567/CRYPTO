from fastapi import HTTPException, Depends
from services.hillService import encrypt_message_hill, decrypt_message_hill,is_invertible_mod26
from models.hillModel import HillCipherRequest
from services.servicesFcts import create_feature
from models.fncts import PasswordFeature
from auth.keycloak import verify_token

MODULO = 26  # Pour l'alphabet anglais

async def handle_encrypt_hill(request: HillCipherRequest) -> dict:
    """Traite la requête de chiffrement Hill Cipher."""
    try:
        # Vérification si la matrice est valide et inversible
        if not is_invertible_mod26(request.key):
            raise HTTPException(status_code=400, detail="La matrice de la clé n'est pas inversible modulo 26.")

        encrypted_message = encrypt_message_hill(request.message, request.key)
       
        # Enregistrement si demandé
        #if request.enregistrement:
            #feature = PasswordFeature(
                #id_utilisateur=request.iduser,
                #nom="encrypt",
                #entree=request.message,
                #sortie=encrypted_message,
                #key=str(request.key),
                #type="encrypt",
                #methode="Hill Cipher"
            #)
            #await create_feature(feature)

        return {
            "encrypted_message": encrypted_message
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du chiffrement : {str(e)}")

async def handle_decrypt_hill(request: HillCipherRequest) -> dict:
    """Traite la requête de déchiffrement Hill Cipher."""
    try:
        # Vérification si la matrice est valide et inversible
        if not is_invertible_mod26(request.key):
            raise HTTPException(status_code=400, detail="La matrice de la clé n'est pas inversible modulo 26.")

        decrypted_message = decrypt_message_hill(request.message, request.key)

        # Enregistrement si demandé
        #if request.enregistrement:
            #feature = PasswordFeature(
                #id_utilisateur=request.iduser,
                #nom="decrypt",
                #entree=request.message,
                #sortie=decrypted_message,
                #key=str(request.key),
                #type="decrypt",
                #methode="Hill Cipher"
            #)
            #await create_feature(feature)

        return {
            "decrypted_message": decrypted_message
            
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du déchiffrement : {str(e)}")
