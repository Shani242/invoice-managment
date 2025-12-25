export interface Expense {
    id: number;
    business_name: string;
    transaction_date: string;
    amount_after_vat: number;
    category: string;
}

export interface Filters {
    category: string;
    business_name: string;
}