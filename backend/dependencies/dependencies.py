from typing import Literal

from fastapi import HTTPException, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session

from core.translation import MESSAGES
from database.database import get_db
from models.consumable import ConsumableModel


def get_lang(lang: Literal["ru", "en"] = Query(description="Response language", example="en", default="en")):
    return lang

def check_consumable_exists(consumable_id: int,
                            lang: str = Depends(get_lang),
                            db: Session = Depends(get_db)) -> ConsumableModel:

    consumable = db.get(ConsumableModel, consumable_id)

    if consumable is None:
        raise HTTPException(status_code=404, detail=MESSAGES[lang]["consumable.not_found"])
    return consumable

