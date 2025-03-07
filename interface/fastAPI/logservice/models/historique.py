from beanie import Document
from pydantic import Field 
from datetime import datetime

class History(Document):
    id_utilisateur: str = Field(..., description="ID de l'utilisateur ayant effectué l'action")
    id_fonction: str = Field(..., description="ID de la fonctionnalité utilisée")
    message_entrer: str = Field(
        ..., description="Le message ou mot de passe saisi par l'utilisateur"
    )
    resultat_obtenu: str = Field(..., description="Résultat obtenu après l'exécution de la fonctionnalité")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Horodatage de l'action"
    )

    class Settings:
        name = "histories"

    class Config:
        json_schema_extra = {
            "example": {
                "id_utilisateur": "123456",
                "id_fonction": "654321",
                "message_entrer": "password123",
                "resultat_obtenu": "Mot de passe faible",
                "timestamp": "2024-11-28T12:34:56.789Z"
            }
        }

