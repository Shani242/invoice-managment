from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .deps import get_current_user
from ..services.ocr_service import OCRService
from ..repositories.expense_repo import ExpenseRepository
from ..schemas.expense_schemas import ExpenseResponse, ExpenseFilter, ExpenseCategory
from ..models.user import User
from ..models.invoice import Invoice as InvoiceModel
from ..models.expense import Expense as ExpenseModel

router = APIRouter(prefix="/api", tags=["Invoices & Expenses"])

# Initialize Services
ocr_service = OCRService()

@router.post("/invoice/upload")
async def upload_invoice(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # ולידציה של סוג קובץ
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()

    # הפעלת שירות ה-OCR
    ocr_data = await ocr_service.process_invoice(contents)

    try:
        # יצירת רשומה בטבלת חשבוניות
        new_invoice = InvoiceModel(
            user_id=current_user.id,
            document_type=ocr_data.document_type,
            business_name=ocr_data.business_name,
            company_id=ocr_data.business_vat_number,  # תואם ל-Model (ח"פ/עוסק)
            amount_before_vat=ocr_data.amount_before_vat,
            amount_after_vat=ocr_data.amount_after_vat,
            transaction_date=ocr_data.transaction_date
        )

        db.add(new_invoice)
        db.flush()  # קבלת ה-ID של החשבונית לפני ה-Commit הסופי

        # יצירת רשומה בטבלת הוצאות המקושרת לחשבונית
        new_expense = ExpenseModel(
            invoice_id=new_invoice.id,
            user_id=current_user.id,
            category=ExpenseCategory.OTHER,
            notes="Automatically processed"
        )

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        # החזרת נתונים בצורה גמישה למניעת שגיאות Serialization
        return {
            "status": "success",
            "expense_id": new_expense.id,
            "business_name": new_invoice.business_name,
            "amount": new_invoice.amount_after_vat,
            "date": new_invoice.transaction_date
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/expenses", response_model=List[ExpenseResponse])
async def get_expenses(
        category: ExpenseCategory = None,
        business_name: str = None,
        min_amount: float = None,
        max_amount: float = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """סינון צד שרת המבוסס על המשתמש המחובר בלבד"""
    repo = ExpenseRepository(db)

    filters = ExpenseFilter(
        category=category,
        business_name=business_name,
        min_amount=min_amount,
        max_amount=max_amount
    )

    # שליפת נתונים דרך ה-Repository
    expenses = repo.get_user_expenses_with_filters(user_id=current_user.id, filters=filters)
    return expenses