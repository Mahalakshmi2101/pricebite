import React from 'react';
import { Star, Bike, Tag, Flame, ShieldAlert } from 'lucide-react';

export default function DishCard({ item }) {
  const {
    dish_name,
    dish_image_url,
    category,
    diet_type,
    calories,
    protein_g,
    restaurant_name,
    restaurant_area,
    food_rating,
    delivery_rating,
    price,
    portion_size,
    discount_percent,
    final_price,
    delivery_fee,
    tax,
    total_cost,
  } = item;

  const dietBadgeColor = {
    veg: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    'non-veg': 'bg-rose-50 text-rose-700 border-rose-200',
    keto: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    'diabetic-friendly': 'bg-teal-50 text-teal-700 border-teal-200',
  }[diet_type] || 'bg-slate-50 text-slate-700 border-slate-200';

  return (
    <div className="group bg-white rounded-2xl border border-slate-200/80 overflow-hidden shadow-xs hover:shadow-xl hover:border-slate-300 hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between">
      <div>
        {/* Image & Badges */}
        <div className="relative h-44 w-full bg-slate-100 overflow-hidden">
          <img
            src={dish_image_url || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600'}
            alt={dish_name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
          />
          <div className="absolute inset-0 bg-linear-to-t from-black/60 via-transparent to-transparent"></div>

          {/* Active Discount Badge */}
          {discount_percent > 0 && (
            <div className="absolute top-3 left-3 flex items-center gap-1 px-2.5 py-1 bg-linear-to-r from-orange-500 to-amber-500 text-white rounded-lg text-xs font-black shadow-md">
              <Tag className="w-3 h-3 fill-current" />
              <span>{discount_percent}% OFF</span>
            </div>
          )}

          {/* Diet Pill */}
          <div className={`absolute top-3 right-3 px-2 py-0.5 rounded-md text-[10px] font-bold border uppercase tracking-wider bg-white/95 backdrop-blur-xs ${dietBadgeColor}`}>
            {diet_type}
          </div>

          {/* Dish Title Overlay */}
          <div className="absolute bottom-2.5 left-3 right-3 text-white">
            <h3 className="font-bold text-base line-clamp-1 leading-snug drop-shadow-xs">
              {dish_name}
            </h3>
            <p className="text-[11px] text-slate-200 font-medium">
              {category} • {portion_size}
            </p>
          </div>
        </div>

        {/* Restaurant Details & Dual Ratings */}
        <div className="p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
            <div>
              <h4 className="font-bold text-slate-900 text-sm line-clamp-1">
                {restaurant_name}
              </h4>
              <p className="text-xs text-slate-500">{restaurant_area}</p>
            </div>

            {/* Ratings: Food vs Delivery shown separately */}
            <div className="flex items-center gap-1.5">
              <div className="flex items-center gap-0.5 px-2 py-1 bg-emerald-50 rounded-lg border border-emerald-100 text-emerald-700 text-xs font-bold" title="Food Taste Rating">
                <Star className="w-3 h-3 fill-emerald-600 text-emerald-600" />
                <span>{food_rating.toFixed(1)}</span>
              </div>
              <div className="flex items-center gap-0.5 px-2 py-1 bg-blue-50 rounded-lg border border-blue-100 text-blue-700 text-xs font-bold" title="Delivery Speed Rating">
                <Bike className="w-3 h-3 text-blue-600" />
                <span>{delivery_rating.toFixed(1)}</span>
              </div>
            </div>
          </div>

          {/* Nutrition info if available */}
          {(calories || protein_g) && (
            <div className="flex items-center gap-3 text-[11px] text-slate-500 bg-slate-50 px-2.5 py-1.5 rounded-lg border border-slate-100">
              {calories && (
                <span className="flex items-center gap-1">
                  <Flame className="w-3 h-3 text-amber-500" />
                  <span>{calories} kcal</span>
                </span>
              )}
              {protein_g && (
                <span>Protein: <strong className="text-slate-700">{protein_g}g</strong></span>
              )}
            </div>
          )}

          {/* Cost Breakdown Accordion/Grid */}
          <div className="text-xs space-y-1 text-slate-600">
            <div className="flex justify-between items-center">
              <span>Base Item Price:</span>
              <div className="flex items-center gap-1.5">
                {discount_percent > 0 && (
                  <span className="line-through text-slate-400">₹{price.toFixed(0)}</span>
                )}
                <span className="font-semibold text-slate-900">₹{final_price.toFixed(2)}</span>
              </div>
            </div>
            <div className="flex justify-between items-center text-[11px] text-slate-500">
              <span>Delivery Fee:</span>
              <span>₹{delivery_fee.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center text-[11px] text-slate-500">
              <span>GST (5%):</span>
              <span>₹{tax.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer with Total Cost */}
      <div className="p-4 pt-0">
        <div className="bg-orange-50/70 border border-orange-100 rounded-xl p-2.5 flex items-center justify-between">
          <div>
            <span className="text-[10px] font-bold text-orange-700 uppercase tracking-wider block">
              All-Inclusive Total
            </span>
            <span className="text-lg font-black text-slate-950">
              ₹{total_cost.toFixed(2)}
            </span>
          </div>
          <button className="px-3.5 py-1.5 bg-orange-500 hover:bg-orange-600 text-white rounded-lg text-xs font-bold shadow-xs hover:shadow-md transition-all cursor-pointer">
            Select
          </button>
        </div>
      </div>
    </div>
  );
}
