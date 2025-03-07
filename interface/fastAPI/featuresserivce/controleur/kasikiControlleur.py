from fastapi import HTTPException
from services.kaseskiService import kasiski_test

def kasiski_controller(ciphertext: str):
    try:
        result = kasiski_test(ciphertext)
        return {
            "repeated_sequences": result["repeated_sequences"],
            "distances": result["distances"],
            "common_factors": result["common_factors"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse de Kasiski : {str(e)}")
