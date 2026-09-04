import React from "react";
import { Merchant } from "../lib/types";

interface HeaderProps {
  title?: string;
  subtitle?: string;
  merchants: Merchant[];
  selectedMerchantId: number;
  onSelectMerchant: (id: number) => void;
  onRefresh: () => void;
  isRefreshing: boolean;
  onToggleMobileMenu: () => void;
}

export function Header({
  title = "Revenue Intelligence",
  subtitle = "AI-powered opportunities to grow merchant revenue.",
  merchants,
  selectedMerchantId,
  onSelectMerchant,
  onRefresh,
  isRefreshing,
  onToggleMobileMenu,
}: HeaderProps) {
  const currentMerchant = merchants.find((m) => m.id === selectedMerchantId);

  return (
    <header className="sticky top-0 z-20 bg-white/95 backdrop-blur-xs border-b border-slate-200 px-6 py-4 shadow-2xs">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Title & Mobile Toggle */}
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleMobileMenu}
            className="lg:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-slate-900 cursor-pointer"
            aria-label="Open Navigation"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-900">{title}</h1>
            <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>
          </div>
        </div>

        {/* Right Side: Merchant Selector, Refresh, Status Badge */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Status Indicator */}
          <div className="hidden sm:inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-800">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>AI Agent Active</span>
          </div>

          {/* Merchant Selector Dropdown */}
          <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 focus-within:border-slate-400 transition-colors">
            <div className="w-2 h-2 rounded-full bg-indigo-600"></div>
            <span className="text-xs font-medium text-slate-500">Merchant:</span>
            <select
              value={selectedMerchantId}
              onChange={(e) => onSelectMerchant(Number(e.target.value))}
              className="bg-transparent text-xs font-bold text-slate-900 focus:outline-none cursor-pointer pr-2"
            >
              {merchants.length > 0 ? (
                merchants.map((m) => (
                  <option key={m.id} value={m.id}>
                    #{m.id} {m.name} ({m.category})
                  </option>
                ))
              ) : (
                <option value={10}>#10 Lumen Jewels (Jewelry)</option>
              )}
            </select>
          </div>

          {/* Refresh Button */}
          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-white text-xs font-semibold text-slate-700 hover:bg-slate-50 hover:text-slate-900 active:scale-98 disabled:opacity-50 transition-all shadow-2xs cursor-pointer"
            title="Refresh live metrics from backend"
          >
            <svg
              className={`w-3.5 h-3.5 text-slate-500 ${isRefreshing ? "animate-spin" : ""}`}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            <span className="hidden sm:inline">Refresh</span>
          </button>
        </div>
      </div>
    </header>
  );
}
