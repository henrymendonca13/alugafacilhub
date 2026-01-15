from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import models, schemas, auth, database

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/", response_model=schemas.PropertyOut)
async def create_property(
    prop: schemas.PropertyCreate,
    db: AsyncSession = Depends(database.get_db),
    current_partner: models.Partner = Depends(auth.get_current_partner)
):
    if current_partner.status != models.PartnerStatus.ACTIVE:
        raise HTTPException(status_code=403, detail="Assinatura inativa.")

    new_prop = models.Property(**prop.dict(), owner_id=current_partner.id)
    db.add(new_prop)
    await db.commit()
    await db.refresh(new_prop)
    return new_prop

@router.get("/", response_model=List[schemas.PropertyOut])
async def list_properties(
    db: AsyncSession = Depends(database.get_db),
    current_partner: models.Partner = Depends(auth.get_current_partner)
):
    result = await db.execute(select(models.Property).where(models.Property.owner_id == current_partner.id))
    return result.scalars().all()

@router.delete("/{prop_id}")
async def delete_property(
    prop_id: int,
    db: AsyncSession = Depends(database.get_db),
    current_partner: models.Partner = Depends(auth.get_current_partner)
):
    result = await db.execute(select(models.Property).where(models.Property.id == prop_id, models.Property.owner_id == current_partner.id))
    prop = result.scalars().first()
    if not prop:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")
    
    await db.delete(prop)
    await db.commit()
    return {"status": "removido"}
