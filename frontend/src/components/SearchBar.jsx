import React from 'react';
import { Search, X } from 'lucide-react';

export default function SearchBar({ value, onChange, onClear, placeholder = "Search for Biryani, Lassi, Gulab Jamun, Dosa..." }) {
  return (
    <div className="relative w-full max-w-2xl mx-auto">
      <div className="relative flex items-center shadow-lg shadow-orange-500/5 rounded-2xl bg-white border border-slate-200 focus-within:border-orange-500 focus-within:ring-4 focus-within:ring-orange-500/15 transition-all">
        <div className="pl-4 pr-2 text-slate-400">
          <Search className="w-5 h-5 text-orange-500" />
        </div>
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full py-4 pr-12 text-base text-slate-800 placeholder-slate-400 bg-transparent rounded-2xl outline-hidden font-medium"
        />
        {value && (
          <button
            onClick={onClear}
            className="absolute right-3.5 p-1.5 rounded-full hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
            title="Clear search"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
}
