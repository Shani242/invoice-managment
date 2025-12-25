from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import Query
from typing import Optional
from ..database import get_db
from .deps import get_current_user
from ..services.ocr_service import OCRService
from ..repositories.expense_repo import ExpenseRepository
from ..schemas.expense_schemas import ExpenseResponse, ExpenseFilter, ExpenseCategory
from ..models.user import User
from ..models.invoice import Invoice as InvoiceModel
from ..models.expense import Expense as ExpenseModel
from fastapi import Form

router = APIRouter(prefix="/api", tags=["Invoices & Expenses"])

# Initialize Services
ocr_service = OCRService()
@router.post("/invoice/upload")
async def upload_invoice(
        file: UploadFile = File(...),
        category: ExpenseCategory = Form(ExpenseCategory.OTHER),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()
    ocr_data = await ocr_service.process_invoice(contents)
    try:
        # 1. Create the Invoice record
        new_invoice = InvoiceModel(
            user_id=current_user.id,
            document_type=ocr_data.document_type,
            business_name=ocr_data.business_name,
            company_id=ocr_data.business_vat_number,
            amount_before_vat=ocr_data.amount_before_vat,
            amount_after_vat=ocr_data.amount_after_vat,
            transaction_date=ocr_data.transaction_date
        )
        db.add(new_invoice)
        db.flush() # This generates new_invoice.id

        # 2. Create the Expense record using the category from the Form
        new_expense = ExpenseModel(
            invoice_id=new_invoice.id,
            user_id=current_user.id,
            category=category, # Now 'category' is resolved
            notes="Automatically processed"
        )

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

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
        category: Optional[ExpenseCategory] = Query(None),
        business_name: Optional[str] = Query(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    category_val = category if category != "" else None

    repo = ExpenseRepository(db)
    filters = ExpenseFilter(
        category=category_val,
        business_name=business_name if business_name != "" else None
    )

    expenses = repo.get_user_expenses_with_filters(user_id=current_user.id, filters=filters)
    return expenses