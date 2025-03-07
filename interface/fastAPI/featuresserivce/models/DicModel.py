from beanie import Document

class Dictionary(Document):
    """
    Modèle représentant un mot du dictionnaire.
    """
    password: str

    class Settings:
        name = "dictionaries"  # Nom de la collection dans la base de données
