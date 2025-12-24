from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from enum import Enum

class ExpenseCategory(str, Enum):
    VEHICLE = "רכב"
    FOOD = "מזון"
    OPERATIONS = "תפעול"
    IT = "IT"
    TRAINING = "הדרכה/הכשרה"
    OTHER = "אחר"

class ExpenseBase(BaseModel):
    category: ExpenseCategory
    notes: Optional[str] = None

class ExpenseResponse(ExpenseBase):
    id: int
    invoice_id: int
    business_name: str
    amount_before_vat: float
    amount_after_vat: float
    transaction_date: date
    invoice_number: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ExpenseFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    category: Optional[ExpenseCategory] = None
    business_name: Optional[str] = None