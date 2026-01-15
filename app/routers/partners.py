from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import models, schemas, auth, database

router = APIRouter(prefix="/partners", tags=["Partners"])

@router.get("/me", response_model=schemas.PartnerOut)
async def get_my_profile(current_partner: models.Partner = Depends(auth.get_current_partner)):
    return current_partner

@router.put("/me", response_model=schemas.PartnerOut)
async def update_profile(
    partner_update: schemas.PartnerBase,
    db: AsyncSession = Depends(database.get_db),
    current_partner: models.Partner = Depends(auth.get_current_partner)
):
    for key, value in partner_update.dict().items():
        setattr(current_partner, key, value)
    
    await db.commit()
    await db.refresh(current_partner)
    return current_partner
