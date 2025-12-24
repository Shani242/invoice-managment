
from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class DocumentType(str, Enum):
    INVOICE = "חשבונית"
    RECEIPT = "קבלה"

class InvoiceOCRResponse(BaseModel):
    document_type: DocumentType
    business_name: str
    business_vat_number: str
    amount_before_vat: float
    amount_after_vat: float
    transaction_date: date
    invoice_number: Optional[str] = None
    service_description: Optional[str] = None