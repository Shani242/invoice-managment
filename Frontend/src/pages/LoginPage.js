import React, { useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const [isRegister, setIsRegister] = useState(false); // Toggle state
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            if (isRegister) {
                // Registration Flow
                await api.post('/api/auth/register', { email, password });
                alert('Account created! Please sign in.');
                setIsRegister(false); // Switch back to login after success
            } else {
                // Login Flow
                const formData = new URLSearchParams();
                formData.append('username', email);
                formData.append('password', password);

                const response = await api.post('/api/auth/login', formData, {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
                });

                login(response.data.access_token);
                navigate('/dashboard');
            }
        } catch (error) {
            console.error(error);
            alert('Error: ' + (error.response?.data?.detail || 'Something went wrong'));
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <div className="flex justify-center mb-6">
                    <div className="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-indigo-200">
                        I
                    </div>
                </div>
                <h2 className="text-center text-3xl font-black text-slate-900 tracking-tight">
                    {isRegister ? "Create an account" : "Sign in to Invoicely"}
                </h2>
                <p className="mt-2 text-center text-sm text-slate-500">
                    {isRegister ? "Already have an account?" : "New to the platform?"}
                    <button
                        onClick={() => setIsRegister(!isRegister)}
                        className="ml-1 font-bold text-indigo-600 hover:text-indigo-500 transition-colors"
                    >
                        {isRegister ? "Sign in here" : "Register now"}
                    </button>
                </p>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                <div className="bg-white py-10 px-4 shadow-2xl shadow-slate-200/50 border border-slate-100 sm:rounded-[2rem] sm:px-10">
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <div>
                            <label className="block text-xs font-black text-slate-400 uppercase tracking-widest">Email Address</label>
                            <input
                                type="email"
                                required
                                onChange={(e) => setEmail(e.target.value)}
                                className="mt-2 block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition-all"
                                placeholder="name@company.com"
                            />
                        </div>

                        <div>
                            <label className="block text-xs font-black text-slate-400 uppercase tracking-widest">Password</label>
                            <input
                                type="password"
                                required
                                onChange={(e) => setPassword(e.target.value)}
                                className="mt-2 block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition-all"
                                placeholder="••••••••"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className={`w-full py-4 px-4 rounded-xl font-black uppercase tracking-widest text-white transition-all duration-300 ${
                                isLoading ? 'bg-slate-300 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 shadow-xl shadow-indigo-100 active:scale-95'
                            }`}
                        >
                            {isLoading ? "Processing..." : (isRegister ? "Create Account" : "Sign In")}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;