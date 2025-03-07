from fastapi import HTTPException
from services.Affineservices import affine_brute_force,affine_encrypt,affine_decrypt,affine_frequency_analysis

def encrypt_controller(text: str, A: int, B: int):
    try:
        return {"encrypted_text": affine_encrypt(text, A, B)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def decrypt_controller(cipher: str, A: int, B: int):
    try:
        return {"decrypted_text": affine_decrypt(cipher, A, B)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def brute_force_controller(cipher: str):
    return {"possibilities": affine_brute_force(cipher)}

def frequency_analysis_controller(cipher: str, language: str = "english"):
    return {"possible_decryptions": affine_frequency_analysis(cipher, language)}