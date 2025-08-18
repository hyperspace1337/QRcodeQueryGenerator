from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from core.translation import MESSAGES
from database.database import get_db
from models.consumable import ConsumableModel
from schemas.consumable import ConsumableAddSchema, ConsumablePatchSchema
from dependencies.dependencies import check_consumable_exists, get_lang
from services.consumable_services import create_consumable_service, get_consumables_service, get_qr_service, \
    patch_consumable_service, delete_consumable_service

router = APIRouter(
    prefix="/consumables",
    tags=["Consumables"],
)


@router.post("/", summary="Create a consumable")
def create_consumable(consumable: ConsumableAddSchema,
                      db: Session = Depends(get_db),
                      lang: str = Depends(get_lang)):
    new_consumable = create_consumable_service(consumable, db)

    return {"data": new_consumable,
            "ok": True,
            "message": MESSAGES[lang]["consumable.created"]}


@router.get("/", summary="Get a consumable list")
def get_consumables(lang: str = Depends(get_lang),
                    db: Session = Depends(get_db)):
    consumables_list = get_consumables_service(db)

    return {"data": consumables_list,
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
    qr_buffer = get_qr_service(consumable)

    return Response(content=qr_buffer.read(), media_type="image/png")


@router.patch("/{consumable_id}", tags=["Consumables"], summary="Update a consumable")
def update_consumable(patch_data: ConsumablePatchSchema,
                      lang: str = Depends(get_lang),
                      db: Session = Depends(get_db),
                      consumable: ConsumableModel = Depends(check_consumable_exists)):
    consumable = patch_consumable_service(patch_data, lang, db, consumable)

    return {"data": consumable,
            "ok": True,
            "message": MESSAGES[lang]["consumable.created"]}


@router.delete("/{consumable_id}", tags=["Consumables"], summary="Delete a consumable")
def delete_consumable(db: Session = Depends(get_db),
                      lang: str = Depends(get_lang),
                      consumable: ConsumableModel = Depends(check_consumable_exists)):

    delete_consumable_service(db, consumable)

    return {"ok": True,
            "message": MESSAGES[lang]["consumable.deleted"]}
