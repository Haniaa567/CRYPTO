from fastapi import APIRouter, Depends
from controleur.hillControleur import handle_encrypt_hill, handle_decrypt_hill
from controleur.HillAttaque import handle_attack_hill,handle_attack_hill2

from models.hillModel import HillCipherRequest,HillAttackRequest,HillRequest
from auth.keycloak import verify_token

router = APIRouter()

@router.post("/encrypt", response_model=dict)
async def encrypt_message(request: HillCipherRequest):
    """
    Chiffre un message avec l'algorithme de Hill Cipher.

    Exemple de corps de requête :
    {
      "message": "HELLO",
      "key": [[6, 24], [1, 13]],
      "iduser": 123,
      "enregistrement": true
    }
    """
    return await handle_encrypt_hill(request)

@router.post("/decrypt", response_model=dict)
async def decrypt_message(request: HillCipherRequest):
    """
    Déchiffre un message avec l'algorithme de Hill Cipher.

    Exemple de corps de requête :
    {
      "message": "ZEBBW",
      "key": [[6, 24], [1, 13]],
      "iduser": 123,
      "enregistrement": true
    }
    """
    return await handle_decrypt_hill(request)

@router.post("/blindattaque", response_model=dict)
async def decrypt_message(request:HillAttackRequest ):

    return await handle_attack_hill(request)

@router.post("/attaqueknown",response_model=dict)
async def attack_hill(request: HillRequest):
    return await handle_attack_hill2(request)