# models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple


class VigenereRequest(BaseModel):
    text: str = Field(..., description="Text to encrypt/decrypt")
    key: str = Field(..., description="Vigenere cipher key")


class VigenereResponse(BaseModel):
    result: str = Field(..., description="Result of the encryption/decryption")


class CryptanalysisKeyLengthRequest(BaseModel):
    ciphertext: str = Field(..., description="The encrypted text to analyze")
    key_length: int = Field(..., description="Suspected key length")
    top_results: int = Field(10, description="Number of top results to return")


class KeyResult(BaseModel):
    key: str
    score: float
    plaintext: str


class CryptanalysisKeyLengthResponse(BaseModel):
    results: List[KeyResult]
    best_key: str
    best_score: float
    best_plaintext: str


class CryptanalysisWordRequest(BaseModel):
    ciphertext: str = Field(..., description="The encrypted text to analyze")
    key_length: int = Field(..., description="Suspected key length")
    suspected_word: str = Field(..., description="Word suspected to be in the plaintext")


class WordResult(BaseModel):
    key: str
    plaintext: str


class CryptanalysisWordResponse(BaseModel):
    results: List[WordResult]