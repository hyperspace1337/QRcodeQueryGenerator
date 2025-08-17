from io import BytesIO

import qrcode

from fastapi import APIRouter, HTTPException, Depends, Response
from qrcode.image.styledpil import StyledPilImage
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.translation import MESSAGES
from database.database import get_db
from models.consumable import ConsumableModel
from schemas.consumable import ConsumableAddSchema, ConsumablePatchSchema
from dependencies.dependencies import check_consumable_exists, get_lang
from config import assets_dir

router = APIRouter(
    prefix="/consumables",
    tags=["Consumables"],
)


@router.post("/", summary="Create a consumable")
def create_consumable(consumable: ConsumableAddSchema,
                      db: Session = Depends(get_db),
                      lang: str = Depends(get_lang)):
    new_consumable = ConsumableModel(
        name=consumable.name,
        erp_code=consumable.erp_code,
        qty=consumable.qty,
        department=consumable.department
    )

    db.add(new_consumable)
    db.commit()
    db.refresh(new_consumable)

    return {"data": new_consumable,
            "ok": True,
            "message": MESSAGES[lang]["consumable.created"]}


@router.get("/", summary="Get a consumable list")
def get_consumables(lang: str = Depends(get_lang),
                    db: Session = Depends(get_db)):
    query = select(ConsumableModel)
    data = db.execute(query)

    return {"data": data.scalars().all(),
            "ok": True,
            "message": MESSAGES[lang]["consumable.get_all"]}


@router.get("/{consumable_id}", summary="Get a consumable")
def get_consumable(lang: str = Depends(get_lang),
                   consumable: ConsumableModel = Depends(check_consumable_exists)):
    return {"data": consumable,
            "ok": True,
            "message": MESSAGES[lang]["consumable.get"]}


@router.get("/{consumable_id}/qrcode",
            tags=["Consumables", "QR-codes"],
            summary="Get consumable QR-code")
def get_qrcode(consumable: ConsumableModel = Depends(check_consumable_exists)):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(consumable.id)
    qr_img = qr.make_image(image_factory=StyledPilImage, embedded_image_path=assets_dir / "AE.png")

    buffer = BytesIO()
    qr_img = qr_img.resize((500, 500))
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(content=buffer.read(), media_type="image/png")


@router.patch("/{consumable_id}", tags=["Consumables"], summary="Update a consumable")
def update_consumable(patch_data: ConsumablePatchSchema,
                      lang: str = Depends(get_lang),
                      db: Session = Depends(get_db),
                      consumable: ConsumableModel = Depends(check_consumable_exists)):
    consumable_patch = patch_data.model_dump(exclude_unset=True)

    if not consumable_patch:
        raise HTTPException(status_code=400, detail=MESSAGES[lang]["common.no_upd_data"])

    for key, value in consumable_patch.items():
        setattr(consumable, key, value)

    db.add(consumable)
    db.commit()
    db.refresh(consumable)

    return {"data": consumable,
            "ok": True,
            "message": MESSAGES[lang]["consumable.created"]}


@router.delete("/{consumable_id}", tags=["Consumables"], summary="Delete a consumable")
def delete_consumable(db: Session = Depends(get_db),
                      lang: str = Depends(get_lang),
                      consumable: ConsumableModel = Depends(check_consumable_exists)):

    db.delete(consumable)
    db.commit()

    return {"ok": True,
            "message": MESSAGES[lang]["consumable.deleted"]}
