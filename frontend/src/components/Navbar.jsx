import React, { useState, useEffect, useRef } from 'react';
import { Utensils, MapPin, Table, LayoutGrid, Bell, LogOut, User, Shield } from 'lucide-react';
import { getNotifications, markNotificationRead, markAllRead, seedNotifications } from '../api';

export default function Navbar({ viewMode, setViewMode, user, onLogout, onLoginClick, onRegisterClick, onPartnerClick }) {
  const [notifs, setNotifs] = useState([]);
  const [bellOpen, setBellOpen] = useState(false);
  const bellRef = useRef();

  useEffect(() => {
    if (user) {
      getNotifications().then((r) => setNotifs(r.items)).catch(() => { });
    } else {
      setNotifs([]);
    }
  }, [user]);

  useEffect(() => {
    function handleClick(e) {
      if (bellRef.current && !bellRef.current.contains(e.target)) setBellOpen(false);
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const unread = notifs.filter((n) => !n.is_read).length;
  const typeIcon = { price_drop: '🏷️', best_time: '🕐', combo: '🍱', order_update: '👋' };

  function handleMarkAll() {
    markAllRead().then(() => setNotifs((p) => p.map((n) => ({ ...n, is_read: true }))));
  }

  function handleMarkOne(id) {
    markNotificationRead(id).then(() =>
      setNotifs((p) => p.map((n) => (n.id === id ? { ...n, is_read: true } : n)))
    );
  }

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-linear-to-tr from-orange-500 to-amber-500 flex items-center justify-center text-white shadow-md shadow-orange-500/20">
            <Utensils className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-2xl font-black tracking-tight text-slate-900">
                Price<span className="text-orange-500">Bite</span>
              </span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-orange-100 text-orange-700 uppercase tracking-wider">
                Live
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium -mt-0.5 hidden sm:block">
              Cross-Restaurant Price Comparison
            </p>
          </div>
        </div>

        {/* Location */}
        <div className="hidden md:flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-100 border border-slate-200 text-xs font-medium text-slate-700">
          <MapPin className="w-3.5 h-3.5 text-orange-500" />
          <span>Chennai, TN</span>
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-2">

          {/* View Toggle */}
          <div className="flex items-center gap-1 p-1 bg-slate-100 rounded-xl border border-slate-200">
            <button
              onClick={() => setViewMode('grid')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${viewMode === 'grid' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
                }`}
            >
              <LayoutGrid className="w-3.5 h-3.5" />
              <span>Cards</span>
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${viewMode === 'table' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
                }`}
            >
              <Table className="w-3.5 h-3.5" />
              <span>Compare Table</span>
            </button>
          </div>

          {/* Auth section */}
          {user ? (
            <div className="flex items-center gap-2">
              {/* Notification Bell */}
              <div ref={bellRef} className="relative">
                <button
                  onClick={() => setBellOpen((o) => !o)}
                  className="relative p-2 rounded-lg hover:bg-slate-100 transition-colors"
                >
                  <Bell className="w-4 h-4 text-slate-600" />
                  {unread > 0 && (
                    <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-rose-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                      {unread}
                    </span>
                  )}
                </button>

                {bellOpen && (
                  <div className="absolute right-0 top-10 w-80 bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden z-50">
                    <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100">
                      <span className="font-semibold text-sm text-slate-900">Notifications</span>
                      {unread > 0 && (
                        <button onClick={handleMarkAll} className="text-xs text-orange-600 font-medium hover:underline">
                          Mark all read
                        </button>
                      )}
                    </div>
                    <div className="max-h-80 overflow-y-auto">
                      {notifs.length === 0 ? (
                        <div className="p-6 text-center text-xs text-slate-400">
                          No notifications yet.{' '}
                          <button
                            onClick={() => seedNotifications().then(() => getNotifications().then((r) => setNotifs(r.items)))}
                            className="text-orange-500 hover:underline"
                          >
                            Load samples
                          </button>
                        </div>
                      ) : (
                        notifs.map((n) => (
                          <div
                            key={n.id}
                            onClick={() => !n.is_read && handleMarkOne(n.id)}
                            className={`flex gap-3 px-4 py-3 border-b border-slate-50 cursor-pointer hover:bg-slate-50 transition-colors ${!n.is_read ? 'bg-orange-50/40' : ''}`}
                          >
                            <span className="text-lg shrink-0">{typeIcon[n.type] || '📣'}</span>
                            <div className="flex-1 min-w-0">
                              <p className={`text-xs ${n.is_read ? 'font-normal text-slate-700' : 'font-semibold text-slate-900'}`}>{n.title}</p>
                              <p className="text-[11px] text-slate-500 mt-0.5 leading-relaxed">{n.body}</p>
                            </div>
                            {!n.is_read && <div className="w-2 h-2 rounded-full bg-orange-500 shrink-0 mt-1" />}
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Partner Safety */}
              {user.role === 'delivery_partner' && (
                <button
                  onClick={onPartnerClick}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-xs font-semibold text-slate-700 transition-colors"
                >
                  <Shield className="w-3.5 h-3.5 text-orange-500" />
                  Safety
                </button>
              )}

              {/* User name + logout */}
              <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-100 text-xs font-semibold text-slate-700">
                <User className="w-3.5 h-3.5 text-orange-500" />
                <span>{user.name.split(' ')[0]}</span>
              </div>
              <button
                onClick={onLogout}
                className="p-2 rounded-lg hover:bg-slate-100 transition-colors"
                title="Logout"
              >
                <LogOut className="w-4 h-4 text-slate-500" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <button
                onClick={onLoginClick}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-100 transition-colors"
              >
                Login
              </button>
              <button
                onClick={onRegisterClick}
                className="px-3 py-1.5 rounded-lg bg-orange-500 text-white text-xs font-semibold hover:bg-orange-600 transition-colors"
              >
                Sign up
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}