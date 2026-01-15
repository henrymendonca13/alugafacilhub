from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class PartnerStatus(enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"

# Tabela associativa Imóvel <-> Evento
property_events = Table(
    "property_events",
    Base.metadata,
    Column("property_id", ForeignKey("properties.id"), primary_key=True),
    Column("event_name", String, primary_key=True)
)

class Partner(Base):
    __tablename__ = "partners"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    company_name = Column(String)
    creci = Column(String)
    status = Column(Enum(PartnerStatus), default=PartnerStatus.PENDING)
    stripe_customer_id = Column(String, nullable=True)
    slug = Column(String, unique=True)
    
    properties = relationship("Property", back_pop_ref="owner")

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    rent_price = Column(Float)
    city = Column(String)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("partners.id"))
    
    owner = relationship("Partner", back_pop_ref="properties")
