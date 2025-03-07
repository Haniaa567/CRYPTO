from fastapi import APIRouter, Query,Depends
from controleur.hashControleur import handle_hash_request,handle_hash_request_find
from models.dic import AttackRequest,DictionaryWord,PasswordCheckRequest
from models.DicModel import Dictionary
from services.servicesAttaques import perform_dictionary_attack_logic,dic_amelioer,hybrid_attack_logic,brute_force_attack
from fastapi import HTTPException
from beanie import  PydanticObjectId
from controleur.dicControleur import handle_dicAttaque,handle_dicAmeliorer,handle_bruteForce,handle_hybrid,handle_test_password
from middlewares.auth_middlewares import JWTBearer
from fastapi import HTTPException, Request,Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import config
import requests
from jose import jwt
from jose.exceptions import JWTError
from auth.keycloak import verify_token
'''
# Fonction de vérification du token
security = HTTPBearer()

def get_keycloak_public_key():
    url = f"{config.KEYCLOAK_SERVER_URL}/realms/{config.KEYCLOAK_REALM}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        public_key = response.json()['public_key']
        return f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    except Exception as e:
        print(f"Error fetching public key: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch public key")

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        public_key = get_keycloak_public_key()
        
        # Décoder et vérifier le token
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="account",
            issuer=f"{config.KEYCLOAK_SERVER_URL}/realms/{config.KEYCLOAK_REALM}"
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error validating token: {str(e)}"
        )
'''
router = APIRouter()

@router.get("/hash")
async def get_hashed_password(password: str, algorithm: str):
    """
    Appelle la fonction contrôleur pour traiter la requête de hachage.
    """
    return handle_hash_request(password, algorithm)




@router.get("/hash/verif")
async def get_hashed_password_find(
    attaque: str = Query(..., description="Valeur à vérifier (attaque)"),
    algorithme: str = Query(..., description="Algorithme utilisé"),
    id_utilisateur: str = Query(..., description="ID de l'utilisateur")
):
    """
    Route pour gérer les requêtes de hachage avec vérification utilisateur.
    """
    return await handle_hash_request_find(attaque, algorithme,id_utilisateur)



@router.post("/Dictionnaire")
async def dictionary_attack(request: AttackRequest,token: dict = Depends(verify_token))-> dict:
#async def dictionary_attack(request: AttackRequest)-> dict:
    return await handle_dicAttaque(request,token)
    #return await handle_dicAttaque(request)
@router.post("/bruteForce")
async def bruteForce_attack(request: AttackRequest,token: dict = Depends(verify_token))-> dict:
#async def bruteForce_attack(request: AttackRequest)-> dict:
    return await handle_bruteForce(request,token)
    #return await handle_bruteForce(request)
@router.get("/word/{word_id}")
async def get_word(word_id: str):
    try:
        # Rechercher un mot dans la collection par son ID
        word = await Dictionary.get(PydanticObjectId(word_id))
        
        if word:
            return {"word": word.password}  # Retourner le mot
        else:
            raise HTTPException(status_code=404, detail="Word not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/DictionnaireAmeliorer")
async def dicAmeliorer_attack(request: AttackRequest,token: dict = Depends(verify_token))-> dict:
#async def dicAmeliorer_attack(request: AttackRequest)-> dict:   
    return await handle_dicAmeliorer(request,token)
    #return await handle_dicAmeliorer(request)

@router.post("/hybrid")
async def hybrid_attack(request: AttackRequest,token: dict = Depends(verify_token))-> dict:
#async def hybrid_attack(request: AttackRequest)-> dict:
    return await handle_hybrid(request,token)
    #return await handle_hybrid(request)

@router.post("/check-password")
async def check_password_endpoint(request: PasswordCheckRequest):
    return await handle_test_password(request)