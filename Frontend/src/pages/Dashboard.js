import React, { useState } from 'react';
import InvoiceUpload from '../components/invoice/InvoiceUpload';
import ExpenseTable from '../components/expense/ExpenseTable';

const Dashboard = () => {
    const [activeTab, setActiveTab] = useState('upload');

    return (
        <div className="min-h-screen bg-slate-50 text-slate-900 font-sans tracking-tight" dir="ltr">
            {/* Header */}
<nav className="sticky top-0 z-50 backdrop-blur-md bg-white/75 border-b border-slate-200/60 px-8 py-4 flex justify-between items-center">
    <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200">
            <span className="text-white font-bold text-xl">F</span>
        </div>
        <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-600">

        </h1>
    </div>
    <button className="group flex items-center gap-2 text-sm font-semibold text-slate-600 hover:text-rose-600 transition-colors">

        <div className="p-2 bg-slate-100 rounded-lg group-hover:bg-rose-50 transition-colors">

        </div>
    </button>
</nav>
            <main className="max-w-6xl mx-auto p-12">
                {/* Tab Switcher */}
                <div className="flex justify-center mb-12">
                    <div className="inline-flex p-1.5 bg-slate-200/50 rounded-2xl border border-slate-200 shadow-inner">
                        <button onClick={() => setActiveTab('upload')}
                            className={`px-10 py-3 rounded-xl text-[11px] font-black uppercase tracking-widest transition-all duration-300 ${activeTab === 'upload' ? 'bg-white text-indigo-600 shadow-lg' : 'text-slate-400 hover:text-slate-600'}`}>New Upload</button>
                        <button onClick={() => setActiveTab('manage')}
                            className={`px-10 py-3 rounded-xl text-[11px] font-black uppercase tracking-widest transition-all duration-300 ${activeTab === 'manage' ? 'bg-white text-indigo-600 shadow-lg' : 'text-slate-400 hover:text-slate-600'}`}>Management</button>
                    </div>
                </div>

                {/* Content Area */}
                <div className="bg-white rounded-[2.5rem] shadow-2xl shadow-slate-200/60 border border-slate-100 p-8 min-h-[500px]">
                    {activeTab === 'upload' ? <InvoiceUpload /> : <ExpenseTable />}
                </div>
            </main>
        </div>
    );
};

export default Dashboard;