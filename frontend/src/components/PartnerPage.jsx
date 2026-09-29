import React, { useState, useEffect } from 'react';
import { ArrowLeft, Shield, Clock, MapPin, Plus, X } from 'lucide-react';
import { getPartnerPrefs, updatePartnerPrefs } from '../api';

export default function PartnerPage({ onBack }) {
    const [prefs, setPrefs] = useState(null);
    const [cutoff, setCutoff] = useState('22:00');
    const [areas, setAreas] = useState([]);
    const [newArea, setNewArea] = useState({ name: '', reason: '' });
    const [saving, setSaving] = useState(false);
    const [saved, setSaved] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        getPartnerPrefs().then((p) => {
            setPrefs(p);
            if (p.no_delivery_after) setCutoff(p.no_delivery_after.slice(0, 5));
            if (p.avoid_areas) setAreas(p.avoid_areas);
        }).catch(() => setError('Could not load preferences'));
    }, []);

    async function handleSave() {
        setSaving(true);
        setSaved(false);
        setError('');
        try {
            await updatePartnerPrefs({ no_delivery_after: cutoff + ':00', avoid_areas: areas });
            setSaved(true);
            setTimeout(() => setSaved(false), 3000);
        } catch (e) {
            setError(e.response?.data?.detail || 'Save failed');
        } finally {
            setSaving(false);
        }
    }

    function addArea() {
        if (!newArea.name.trim()) return;
        setAreas([...areas, { name: newArea.name.trim(), reason: newArea.reason.trim() || null }]);
        setNewArea({ name: '', reason: '' });
    }

    return (
        <div className="max-w-xl mx-auto px-4 py-8">
            <button onClick={onBack} className="flex items-center gap-2 text-sm text-slate-500 hover:text-slate-900 mb-6 transition-colors">
                <ArrowLeft className="w-4 h-4" /> Back to search
            </button>

            <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-xl bg-orange-100 flex items-center justify-center">
                    <Shield className="w-5 h-5 text-orange-600" />
                </div>
                <div>
                    <h2 className="text-xl font-black text-slate-900">Safety Settings</h2>
                    <p className="text-xs text-slate-500">Your settings are private and respected by the platform.</p>
                </div>
            </div>

            <div className="space-y-4 mt-6">
                {/* Cutoff time */}
                <div className="bg-white rounded-2xl border border-slate-200 p-5">
                    <div className="flex items-center gap-2 mb-1">
                        <Clock className="w-4 h-4 text-orange-500" />
                        <span className="font-semibold text-sm text-slate-900">No deliveries after</span>
                    </div>
                    <p className="text-xs text-slate-500 mb-3">You won't receive delivery requests after this time.</p>
                    <input
                        type="time"
                        value={cutoff}
                        onChange={(e) => setCutoff(e.target.value)}
                        className="px-3 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-orange-400"
                    />
                </div>

                {/* Blocked areas */}
                <div className="bg-white rounded-2xl border border-slate-200 p-5">
                    <div className="flex items-center gap-2 mb-1">
                        <MapPin className="w-4 h-4 text-orange-500" />
                        <span className="font-semibold text-sm text-slate-900">Areas to avoid</span>
                    </div>
                    <p className="text-xs text-slate-500 mb-3">Add areas you're not comfortable delivering to. No reason needed.</p>

                    <div className="space-y-2 mb-3">
                        {areas.map((a, i) => (
                            <div key={i} className="flex items-center justify-between bg-slate-50 rounded-xl px-3 py-2">
                                <div>
                                    <span className="text-sm font-medium text-slate-800">{a.name}</span>
                                    {a.reason && <span className="text-xs text-slate-500 ml-2">— {a.reason}</span>}
                                </div>
                                <button onClick={() => setAreas(areas.filter((_, idx) => idx !== i))} className="p-1 hover:bg-slate-200 rounded-lg">
                                    <X className="w-3.5 h-3.5 text-slate-500" />
                                </button>
                            </div>
                        ))}
                    </div>

                    <div className="flex gap-2 flex-wrap">
                        <input
                            className="flex-1 min-w-32 px-3 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-orange-400"
                            placeholder="Area name"
                            value={newArea.name}
                            onChange={(e) => setNewArea({ ...newArea, name: e.target.value })}
                            onKeyDown={(e) => e.key === 'Enter' && addArea()}
                        />
                        <input
                            className="flex-1 min-w-32 px-3 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-orange-400"
                            placeholder="Reason (optional)"
                            value={newArea.reason}
                            onChange={(e) => setNewArea({ ...newArea, reason: e.target.value })}
                            onKeyDown={(e) => e.key === 'Enter' && addArea()}
                        />
                        <button onClick={addArea} className="px-3 py-2 rounded-xl bg-orange-500 text-white text-sm font-semibold hover:bg-orange-600 transition-colors flex items-center gap-1">
                            <Plus className="w-3.5 h-3.5" /> Add
                        </button>
                    </div>
                </div>

                {error && <p className="text-xs text-rose-600">{error}</p>}
                {saved && <p className="text-xs text-emerald-600 font-medium">Settings saved successfully.</p>}

                <button
                    onClick={handleSave}
                    disabled={saving}
                    className="w-full py-3 rounded-2xl bg-orange-500 text-white font-bold text-sm hover:bg-orange-600 transition-colors disabled:opacity-60"
                >
                    {saving ? 'Saving...' : 'Save settings'}
                </button>
            </div>
        </div>
    );
}