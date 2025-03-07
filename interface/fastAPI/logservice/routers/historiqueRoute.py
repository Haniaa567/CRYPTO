from fastapi import APIRouter, HTTPException
from ..models.historique  import History

router = APIRouter()

@router.post("/", response_model=History)
async def add_history_entry(
    id_utilisateur: str,
    id_fonction: str,
    message_entrer: str,
    resultat_obtenu: str
):
    try:
        history_entry = History(
            id_utilisateur=id_utilisateur,
            id_fonction=id_fonction,
            message_entrer=message_entrer,
            resultat_obtenu=resultat_obtenu
        )
        await history_entry.insert()
        return history_entry
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))