# controllers.py
from fastapi import APIRouter, Depends
from typing import List

from models.VigenereModel import (
    VigenereRequest, VigenereResponse,
    CryptanalysisKeyLengthRequest, CryptanalysisKeyLengthResponse, KeyResult,
    CryptanalysisWordRequest, CryptanalysisWordResponse, WordResult
)
from services.VigenereService import VigenereService, CryptanalysisService


class VigenereController:
    def __init__(self, vigenere_service: VigenereService = Depends()):
        self.vigenere_service = vigenere_service

    async def encrypt(self, request: VigenereRequest) -> VigenereResponse:
        result = self.vigenere_service.encrypt(request.text, request.key)
        return VigenereResponse(result=result)

    async def decrypt(self, request: VigenereRequest) -> VigenereResponse:
        result = self.vigenere_service.decrypt(request.text, request.key)
        return VigenereResponse(result=result)


class CryptanalysisController:
    def __init__(self, cryptanalysis_service: CryptanalysisService = Depends()):
        self.cryptanalysis_service = cryptanalysis_service

    async def analyze_by_key_length(self, request: CryptanalysisKeyLengthRequest) -> CryptanalysisKeyLengthResponse:
        result = self.cryptanalysis_service.analyze_by_key_length(
            request.ciphertext,
            request.key_length,
            top_results=request.top_results
        )
        
        key_results = [
            KeyResult(key=r["key"], score=r["score"], plaintext=r["plaintext"])
            for r in result["results"]
        ]
        
        return CryptanalysisKeyLengthResponse(
            results=key_results,
            best_key=result["best_key"],
            best_score=result["best_score"],
            best_plaintext=result["best_plaintext"]
        )

    async def analyze_by_suspected_word(self, request: CryptanalysisWordRequest) -> CryptanalysisWordResponse:
        results = self.cryptanalysis_service.analyze_by_suspected_word(
            request.ciphertext,
            request.suspected_word,
            request.key_length
        )
        
        word_results = [WordResult(key=r["key"], plaintext=r["plaintext"]) for r in results]
        
        return CryptanalysisWordResponse(results=word_results)