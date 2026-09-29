import React from 'react';
import { Sparkles, ArrowUpDown } from 'lucide-react';

const DIET_OPTIONS = [
  { id: '', label: 'All Items' },
  { id: 'veg', label: '🌱 Pure Veg' },
  { id: 'non-veg', label: '🍗 Non-Veg' },
  { id: 'keto', label: '🥑 Keto' },
  { id: 'diabetic-friendly', label: '🩺 Diabetic-Friendly' },
];

const SORT_OPTIONS = [
  { id: 'total_cost', label: 'Total Cost: Low to High' },
  { id: '-total_cost', label: 'Total Cost: High to Low' },
  { id: 'price', label: 'Base Price: Low to High' },
  { id: '-food_rating', label: 'Highest Food Rating' },
];

export default function FilterChips({
  selectedDiet,
  onSelectDiet,
  selectedSort,
  onSelectSort,
}) {
  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 py-2">
      {/* Diet Chips */}
      <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0 scrollbar-none">
        {DIET_OPTIONS.map((diet) => {
          const isActive = selectedDiet === diet.id;
          return (
            <button
              key={diet.id}
              onClick={() => onSelectDiet(diet.id)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all duration-200 cursor-pointer ${
                isActive
                  ? 'bg-slate-900 text-white shadow-xs scale-102'
                  : 'bg-white text-slate-600 border border-slate-200 hover:border-slate-300 hover:bg-slate-50'
              }`}
            >
              {diet.label}
            </button>
          );
        })}
      </div>

      {/* Sort Dropdown */}
      <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
        <div className="relative inline-flex items-center">
          <ArrowUpDown className="w-3.5 h-3.5 text-slate-400 absolute left-3 pointer-events-none" />
          <select
            value={selectedSort}
            onChange={(e) => onSelectSort(e.target.value)}
            className="pl-8 pr-8 py-1.5 bg-white border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 outline-hidden hover:border-slate-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-500/10 cursor-pointer appearance-none"
          >
            {SORT_OPTIONS.map((opt) => (
              <option key={opt.id} value={opt.id}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}
