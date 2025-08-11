import qrcode
from io import BytesIO

import sqlalchemy.exc
from qrcode.image.styledpil import StyledPilImage

import uvicorn
from fastapi import FastAPI, Response, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import select

from models import ConsumableModel
from schemas import ConsumableAddSchema, ConsumablePatchSchema, ConsumableSchema
from database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/consumables", tags = ["Расходники"], summary="Создать расходник")
def create_consumable(consumable: ConsumableAddSchema, db: Session = Depends(get_db)):
    new_consumable = ConsumableModel(
        name = consumable.name,
        erp_code = consumable.erp_code,
        qty = consumable.qty,
        department = consumable.department
    )
    db.add(new_consumable)
    db.commit()
    db.refresh(new_consumable)
    return {"ok": True,
            "id": new_consumable.id,
            "message": f"Расходник '{new_consumable.name}' c id {new_consumable.id} успешно добавлен"}

@app.get("/consumables", tags = ["Расходники"], summary="Получить список расходников")
def get_cunsumables(db: Session = Depends(get_db)):
    query = select(ConsumableModel)
    data = db.execute(query)
    return {"data": data.scalars().all(),
            "ok": True,
            "message": "Cписок расходников успешно передан"}

@app.get("/consumables/{consumable_id}", tags = ["Расходники"], summary="Получить расходник")
def get_consumable(consumable_id: int, db: Session = Depends(get_db)):
    consumable = db.get(ConsumableModel, consumable_id)
    if consumable is None:
        raise HTTPException(status_code=404, detail="Расходник не найден")
    return {"data": consumable,
            "ok": True,
            "message": f"Расходник с id {consumable_id} успешно передан"}

@app.get("/consumables/{consumable_id}/qrcode", tags = ["QR-коды"], summary="Получить QR-код для расходника")
def get_qrcode(consumable_id: int, db: Session = Depends(get_db)):
        consumable = db.get(ConsumableModel, consumable_id)

        if consumable is None:
            raise HTTPException(status_code=404, detail="Расходник не найден")

        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(consumable_id)
        qr_img = qr.make_image(image_factory=StyledPilImage, embedded_image_path="AE.png")

        buffer = BytesIO()
        qr_img = qr_img.resize((500, 500))
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)

        return Response(content=buffer.read(), media_type="image/png")

@app.patch("/consumables/{consumable_id}", tags=["Расходники"], summary="Обновить расходник")
def update_consumable(consumable_id: int, patch_data: ConsumablePatchSchema, db: Session = Depends(get_db)):
    consumable = db.get(ConsumableModel, consumable_id)
    if consumable is None:
        raise HTTPException(status_code=404, detail="Расходник с таким id не найден")

    consumable_patch = patch_data.model_dump(exclude_unset=True)

    if not consumable_patch:
        raise HTTPException(status_code=400, detail="Данные для обновления не переданы")

    for key, value in consumable_patch.items():
        setattr(consumable, key, value)

    db.add(consumable)
    db.commit()
    db.refresh(consumable)

    return {"data": consumable,
            "ok": True,
            "message": f"Расходник с id {consumable.id} успешно обновлен"}

@app.delete("/consumables/{consumable_id}", tags=["Расходники"], summary="Удалить расходник")
def delete_consumable(consumable_id: int, db: Session = Depends(get_db)):
    consumable = db.get(ConsumableModel, consumable_id)

    if consumable is None:
        raise HTTPException(status_code=404, detail="Расходник не найден")

    db.delete(consumable)
    db.commit()

    return {"ok": True,
            "message": f"Расходник с id {consumable_id} успешно удален"}


if __name__ == "__main__":
    uvicorn.run("main:app")

