from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.consumable import ConsumableModel


def check_consumable_exists(consumable_id: int, db: Session = Depends(get_db)) -> ConsumableModel:
    consumable = db.get(ConsumableModel, consumable_id)
    if consumable is None:
        raise HTTPException(status_code=404, detail="Расходник не найден")
    return consumable