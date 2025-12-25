from sqlalchemy.orm import Session, joinedload
from typing import List
from ..models.expense import Expense
from ..models.invoice import Invoice
from ..schemas.expense_schemas import ExpenseFilter


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_expenses_with_filters(
            self,
            user_id: int,
            filters: ExpenseFilter,
            sort_by: str = "transaction_date",
            direction: str = "desc"
    ) -> List[Expense]:

        # Start the query with a join
        query = self.db.query(Expense).join(Invoice).options(joinedload(Expense.invoice)).filter(
            Expense.user_id == user_id
        )

        # --- Filtering Logic ---
        if filters.category:
            query = query.filter(Expense.category == filters.category)
        if filters.business_name:
            query = query.filter(Invoice.business_name.ilike(f"%{filters.business_name}%"))
        if filters.start_date:
            query = query.filter(Invoice.transaction_date >= filters.start_date)
        if filters.end_date:
            query = query.filter(Invoice.transaction_date <= filters.end_date)

        # --- Sorting Logic ---
        # Map frontend keys to DB columns
        sort_map = {
            "business_name": Invoice.business_name,
            "transaction_date": Invoice.transaction_date,
            "amount_after_vat": Invoice.amount_after_vat,
            "amount_before_vat": Invoice.amount_before_vat,
            "category": Expense.category
        }

        target_column = sort_map.get(sort_by, Invoice.transaction_date)

        if direction == "desc":
            query = query.order_by(target_column.desc())
        else:
            query = query.order_by(target_column.asc())

        results = query.all()

        # Flatten for the Pydantic schema
        for exp in results:
            exp.business_name = exp.invoice.business_name
            exp.amount_before_vat = exp.invoice.amount_before_vat
            exp.amount_after_vat = exp.invoice.amount_after_vat
            exp.transaction_date = exp.invoice.transaction_date
            exp.invoice_number = exp.invoice.invoice_number

        return results