



from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from uuid import UUID
from ..models.expense import Expense
from ..models.invoice import Invoice
from ..schemas.expense_schemas import ExpenseFilter


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_expenses_with_filters(self, user_id: UUID, filters: ExpenseFilter) -> List[Expense]:
        """
        Fetches expenses for a specific user with dynamic server-side filtering.
        Joins with Invoices to filter by Business Name or Amount.
        """
        # Start the query by joining Expense and Invoice
        query = self.db.query(Expense).join(Invoice).filter(Expense.user_id == user_id)

        # Apply Filters dynamically if they are provided
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
            # Case-insensitive search (ILIKE in PostgreSQL)
            query = query.filter(Invoice.business_name.ilike(f"%{filters.business_name}%"))

        # Execute and return results
        return query.all()

    def create_expense(self, expense_data: Expense) -> Expense:
        """Saves a new expense record to the database."""
        self.db.add(expense_data)
        self.db.commit()
        self.db.refresh(expense_data)
        return expense_data