from pydantic import BaseModel, Field
from typing import List

class HillCipherRequest(BaseModel):
    message: str = Field(..., example="HELLO")
    key: List[List[int]] = Field(..., example=[[6, 24], [1, 13]])
    enregistrement: bool = Field(False, example=True)


class HillAttackRequest(BaseModel):
    plaintext:str  # Liste des textes clairs connus
    ciphertext: str # Liste des textes chiffrés correspondants
    language: str 
    top_n:int
    block_size: int        # Taille des blocs (2x2 ou 3x3 en général)

class HillRequest(BaseModel):
    plaintext: str
    ciphertext: str
    block_size: int
