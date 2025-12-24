import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const ExpenseTable = () => {
    const [expenses, setExpenses] = useState([]);
    const [filters, setFilters] = useState({ category: '', business_name: '' });

    const fetchExpenses = async () => {
        try {
            // שליחת הסינון כ-Params לשרת (Server-side filtering)
            const res = await api.get('/api/expenses', { params: filters });
            setExpenses(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchExpenses();
    }, [filters]); // טעינה מחדש בכל שינוי פילטר

    return (
        <div>
            {/* שורת סינון */}
            <div className="flex gap-4 mb-4">
                <input
                    placeholder="שם עסק..."
                    onChange={(e) => setFilters({...filters, business_name: e.target.value})}
                    className="border p-2"
                />
                <select
                    onChange={(e) => setFilters({...filters, category: e.target.value})}
                    className="border p-2"
                >
                    <option value="">כל הקטגוריות</option>
                    <option value="מזון">מזון</option>
                    <option value="רכב">רכב</option>
                    {/* שאר הקטגוריות */}
                </select>
            </div>

            {/* טבלת נתונים */}
            <table className="w-full text-right border">
                <thead className="bg-gray-100">
                    <tr>
                        <th className="p-2 border">עסק</th>
                        <th className="p-2 border">תאריך</th>
                        <th className="p-2 border">סכום (כולל מע"מ)</th>
                        <th className="p-2 border">קטגוריה</th>
                    </tr>
                </thead>
                <tbody>
                    {expenses.map(exp => (
                        <tr key={exp.id}>
                            <td className="p-2 border">{exp.business_name}</td>
                            <td className="p-2 border">{exp.transaction_date}</td>
                            <td className="p-2 border">{exp.amount_after_vat} ₪</td>
                            <td className="p-2 border">{exp.category}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ExpenseTable;