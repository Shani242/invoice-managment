import React, { useState, useEffect, useMemo } from 'react';
import api from '../../services/api';
import { ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-react';
// Modern icons
const ExpenseTable = () => {
    const [expenses, setExpenses] = useState([]);
    const [filters, setFilters] = useState({
        category: '', business_name: '', start_date: '', end_date: '', min_amount: '', max_amount: ''
    });
    const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

    const fetchExpenses = async () => {
        try {
            const res = await api.get('/api/expenses', { params: filters });
            setExpenses(res.data);
        } catch (err) { console.error(err); }
    };

    useEffect(() => { fetchExpenses(); }, [filters]);

    const handleSort = (key) => {
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
    };

    const getSortedExpenses = () => {
        if (!sortConfig.key) return expenses;

        const sorted = [...expenses].sort((a, b) => {
            let aVal = a[sortConfig.key];
            let bVal = b[sortConfig.key];

            // Handle date sorting
            if (sortConfig.key === 'transaction_date') {
                aVal = new Date(aVal);
                bVal = new Date(bVal);
            }

            // Handle numeric sorting
            if (sortConfig.key === 'amount_before_vat' || sortConfig.key === 'amount_after_vat') {
                aVal = Number(aVal);
                bVal = Number(bVal);
            }

            if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
            if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
            return 0;
        });

        return sorted;
    };

    const SortIcon = ({ columnKey }) => {
        if (sortConfig.key !== columnKey) {
            return <ChevronsUpDown className="w-3 h-3 text-slate-300" />;
        }
        return sortConfig.direction === 'asc'
            ? <ChevronUp className="w-3 h-3 text-indigo-600" />
            : <ChevronDown className="w-3 h-3 text-indigo-600" />;
    };

    const sortedExpenses = getSortedExpenses();

    return (
        <div className="animate-in fade-in duration-500 p-6">
            {/* Filter Panel */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10 bg-slate-50/50 p-6 rounded-2xl border border-slate-100">
                <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Search</label>
                    <input type="text" placeholder="Vendor name..." className="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                        onChange={(e) => setFilters({...filters, business_name: e.target.value})} />
                </div>

                <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Category</label>
                    <select className="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                        onChange={(e) => setFilters({...filters, category: e.target.value})}>
                        <option value="רכב">Vehicle</option>
                        <option value="מזון">Food</option>
                        <option value="תפעול">Operations</option>
                        <option value="IT">IT</option>
                        <option value="הדרכה/הכשרה">Training</option>
                        <option value="אחר">Other</option>
                    </select>
                </div>

                <div className="space-y-2">

                </div>


            </div>

            {/* Styled Table */}
            <div className="overflow-hidden rounded-2xl border border-slate-100 shadow-sm">
                <table className="w-full text-left">
                    <thead className="bg-slate-50 text-slate-400 text-[10px] font-black uppercase tracking-widest border-b border-slate-100">
                        <tr>
                            <th className="px-6 py-4 cursor-pointer hover:bg-slate-100 transition-colors" onClick={() => handleSort('business_name')}>
                                <div className="flex items-center gap-2">
                                    Vendor
                                    <SortIcon columnKey="business_name" />
                                </div>
                            </th>
                            <th className="px-6 py-4 cursor-pointer hover:bg-slate-100 transition-colors" onClick={() => handleSort('transaction_date')}>
                                <div className="flex items-center gap-2">
                                    Date
                                    <SortIcon columnKey="transaction_date" />
                                </div>
                            </th>
                            <th className="px-6 py-4 cursor-pointer hover:bg-slate-100 transition-colors" onClick={() => handleSort('amount_before_vat')}>
                                <div className="flex items-center gap-2">
                                    Excl. VAT
                                    <SortIcon columnKey="amount_before_vat" />
                                </div>
                            </th>
                            <th className="px-6 py-4 cursor-pointer hover:bg-slate-100 transition-colors" onClick={() => handleSort('amount_after_vat')}>
                                <div className="flex items-center gap-2">
                                    Total Amount
                                    <SortIcon columnKey="amount_after_vat" />
                                </div>
                            </th>
                            <th className="px-6 py-4">Invoice #</th>
                            <th className="px-6 py-4">Status</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 bg-white">
                        {sortedExpenses.map((exp) => (
                            <tr key={exp.id} className="hover:bg-slate-50/50 transition-colors group">
                                <td className="px-6 py-4 font-bold text-slate-700">{exp.business_name}</td>
                                <td className="px-6 py-4 text-slate-500 text-sm">{exp.transaction_date}</td>
                                <td className="px-6 py-4 text-slate-500 text-sm">₪{exp.amount_before_vat}</td>
                                <td className="px-6 py-4 text-indigo-600 font-extrabold text-sm">₪{exp.amount_after_vat}</td>
                                <td className="px-6 py-4 text-slate-400 font-mono text-xs">{exp.invoice_number || 'N/A'}</td>
                                <td className="px-6 py-4">
                                    <span className="px-3 py-1 rounded-full bg-indigo-50 text-indigo-600 text-[10px] font-bold uppercase tracking-wider">
                                        {exp.category}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ExpenseTable;