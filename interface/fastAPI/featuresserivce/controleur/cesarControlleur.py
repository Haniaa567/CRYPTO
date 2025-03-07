from fastapi import HTTPException
from models.cesarModel import (
    CaesarEncryptRequest, 
    CaesarDecryptRequest, 
    BruteForceRequest,
    FrequencyAnalysisRequest,
    FrequencyAnalysisResponse
)
from services.cesarservice import (
    caesar_encryption, 
    caesar_decryption, 
    get_brute_force_results,
    get_frequency_analysis_results
)

async def encrypt_text(request: CaesarEncryptRequest) -> dict:
    """
    Controller to encrypt text using Caesar cipher
    """
    try:
        encrypted_text = caesar_encryption(request.text, request.shift)
        return {"encrypted_text": encrypted_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during encryption: {str(e)}")

async def decrypt_text(request: CaesarDecryptRequest) -> dict:
    """
    Controller to decrypt text using Caesar cipher
    """
    try:
        decrypted_text = caesar_decryption(request.text, request.shift)
        return {"decrypted_text": decrypted_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during decryption: {str(e)}")

async def brute_force_crack(request: BruteForceRequest) -> dict:
    """
    Controller to crack text using brute force approach
    """
    try:
        results = get_brute_force_results(request.text)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during brute force attack: {str(e)}")

async def analyze_frequency(request: FrequencyAnalysisRequest) -> FrequencyAnalysisResponse:
    """
    Controller to analyze text using frequency analysis
    """
    try:
        results = get_frequency_analysis_results(request.text, request.language)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during frequency analysis: {str(e)}")