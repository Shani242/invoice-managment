import React, { useState } from 'react';
import api from '../../services/api';

const InvoiceUpload = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleUpload = async () => {
        if (!file) return alert("אנא בחר קובץ");

        const formData = new FormData();
        formData.append('file', file); // 'file' חייב להתאים לשם הפרמטר ב-FastAPI

        setLoading(true);
        try {
            await api.post('api/invoice/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            alert("החשבונית נשלחה ונותחה בהצלחה!");
        } catch (err) {
            alert("שגיאה בהעלאה: " + err.response?.data?.detail);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-gray-50 p-6 border-dashed border-2 border-gray-300 rounded-lg text-center">
            <input
                type="file"
                accept="image/*,.pdf"
                onChange={(e) => setFile(e.target.files[0])}
                className="mb-4"
            />
            <button
                onClick={handleUpload}
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-2 rounded"
            >
                {loading ? "מנתח חשבונית..." : "העלה ונתח"}
            </button>
        </div>
    );
};

export default InvoiceUpload;