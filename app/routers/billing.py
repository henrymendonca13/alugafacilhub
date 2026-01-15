from fastapi import APIRouter, Depends, HTTPException
import stripe
import os
from .. import models, auth

router = APIRouter(prefix="/billing", tags=["Billing"])
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/create-portal")
async def customer_portal(current_partner: models.Partner = Depends(auth.get_current_partner)):
    # Cria um link para o cliente gerenciar o cartão ou cancelar a assinatura no próprio Stripe
    if not current_partner.stripe_customer_id:
        raise HTTPException(status_code=400, detail="Nenhuma assinatura encontrada.")
    
    session = stripe.billing_portal.Session.create(
        customer=current_partner.stripe_customer_id,
        return_url="https://app.alugafacilhub.com/dashboard",
    )
    return {"url": session.url}

@router.get("/status")
async def get_billing_status(current_partner: models.Partner = Depends(auth.get_current_partner)):
    return {
        "status": current_partner.status,
        "is_active": current_partner.status == models.PartnerStatus.ACTIVE
    }
