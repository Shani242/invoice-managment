from sqlalchemy.orm import Session, joinedload
from typing import List
from uuid import UUID
from ..models.expense import Expense
from ..models.invoice import Invoice
from ..schemas.expense_schemas import ExpenseFilter


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_expenses_with_filters(self, user_id: int, filters: ExpenseFilter) -> List[Expense]:
        # Use joinedload to ensure the invoice data is fetched in one query
        query = self.db.query(Expense).join(Invoice).options(joinedload(Expense.invoice)).filter(
            Expense.user_id == user_id)

        if filters.category:
            query = query.filter(Expense.category == filters.category)
        if filters.start_date:
            query = query.filter(Invoice.transaction_date >= filters.start_date)
        if filters.end_date:
            query = query.filter(Invoice.transaction_date <= filters.end_date)
        if filters.min_amount:
            query = query.filter(Invoice.amount_after_vat >= filters.min_amount)
        if filters.max_amount:
            query = query.filter(Invoice.amount_after_vat <= filters.max_amount)
        if filters.business_name:
            query = query.filter(Invoice.business_name.ilike(f"%{filters.business_name}%"))

        results = query.all()

        # FLATTENING LOGIC: Attach invoice fields to the expense object
        # This satisfies the ExpenseResponse schema requirements
        for exp in results:
            exp.business_name = exp.invoice.business_name
            exp.amount_before_vat = exp.invoice.amount_before_vat
            exp.amount_after_vat = exp.invoice.amount_after_vat
            exp.transaction_date = exp.invoice.transaction_date
            exp.invoice_number = exp.invoice.invoice_number

        return results

    def create_expense(self, expense_data: Expense) -> Expense:
        """Saves a new expense record to the database."""
        self.db.add(expense_data)
        self.db.commit()
        self.db.refresh(expense_data)
        return expense_data