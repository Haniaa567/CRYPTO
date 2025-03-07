from pydantic import BaseModel, Field
from typing import List, Optional

class AffineRequest(BaseModel):
    text: str
    A: int
    B: int


class BruteForceRequest(BaseModel):
    cipher: str

# Modèle pour l'analyse de fréquence (texte chiffré + langue optionnelle)
class FrequencyAnalysisRequest(BaseModel):
    cipher: str
    language: Optional[str] = "english" 