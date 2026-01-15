from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum

class PartnerStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"

class PartnerBase(BaseModel):
    email: EmailStr
    responsible_name: str
    company_name: str
    creci: str
    cpf_cnpj: str
    city: str
    whatsapp: str
    website: Optional[str] = None

class PartnerCreate(PartnerBase):
    password: str

class PartnerOut(PartnerBase):
    id: int
    status: PartnerStatus
    slug: str

    class Config:
        from_attributes = True

class PropertyBase(BaseModel):
    title: str
    property_type: str
    bedrooms: int
    suites: int
    parking: int
    area_m2: float
    rent_price: float
    condo_fee: float
    iptu: float
    city: str
    description: str

class PropertyCreate(PropertyBase):
    pass

class PropertyOut(PropertyBase):
    id: int
    is_active: bool
    owner_id: int

    class Config:
        from_attributes = True
