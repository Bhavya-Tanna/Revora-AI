import React from "react";

interface KpiCardProps {
  title: string;
  value: string;
  subtitle?: string;
  badgeText?: string;
  badgeVariant?: "emerald" | "amber" | "indigo" | "slate";
  icon: React.ReactNode;
}

export function KpiCard({
  title,
  value,
  subtitle,
  badgeText,
  badgeVariant = "slate",
  icon,
}: KpiCardProps) {
  const badgeStyles = {
    emerald: "bg-emerald-50 text-emerald-700 border-emerald-200",
    amber: "bg-amber-50 text-amber-700 border-amber-200",
    indigo: "bg-indigo-50 text-indigo-700 border-indigo-200",
    slate: "bg-slate-100 text-slate-700 border-slate-200",
  }[badgeVariant];

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:border-slate-300 transition-all">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
          {title}
        </span>
        <div className="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600">
          {icon}
        </div>
      </div>

      <div className="flex items-baseline justify-between gap-2">
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">{value}</h2>
        {badgeText && (
          <span
            className={`text-xs px-2 py-0.5 rounded-full font-medium border ${badgeStyles}`}
          >
            {badgeText}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="mt-2 text-xs text-slate-500 flex items-center gap-1.5">
          {subtitle}
        </p>
      )}
    </div>
  );
}
