'''''
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.servicesub import generateRandomKey, generatePasswordKey, encode, decode

router = APIRouter()

# Modèle Pydantic pour la requête
class MessageRequest(BaseModel):
    message: str
    key: str

class PasswordRequest(BaseModel):
    password: str

# Contrôleur pour générer une clé

def generate_key():
#def generate_key(mode: str, password: str = ""):
    #if mode == "A":
    key = generateRandomKey()
    #elif mode == "P":
        #key = generatePasswordKey(password)
    #else:
        #raise HTTPException(status_code=400, detail="Choix invalide")
    
    return {"key": key}
    
async def generate_key():
    key = generateRandomKey()
    return {"key": key}

# Contrôleur pour chiffrer un message

def encrypt_message(request: MessageRequest):
    message = request.message
    key = request.key
    
    secret = encode(message, key)
    return {"encrypted_message": secret}

# Contrôleur pour déchiffrer un message

def decrypt_message(request: MessageRequest):
    message = request.message
    key = request.key
    
    plaintext = decode(message, key)
    return {"decrypted_message": plaintext}
'''
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.servicesub import generateRandomKey, generatePasswordKey, encode, decode

router = APIRouter()

# Modèle Pydantic pour la requête
class MessageRequest(BaseModel):
    message: str
    key: str

# Contrôleur pour générer une clé
async def generate_key() -> dict:
    """Génère une clé aléatoire"""
    try:
        key = generateRandomKey()
        return {"key": key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la clé: {str(e)}")

# Contrôleur pour chiffrer un message
async def encrypt_message(request: MessageRequest) -> dict:
    """Chiffre un message avec une clé donnée"""
    try:
        message = request.message
        key = request.key
        
        secret = encode(message, key)
        return {"encrypted_message": secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du chiffrement du message: {str(e)}")

# Contrôleur pour déchiffrer un message
async def decrypt_message(request: MessageRequest) -> dict:
    """Déchiffre un message avec une clé donnée"""
    try:
        message = request.message
        key = request.key
        
        plaintext = decode(message, key)
        return {"decrypted_message": plaintext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du déchiffrement du message: {str(e)}")
