from fastapi import APIRouter,Depends
from controleur.encryControleur import generate_key_aes, handle_encrypt_aes, handle_decrypt_aes,generate_key_3des,handle_decrypt_3des,handle_encrypt_3des,handle_generate_keys_rsa, handle_encrypt_message_rsa, handle_decrypt_message_rsa
from controleur.encryControleur import generate_key_RC4,handle_decrypt_RC4,handle_encrypt_RC4,generate_key_Chacha20,handle_decrypt_Chacha20,handle_encrypt_Chacha20
from models.encry import EncryptRequest, DecryptRequest
from auth.keycloak import verify_token

router = APIRouter()


#********************************AES*************************************************


@router.get("/generate-key/AES", response_model=str)
async def generate_key():
    """Route pour générer une clé AES."""
    return generate_key_aes()

@router.post("/encrypt/AES", response_model=dict)
async def encrypt(request: EncryptRequest, token: dict = Depends(verify_token)) -> dict:
    """Route pour chiffrer un message AES."""
    return await handle_encrypt_aes(request,token)

@router.post("/decrypt/AES", response_model=dict)
async def decrypt(request: DecryptRequest,token: EncryptRequest = Depends(verify_token))-> EncryptRequest:
    """Route pour déchiffrer un message AES."""
    return await handle_decrypt_aes(request,token)


#********************************3DES*************************************************


@router.get("/generate-key/3DES", response_model=str)
async def generate_key():
    """Route pour générer une clé 3DES."""
    return generate_key_3des()

@router.post("/encrypt/3DES", response_model=dict)
async def encrypt(request: EncryptRequest,token: dict = Depends(verify_token)) -> dict:
    """Route pour chiffrer un message 3DES."""
    return await handle_encrypt_3des(request,token)

@router.post("/decrypt/3DES", response_model=dict)
async def decrypt(request: DecryptRequest,token: dict = Depends(verify_token)) -> dict:
    """Route pour déchiffrer un message 3DES."""
    return await handle_decrypt_3des(request,token)

#***********************************RC4****************************************************

@router.get("/generate-key/RC4", response_model=str)
async def generate_key():
    """Route pour générer une clé RC4."""
    return generate_key_RC4()

@router.post("/encrypt/RC4", response_model=dict)
async def encrypt(request: EncryptRequest,token: dict = Depends(verify_token)) -> dict:
    """Route pour chiffrer un message RC4."""
    return await handle_encrypt_RC4(request,token)

@router.post("/decrypt/RC4", response_model=dict)
async def decrypt(request: DecryptRequest,token: dict = Depends(verify_token)) -> dict:
    """Route pour déchiffrer un message RC4."""
    return await handle_decrypt_RC4(request,token)


#***********************************CHACHA20****************************************************

@router.get("/generate-key/Chacha20", response_model=str)
async def generate_key():
    """Route pour générer une clé chacha20."""
    return  generate_key_Chacha20()

@router.post("/encrypt/Chacha20", response_model=dict)
async def encrypt(request: EncryptRequest,token: dict = Depends(verify_token)) -> dict:
    """Route pour chiffrer un message chacha20"""
    return await handle_encrypt_Chacha20(request,token)

@router.post("/decrypt/Chacha20", response_model=dict)
async def decrypt(request: DecryptRequest,token: dict = Depends(verify_token)) -> dict:
    """Route pour déchiffrer un message Chacha20."""
    return await  handle_decrypt_Chacha20(request,token)


#***********************************RSA****************************************************

@router.get("/generate-keys/RSA")
def generate_keys():
    """Endpoint pour générer des clés RSA."""
    return handle_generate_keys_rsa()

@router.post("/encrypt/RSA")
def encrypt_message(request:EncryptRequest,token: dict = Depends(verify_token))-> dict:
    """Endpoint pour chiffrer un message."""
    return handle_encrypt_message_rsa(request,token)

@router.post("/decrypt/RSA")
def decrypt_message(request:DecryptRequest,token: dict = Depends(verify_token))-> dict:
    """Endpoint pour déchiffrer un message."""
    return handle_decrypt_message_rsa(request,token)

