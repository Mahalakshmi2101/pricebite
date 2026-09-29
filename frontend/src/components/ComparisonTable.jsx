import React from 'react';
import { Star, Bike, Check, Trophy, ArrowUpDown } from 'lucide-react';

export default function ComparisonTable({ items, selectedSort, onSelectSort }) {
  if (!items || items.length === 0) return null;

  // Find the lowest total cost item to badge as "Best Deal"
  const minCost = Math.min(...items.map((i) => i.total_cost));

  return (
    <div className="w-full bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
      <div className="p-4 sm:p-5 bg-slate-900 text-white flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <Trophy className="w-5 h-5 text-amber-400" />
            <h3 className="font-bold text-base sm:text-lg">
              Live Restaurant Comparison Matrix
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Comparing {items.length} restaurant offerings with all hidden fees (delivery + GST) calculated upfront.
          </p>
        </div>

        <div className="text-xs font-semibold px-3 py-1 rounded-full bg-amber-400/20 text-amber-300 border border-amber-400/30">
          Cheapest from ₹{minCost.toFixed(2)}
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-600">
          <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 font-bold uppercase tracking-wider text-[11px]">
            <tr>
              <th className="py-3.5 px-4">Restaurant</th>
              <th className="py-3.5 px-3">Portion</th>
              <th className="py-3.5 px-3">Ratings</th>
              <th className="py-3.5 px-3">Base Price</th>
              <th className="py-3.5 px-3">Discount</th>
              <th className="py-3.5 px-3">Delivery</th>
              <th className="py-3.5 px-3">GST (5%)</th>
              <th
                onClick={() => onSelectSort(selectedSort === 'total_cost' ? '-total_cost' : 'total_cost')}
                className="py-3.5 px-4 text-orange-600 bg-orange-50/50 cursor-pointer hover:bg-orange-100/50 transition-colors"
              >
                <div className="flex items-center gap-1">
                  <span>Total Cost</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th className="py-3.5 px-4 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {items.map((item, idx) => {
              const isBestDeal = item.total_cost === minCost;
              return (
                <tr
                  key={`${item.restaurant_id}-${item.dish_id}-${idx}`}
                  className={`hover:bg-slate-50/80 transition-colors ${
                    isBestDeal ? 'bg-amber-50/30 font-medium' : ''
                  }`}
                >
                  {/* Restaurant Name & Area */}
                  <td className="py-3.5 px-4 font-semibold text-slate-900">
                    <div className="flex items-center gap-2">
                      {isBestDeal && (
                        <span className="p-1 rounded-full bg-amber-500 text-white" title="Best Price Deal">
                          <Check className="w-3 h-3 stroke-[3]" />
                        </span>
                      )}
                      <div>
                        <div className="text-sm font-bold">{item.restaurant_name}</div>
                        <div className="text-[11px] text-slate-400 font-normal">{item.restaurant_area}</div>
                      </div>
                    </div>
                  </td>

                  {/* Portion */}
                  <td className="py-3.5 px-3 text-slate-600 font-medium">
                    {item.portion_size}
                  </td>

                  {/* Ratings */}
                  <td className="py-3.5 px-3">
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center gap-0.5 text-emerald-700 font-bold">
                        <Star className="w-3 h-3 fill-emerald-600 text-emerald-600" />
                        {item.food_rating.toFixed(1)}
                      </span>
                      <span className="inline-flex items-center gap-0.5 text-blue-700 font-bold">
                        <Bike className="w-3 h-3 text-blue-600" />
                        {item.delivery_rating.toFixed(1)}
                      </span>
                    </div>
                  </td>

                  {/* Base Price */}
                  <td className="py-3.5 px-3 text-slate-700">
                    ₹{item.price.toFixed(2)}
                  </td>

                  {/* Discount */}
                  <td className="py-3.5 px-3">
                    {item.discount_percent > 0 ? (
                      <span className="px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                        {item.discount_percent}% OFF
                      </span>
                    ) : (
                      <span className="text-slate-400">—</span>
                    )}
                  </td>

                  {/* Delivery Fee */}
                  <td className="py-3.5 px-3 text-slate-600">
                    ₹{item.delivery_fee.toFixed(2)}
                  </td>

                  {/* GST */}
                  <td className="py-3.5 px-3 text-slate-500">
                    ₹{item.tax.toFixed(2)}
                  </td>

                  {/* Total Cost */}
                  <td className="py-3.5 px-4 bg-orange-50/30">
                    <div className="flex flex-col">
                      <span className="text-sm font-black text-slate-950">
                        ₹{item.total_cost.toFixed(2)}
                      </span>
                      {isBestDeal && (
                        <span className="text-[10px] text-amber-600 font-bold uppercase tracking-wider">
                          Best Deal
                        </span>
                      )}
                    </div>
                  </td>

                  {/* Action */}
                  <td className="py-3.5 px-4 text-center">
                    <button className="px-3 py-1.5 bg-slate-900 hover:bg-orange-500 text-white rounded-lg text-xs font-bold transition-all cursor-pointer">
                      Order
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
