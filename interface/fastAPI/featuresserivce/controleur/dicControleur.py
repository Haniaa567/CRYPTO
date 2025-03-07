from fastapi import HTTPException, Request,Security
from fastapi import HTTPException,Depends
from models.dic import AttackRequest,PasswordCheckRequest
from services.servicesAttaques import perform_dictionary_attack_logic,dic_amelioer,hybrid_attack_logic,brute_force_attack
from services.servicesAttaques import test_password
import logging
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from middlewares.auth_middlewares import JWTBearer
from config import config
import requests
from jose import jwt
from jose.exceptions import JWTError
from auth.keycloak import verify_token
from services.servicesFcts import create_feature
from models.fncts import PasswordFeature
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
async def handle_dicAttaque(request: AttackRequest, token: dict = Depends(verify_token)) -> dict:
#async def handle_dicAttaque(request: AttackRequest) -> dict:
    try:
        # Appel de la fonction qui effectue l'attaque par dictionnaire
        result = await perform_dictionary_attack_logic(request.hashed_password, request.salt, request.hash_algorithm)
        if request.enregistrement:
            password_found = result.get("password_found", "unknown")
            # Préparer le champ `key` si `salt` est fourni
            key = request.salt if request.salt else None
            feature = PasswordFeature(
              id_utilisateur=request.iduser,
              nom="Attaque par dictionnaire",
              entree=request.hashed_password,
              sortie=password_found,
              key=key,
              type="HtoM",
              methode=request.hash_algorithm
            )
            await create_feature( feature)
        
        # Vérifiez si le résultat indique une erreur (par exemple, "success": False)
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        
         # Retourne le résultat combiné avec les informations d'authentification
        return {
            **result,  
            "message": "You have access to this protected service",
            "user": token.get("preferred_username")
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error in hash computation: {str(e)}")
    except Exception as e:
        # Capture toute autre exception et renvoyer une erreur 500 pour l'erreur interne
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
async def handle_bruteForce(request: AttackRequest, token: dict = Depends(verify_token)) -> dict:
#async def handle_bruteForce(request: AttackRequest) -> dict:
    try:
  # Appel de la fonction qui effectue l'attaque par dictionnaire
        result = await brute_force_attack(
            request.hashed_password, 
            request.salt, 
            request.hash_algorithm
        )
        if request.enregistrement:
            password_found = result.get("password_found", "unknown")
            # Préparer le champ `key` si `salt` est fourni
            key = request.salt if request.salt else None
            feature = PasswordFeature(
              id_utilisateur=request.iduser,
              nom="Attaque par brut force",
              entree=request.hashed_password,
              sortie=password_found,
              key=key,
              type="HtoM",
              methode=request.hash_algorithm
            )
            await create_feature( feature)
        

        
        # Vérifiez si le résultat indique une erreur
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        
        # Retourne le résultat combiné avec les informations d'authentification
        return {
            **result,  
            "message": "You have access to this protected service",
            "user": token.get("preferred_username")
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error in hash computation: {str(e)}"
        )
    
    except Exception as e:
        # Log l'erreur pour le debugging
        logging.error(f"Internal server error in bruteforce: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

async def handle_dicAmeliorer(request: AttackRequest, token: dict = Depends(verify_token)) -> dict:
#async def handle_dicAmeliorer(request: AttackRequest) -> dict:
    try:
        # Appel de la fonction qui effectue l'attaque par dictionnaire
        result = await dic_amelioer(request.hashed_password, request.salt, request.hash_algorithm)
        if request.enregistrement:
            password_found = result.get("password_found", "unknown")
            # Préparer le champ `key` si `salt` est fourni
            key = request.salt if request.salt else None
            feature = PasswordFeature(
              id_utilisateur=request.iduser,
              nom="Attaque dictionnaire amélioré",
              entree=request.hashed_password,
              sortie=password_found,
              key=key,
              type="HtoM",
              methode=request.hash_algorithm
            )
            await create_feature( feature)
        
        # Vérifiez si le résultat indique une erreur (par exemple, "success": False)
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        
        # Retourne le résultat combiné avec les informations d'authentification
        return {
            **result,  
            "message": "You have access to this protected service",
            "user": token.get("preferred_username")
        }
         # Retourne le résultat de l'attaque par dictionnaire
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error in hash computation: {str(e)}")
    except Exception as e:
        # Capture toute autre exception et renvoyer une erreur 500 pour l'erreur interne
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    
async def handle_hybrid(request: AttackRequest, token: dict = Depends(verify_token)) -> dict:
#async def handle_hybrid(request: AttackRequest) -> dict:   
    try:
        # Appel de la fonction qui effectue l'attaque par dictionnaire
        result = await hybrid_attack_logic(request.hashed_password, request.salt, request.hash_algorithm)
        if request.enregistrement:
            password_found = result.get("password_found", "unknown")
            # Préparer le champ `key` si `salt` est fourni
            key = request.salt if request.salt else None
            feature = PasswordFeature(
              id_utilisateur=request.iduser,
              nom="Attaque hybrid",
              entree=request.hashed_password,
              key=key,
              sortie=password_found,
              type="HtoM",
              methode=request.hash_algorithm
            )
            await create_feature( feature)
        
        # Vérifiez si le résultat indique une erreur (par exemple, "success": False)
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        
        # Retourne le résultat combiné avec les informations d'authentification
        return {
            **result,  
            "message": "You have access to this protected service",
            "user": token.get("preferred_username")
        }
         # Retourne le résultat de l'attaque par dictionnaire
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error in hash computation: {str(e)}")
    except Exception as e:
        # Capture toute autre exception et renvoyer une erreur 500 pour l'erreur interne
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

async def handle_test_password(request: PasswordCheckRequest):
    try:
        # Appel de la fonction qui effectue les vérifications sur le mot de passe
        result = await test_password(request.password)
        
        # Si le mot de passe est jugé non sécurisé, lever une exception HTTP avec un message clair
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        # Retourne le résultat si le mot de passe est sécurisé
        # Retourne le résultat combiné avec les informations d'authentification
        return {
            **result,  
            #"message": "You have access to this protected service",
            #"user": token.get("preferred_username")
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error during password validation: {str(e)}")
    except Exception as e:
        # Capture toute autre exception et renvoyer une erreur 500 pour une erreur interne
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")