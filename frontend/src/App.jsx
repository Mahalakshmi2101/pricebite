import React, { useState, useEffect, useCallback } from 'react';
import Navbar from './components/Navbar';
import SearchBar from './components/SearchBar';
import FilterChips from './components/FilterChips';
import DishCard from './components/DishCard';
import ComparisonTable from './components/ComparisonTable';
import SkeletonLoader from './components/SkeletonLoader';
import EmptyState from './components/EmptyState';
import AuthModal from './components/AuthModal';
import PartnerPage from './components/PartnerPage';
import { searchDishes, getMe } from './api';
import { Sparkles, AlertCircle, RefreshCw } from 'lucide-react';

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDiet, setSelectedDiet] = useState('');
  const [selectedSort, setSelectedSort] = useState('total_cost');
  const [viewMode, setViewMode] = useState('grid');
  const [items, setItems] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Auth state
  const [user, setUser] = useState(null);
  const [authModal, setAuthModal] = useState(null); // 'login' | 'register' | null
  const [showPartner, setShowPartner] = useState(false);

  // Load user from token on mount
  useEffect(() => {
    const token = localStorage.getItem('pb_token');
    if (token) {
      getMe().then(setUser).catch(() => {
        localStorage.removeItem('pb_token');
      });
    }
  }, []);

  function handleLoginSuccess(token, userData) {
    localStorage.setItem('pb_token', token);
    setUser(userData);
    setAuthModal(null);
  }

  function handleLogout() {
    localStorage.removeItem('pb_token');
    setUser(null);
    setShowPartner(false);
  }

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = { limit: 50, sort: selectedSort };
      if (searchTerm.trim()) params.q = searchTerm.trim();
      if (selectedDiet) params.diet = selectedDiet;
      const data = await searchDishes(params);
      setItems(data.items || []);
      setTotalCount(data.total || 0);
    } catch (err) {
      console.error('API Error:', err);
      setError(
  err.response?.data?.detail ||
  'Failed to connect to PriceBite backend. Please try again.'
);
    } finally {
      setLoading(false);
    }
  }, [searchTerm, selectedDiet, selectedSort]);

  useEffect(() => {
    const timer = setTimeout(() => { fetchData(); }, 250);
    return () => clearTimeout(timer);
  }, [fetchData]);

  const handleReset = () => {
    setSearchTerm('');
    setSelectedDiet('');
    setSelectedSort('total_cost');
  };

  // Show partner page
  if (showPartner && user?.role === 'delivery_partner') {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
        <Navbar
          viewMode={viewMode} setViewMode={setViewMode}
          user={user} onLogout={handleLogout}
          onLoginClick={() => setAuthModal('login')}
          onRegisterClick={() => setAuthModal('register')}
          onPartnerClick={() => setShowPartner(true)}
        />
        <PartnerPage user={user} onBack={() => setShowPartner(false)} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar
        viewMode={viewMode} setViewMode={setViewMode}
        user={user} onLogout={handleLogout}
        onLoginClick={() => setAuthModal('login')}
        onRegisterClick={() => setAuthModal('register')}
        onPartnerClick={() => setShowPartner(true)}
      />

      {/* Auth Modal */}
      {authModal && (
        <AuthModal
          mode={authModal}
          onClose={() => setAuthModal(null)}
          onSuccess={handleLoginSuccess}
          switchMode={(m) => setAuthModal(m)}
        />
      )}

      {/* Hero */}
      <section className="relative bg-linear-to-b from-orange-50/60 via-amber-50/30 to-slate-50 border-b border-slate-200/60 pt-10 pb-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-orange-100 text-orange-800 text-xs font-bold tracking-wide">
            <Sparkles className="w-3.5 h-3.5 text-orange-600" />
            <span>Never Overpay for the Same Dish Again</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-black text-slate-950 tracking-tight leading-tight">
            Compare Food Prices Across <br className="hidden sm:inline" />
            <span className="bg-linear-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent">
              Chennai's Top Restaurants
            </span>
          </h1>
          <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto font-normal">
            Real prices calculated with <strong>restaurant discounts</strong>, <strong>delivery fees</strong>, and <strong>flat 5% GST</strong> so you see the true all-inclusive cost upfront.
          </p>
          <div className="pt-2">
            <SearchBar value={searchTerm} onChange={setSearchTerm} onClear={() => setSearchTerm('')} />
          </div>
          <div className="flex flex-wrap items-center justify-center gap-2 pt-1 text-xs text-slate-500">
            <span className="font-semibold text-slate-400">Popular:</span>
            {['Biryani', 'Lassi', 'Gulab Jamun', 'Masala Dosa', 'Keto', 'Paneer'].map((tag) => (
              <button
                key={tag}
                onClick={() => setSearchTerm(tag)}
                className="px-2.5 py-1 rounded-lg bg-white border border-slate-200 hover:border-orange-300 hover:text-orange-600 transition-colors font-medium cursor-pointer"
              >
                {tag}
              </button>
            ))}
          </div>
        </div>
      </section>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <div className="bg-white p-3 sm:p-4 rounded-2xl border border-slate-200 shadow-xs">
          <FilterChips selectedDiet={selectedDiet} onSelectDiet={setSelectedDiet} selectedSort={selectedSort} onSelectSort={setSelectedSort} />
        </div>
        <div className="flex items-center justify-between text-xs text-slate-500 px-1">
          <div>Showing <strong className="text-slate-900">{items.length}</strong> of <strong className="text-slate-900">{totalCount}</strong> available offerings</div>
          {searchTerm && <div className="text-orange-600 font-medium">Filtered by: "{searchTerm}"</div>}
        </div>
        {error && (
          <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 flex items-center justify-between gap-3 text-xs sm:text-sm">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-rose-600 shrink-0" />
              <span>{error}</span>
            </div>
            <button onClick={fetchData} className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-rose-600 text-white rounded-lg text-xs font-bold hover:bg-rose-700 transition-colors cursor-pointer">
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </div>
        )}
        {loading && <SkeletonLoader count={6} />}
        {!loading && !error && items.length === 0 && <EmptyState searchTerm={searchTerm} onReset={handleReset} />}
        {!loading && !error && items.length > 0 && viewMode === 'grid' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {items.map((item, idx) => (
              <DishCard key={`${item.restaurant_id}-${item.dish_id}-${idx}`} item={item} />
            ))}
          </div>
        )}
        {!loading && !error && items.length > 0 && viewMode === 'table' && (
          <ComparisonTable items={items} selectedSort={selectedSort} onSelectSort={setSelectedSort} />
        )}
      </main>

      <footer className="mt-auto border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500 space-y-1">
        <p className="font-semibold text-slate-700">PriceBite — Placement Portfolio Project</p>
        <p>Built with FastAPI, SQLAlchemy 2.0, MySQL, React, Tailwind CSS, & Axios</p>
      </footer>
    </div>
  );
}