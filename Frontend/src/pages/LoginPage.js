import React, { useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom'; // 1. ייבוא ה-Hook לניווט

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate(); // 2. אתחול הניווט

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // שימוש ב-URLSearchParams עבור OAuth2 ב-FastAPI
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await api.post('/api/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            // שמירת הטוקן ב-Context
            login(response.data.access_token);

            alert('מחובר בהצלחה!');

            // 3. מעבר לדף ה-Dashboard לאחר הצלחה
            navigate('/dashboard');

        } catch (error) {
            console.error(error);
            alert('שגיאה בהתחברות: ' + (error.response?.data?.detail || 'בדוק את הפרטים'));
        }
    };

    return (
        <div className="login-container" style={{ textAlign: 'center', marginTop: '100px' }}>
            <h2 className="text-xl font-bold mb-4">התחברות למערכת</h2>
            <form onSubmit={handleSubmit} className="flex flex-col gap-3 max-w-sm mx-auto">
                <input
                    className="border p-2 rounded"
                    type="email"
                    placeholder="אימייל"
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    className="border p-2 rounded"
                    type="password"
                    placeholder="סיסמה"
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button
                    type="submit"
                    className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
                >
                    כניסה
                </button>
            </form>
        </div>
    );
};

export default LoginPage;