import React from 'react';

export default function SkeletonLoader({ count = 6 }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs animate-pulse flex flex-col justify-between"
        >
          <div>
            {/* Image Placeholder */}
            <div className="h-44 bg-slate-200 w-full" />

            {/* Content Placeholder */}
            <div className="p-4 space-y-3">
              <div className="h-4 bg-slate-200 rounded-md w-3/4" />
              <div className="h-3 bg-slate-100 rounded-md w-1/2" />
              <div className="pt-2 border-t border-slate-100 space-y-2">
                <div className="h-3 bg-slate-100 rounded-md w-full" />
                <div className="h-3 bg-slate-100 rounded-md w-4/5" />
              </div>
            </div>
          </div>

          {/* Footer Placeholder */}
          <div className="p-4 pt-0">
            <div className="h-12 bg-slate-100 rounded-xl w-full" />
          </div>
        </div>
      ))}
    </div>
  );
}
