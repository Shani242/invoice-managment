import React, { useState } from 'react';
import api from '../../services/api';

const InvoiceUpload = () => {
    const [file, setFile] = useState(null);
    const [category, setCategory] = useState('אחר');
    const [loading, setLoading] = useState(false);

    const handleUpload = async () => {
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', category);
        setLoading(true);
        try {
            await api.post('api/invoice/upload', formData);
            alert("Analysis Complete!");
            setFile(null);
        } catch (err) { alert("Error"); }
        finally { setLoading(false); }
    };

    return (
        <div className="max-w-2xl mx-auto py-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="space-y-10">
                <div className="text-center">
                    <h3 className="text-3xl font-black text-slate-800 tracking-tight">Extract Invoice Data</h3>
                    <p className="text-slate-400 mt-2 font-medium">Upload your document to process financial details automatically.</p>
                </div>

                {/* Dropzone */}
                <div className={`relative border-2 border-dashed rounded-[2rem] p-20 transition-all duration-500 flex flex-col items-center justify-center ${file ? 'border-indigo-500 bg-indigo-50/50' : 'border-slate-200 hover:border-indigo-400 hover:bg-slate-50'}`}>
                    <div className="w-16 h-16 bg-white rounded-2xl shadow-sm border border-slate-100 flex items-center justify-center text-3xl mb-4">{file ? '✅' : '📤'}</div>
                    <p className="text-sm font-bold text-slate-600 uppercase tracking-widest">{file ? file.name : "Select File"}</p>
                    <input type="file" className="absolute inset-0 opacity-0 cursor-pointer" onChange={(e) => setFile(e.target.files[0])} />
                </div>

                {/* Category Grid */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {['רכב', 'מזון', 'IT', 'תפעול', 'הדרכה/הכשרה', 'אחר'].map((cat) => (
                        <button key={cat} onClick={() => setCategory(cat)}
                            className={`py-4 rounded-2xl text-[10px] font-black uppercase tracking-widest border transition-all ${category === cat ? 'bg-indigo-600 border-indigo-600 text-white shadow-xl shadow-indigo-100' : 'bg-white border-slate-100 text-slate-500 hover:border-indigo-200'}`}>
                            {cat === 'אחר' ? 'Other' : cat}
                        </button>
                    ))}
                </div>

                <button onClick={handleUpload} disabled={!file || loading}
                    className="w-full py-5 rounded-2xl bg-indigo-600 text-white font-black uppercase tracking-[0.2em] shadow-2xl shadow-indigo-200 hover:bg-indigo-700 active:scale-95 transition-all disabled:bg-slate-200 disabled:shadow-none">
                    {loading ? "AI is processing..." : "Start Analysis"}
                </button>
            </div>
        </div>
    );
};

export default InvoiceUpload;