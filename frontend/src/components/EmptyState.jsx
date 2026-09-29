import React from 'react';
import { SearchX, RotateCcw } from 'lucide-react';

export default function EmptyState({ searchTerm, onReset }) {
  return (
    <div className="text-center py-16 px-4 bg-white rounded-3xl border border-dashed border-slate-200 max-w-xl mx-auto my-8">
      <div className="w-16 h-16 rounded-2xl bg-orange-50 border border-orange-100 text-orange-500 flex items-center justify-center mx-auto mb-4">
        <SearchX className="w-8 h-8 stroke-[1.8]" />
      </div>
      <h3 className="text-lg font-bold text-slate-900 mb-1">
        No matching dishes found
      </h3>
      <p className="text-xs text-slate-500 max-w-md mx-auto mb-6">
        {searchTerm
          ? `We couldn't find any dishes matching "${searchTerm}". Try checking your spelling or searching for popular dishes like Biryani, Lassi, or Dosa.`
          : 'No dishes match the selected dietary filters. Try loosening your filter criteria.'}
      </p>
      {onReset && (
        <button
          onClick={onReset}
          className="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 hover:bg-orange-500 text-white rounded-xl text-xs font-bold transition-all shadow-xs cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset Search & Filters</span>
        </button>
      )}
    </div>
  );
}
