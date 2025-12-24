import React, { useState } from 'react';
import InvoiceUpload from '../components/invoice/InvoiceUpload';
import ExpenseTable from '../components/expense/ExpenseTable';

const Dashboard = () => {
    const [activeTab, setActiveTab] = useState('upload'); // 'upload' או 'manage'

    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-6">מערכת ניהול חשבוניות</h1>

            {/* מנגנון הטאבים */}
            <div className="flex border-b mb-6">
                <button
                    className={`p-4 ${activeTab === 'upload' ? 'border-b-2 border-blue-500 font-bold' : ''}`}
                    onClick={() => setActiveTab('upload')}
                >
                    העלאת חשבוניות
                </button>
                <button
                    className={`p-4 ${activeTab === 'manage' ? 'border-b-2 border-blue-500 font-bold' : ''}`}
                    onClick={() => setActiveTab('manage')}
                >
                    ניהול הוצאות
                </button>
            </div>

            {/* הצגת תוכן לפי הטאב הפעיל */}
            <div>
                {activeTab === 'upload' ? <InvoiceUpload /> : <ExpenseTable />}
            </div>
        </div>
    );
};

export default Dashboard;