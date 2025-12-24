from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    # Business Details extracted via OCR
    business_name = Column(String, index=True)
    company_id = Column(String)  # Tax ID / H.P.
    invoice_number = Column(String, nullable=True)
    document_type = Column(String)  # e.g., "Invoice" or "Receipt"

    # Financial Data
    amount_before_vat = Column(Float)
    amount_after_vat = Column(Float)
    transaction_date = Column(Date)
    service_description = Column(String, nullable=True)

    # Category (Car, Food, IT, Operations, Training, Other)
    category = Column(String, default="Other", index=True)

    # Foreign Key to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship back to the User model
    owner = relationship("User", back_populates="invoices")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())