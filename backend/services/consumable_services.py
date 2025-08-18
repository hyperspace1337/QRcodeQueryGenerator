from io import BytesIO

import qrcode
from fastapi import HTTPException
from qrcode.image.styledpil import StyledPilImage
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import assets_dir
from core.translation import MESSAGES
from models.consumable import ConsumableModel
from schemas.consumable import ConsumableAddSchema, ConsumablePatchSchema


def create_consumable_service(consumable: ConsumableAddSchema, db: Session):
    new_consumable = ConsumableModel(
        name=consumable.name,
        erp_code=consumable.erp_code,
        qty=consumable.qty,
        department=consumable.department
    )

    db.add(new_consumable)
    db.commit()
    db.refresh(new_consumable)

    return new_consumable


def get_consumables_service(db: Session):
    query = select(ConsumableModel)
    consumables_list = db.execute(query)
    consumables_list = consumables_list.scalars().all()

    return consumables_list


def get_qr_service(consumable: ConsumableModel):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(consumable.id)
    qr_img = qr.make_image(image_factory=StyledPilImage, embedded_image_path=assets_dir / "AE.png")

    buffer = BytesIO()
    qr_img = qr_img.resize((500, 500))
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer

def patch_consumable_service(patch_data: ConsumablePatchSchema,
                             lang: str,
                             db: Session,
                             consumable: ConsumableModel
                             ):
    consumable_patch = patch_data.model_dump(exclude_unset=True)
    if not consumable_patch:
        raise HTTPException(status_code=400, detail=MESSAGES[lang]["common.no_upd_data"])

    for key, value in consumable_patch.items():
        setattr(consumable, key, value)

    db.add(consumable)
    db.commit()
    db.refresh(consumable)

    return consumable

def delete_consumable_service(db: Session,
                              consumable: ConsumableModel):
    db.delete(consumable)
    db.commit()

    return ...