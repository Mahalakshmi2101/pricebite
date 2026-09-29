import React, { useState } from 'react';
import { X } from 'lucide-react';
import { loginUser, registerUser, getMe } from '../api';

export default function AuthModal({ mode, onClose, onSuccess, switchMode }) {
    const [form, setForm] = useState({ name: '', email: '', password: '' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            if (mode === 'register') {
                await registerUser({ name: form.name, email: form.email, password: form.password });
            }
            const data = await loginUser({ email: form.email, password: form.password });
            const userData = await getMe();
            onSuccess(data.access_token, userData);
        } catch (err) {
            setError(err.response?.data?.detail || 'Something went wrong');
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 relative">
                <button onClick={onClose} className="absolute top-4 right-4 p-1 rounded-lg hover:bg-slate-100">
                    <X className="w-4 h-4 text-slate-500" />
                </button>

                <h2 className="text-xl font-black text-slate-900 mb-1">
                    {mode === 'login' ? 'Welcome back' : 'Create account'}
                </h2>
                <p className="text-xs text-slate-500 mb-6">
                    {mode === 'login' ? 'Sign in to get price alerts and notifications.' : 'Start comparing food prices across Chennai.'}
                </p>

                <form onSubmit={handleSubmit} className="space-y-3">
                    {mode === 'register' && (
                        <input
                            className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-orange-400"
                            placeholder="Full name"
                            value={form.name}
                            onChange={(e) => setForm({ ...form, name: e.target.value })}
                            required
                        />
                    )}
                    <input
                        type="email"
                        className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-orange-400"
                        placeholder="Email"
                        value={form.email}
                        onChange={(e) => setForm({ ...form, email: e.target.value })}
                        required
                    />
                    <input
                        type="password"
                        className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-orange-400"
                        placeholder="Password"
                        value={form.password}
                        onChange={(e) => setForm({ ...form, password: e.target.value })}
                        required
                        minLength={6}
                    />
                    {error && <p className="text-xs text-rose-600">{error}</p>}
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-2.5 rounded-xl bg-orange-500 text-white text-sm font-bold hover:bg-orange-600 transition-colors disabled:opacity-60"
                    >
                        {loading ? 'Please wait...' : mode === 'login' ? 'Sign in' : 'Create account'}
                    </button>
                </form>

                <p className="text-xs text-slate-500 text-center mt-4">
                    {mode === 'login' ? "No account? " : "Already have one? "}
                    <button onClick={() => switchMode(mode === 'login' ? 'register' : 'login')} className="text-orange-500 font-semibold hover:underline">
                        {mode === 'login' ? 'Sign up' : 'Sign in'}
                    </button>
                </p>
            </div>
        </div>
    );
}