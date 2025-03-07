from beanie import Document
from pydantic import Field, root_validator,model_validator
from datetime import datetime
from beanie import  PydanticObjectId
from pydantic import Field
from typing import Optional

class PasswordFeature(Document):
    
    id: Optional[PydanticObjectId] = Field(
        default=None, alias="_id", exclude=True, description="Identifiant unique généré automatiquement par MongoDB"
    )
    id_utilisateur: str = Field(..., description="Identifiant de l'utilisateur associé")
    nom: str = Field(
        ..., 
        description="Nom de la fonctionnalité",
        pattern="^(Attaque par brut force|Attaque par dictionnaire|Attaque dictionnaire amélioré|Attaque hybrid|HachageMot|Generate_key|encrypt|decrypt|Hachage SHA256)$"
    )
    entree: str = Field(..., description="Entrée de l'opération (string)")
    sortie: str = Field(..., description="Sortie de l'opération (string)")
    key: Optional[str] = Field(
    default=None, 
    description="Clé publique en cas d'encryption"
    )
    type: str = Field(
        ..., 
        description="Type de l'opération",
        pattern="^(HtoM|MtoH|encrypt)$"   # HtoM les methodes ke type d'entree est un hachage et le type de sortie est un mot et MtoH sont les mots avec le type d'entrée est un mot et la sortie est une hachage
    )
    methode: str = None
    date_creation: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Date et heure de création de l'enregistrement"
    )
    date_modification: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Date et heure de dernière modification de l'enregistrement"
    )

    @model_validator(mode="after")
    def validate_methode_field(cls, values):
      type_op = values.type
      methode = values.methode
      key = values.key

      if type_op in ['HtoM', 'encrypt'] and not methode:
        raise ValueError(
            "Le champ 'methode' est obligatoire pour les types 'HtoM' et 'encrypt'."
        )
      if type_op == 'encrypt' and not key:
        raise ValueError(
            "Le champ 'key' est obligatoire pour le type 'encrypt'."
        )   
      return values



    class Config:
        json_encoders = {
            PydanticObjectId: str,  # Convertit PydanticObjectId en chaîne pour JSON
        }


""""" 
from beanie import Document, PydanticObjectId
from pydantic import Field
from typing import Optional

class PasswordFeature(Document):
    id: Optional[PydanticObjectId] = Field(
        default=None, alias="_id", exclude=True, description="Identifiant unique généré automatiquement par MongoDB"
    )
    id_utilisateur: str = Field(..., description="Identifiant de l'utilisateur associé")
    nom: str = Field(
        ..., 
        description="Nom de la fonctionnalité",
        pattern="^(Attaque par brut force|Attaque par dictionnaire|Attaque dictionnaire amélioré|Attaque hybrid|HachageMot|Generate_key|encrypt|decrypt)$"
    )
    entree: str = Field(..., description="Entrée de l'opération (string)")
    sortie: str = Field(..., description="Sortie de l'opération (string)")
    key: Optional[str] = Field(None, description="Clé publique en cas d'encryption")
    type: str = Field(
        ..., 
        description="Type de l'opération",
        pattern="^(HtoM|MtoH|encrypt)$"
    )
    methode: Optional[str] = Field(None, description="Méthode utilisée pour l'opération")

    class Config:
        json_encoders = {
            PydanticObjectId: str,  # Convertit PydanticObjectId en chaîne pour JSON
        }
"""

