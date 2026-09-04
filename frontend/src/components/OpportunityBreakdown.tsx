import React from "react";
import { formatCompactINR, formatINR, formatOpportunityType } from "../lib/formatters";

interface OpportunityBreakdownProps {
  breakdown: Record<string, number | string>;
  totalOpportunity: number | string;
}

const CATEGORY_CONFIG: Record<
  string,
  { label: string; color: string; bg: string; dot: string; desc: string }
> = {
  ABANDONED_CART_RECOVERY: {
    label: "Abandoned Cart Recovery",
    color: "bg-indigo-600",
    bg: "bg-indigo-50",
    dot: "bg-indigo-500",
    desc: "Recover high-intent checkouts with targeted bounded incentives",
  },
  CROSS_SELL: {
    label: "Cross-Sell Opportunities",
    color: "bg-emerald-600",
    bg: "bg-emerald-50",
    dot: "bg-emerald-500",
    desc: "Relevant product recommendations based on customer buying patterns",
  },
  FAILED_PAYMENT_RECOVERY: {
    label: "Failed Payment Recovery",
    color: "bg-amber-600",
    bg: "bg-amber-50",
    dot: "bg-amber-500",
    desc: "Recoverable gateway timeouts and transaction errors",
  },
  DORMANT_CUSTOMER_REACTIVATION: {
    label: "Dormant Reactivation",
    color: "bg-cyan-600",
    bg: "bg-cyan-50",
    dot: "bg-cyan-500",
    desc: "ML-scored re-engagement nudges for high-LTV inactive shoppers",
  },
};

export function OpportunityBreakdown({
  breakdown,
  totalOpportunity,
}: OpportunityBreakdownProps) {
  const total =
    typeof totalOpportunity === "string"
      ? parseFloat(totalOpportunity)
      : totalOpportunity || 0;

  const entries = Object.entries(breakdown).map(([key, val]) => {
    const numericVal = typeof val === "string" ? parseFloat(val) : val;
    const percentage = total > 0 ? (numericVal / total) * 100 : 0;
    return {
      key,
      value: numericVal,
      percentage: Math.round(percentage * 10) / 10,
      config: CATEGORY_CONFIG[key] || {
        label: formatOpportunityType(key),
        color: "bg-slate-600",
        bg: "bg-slate-50",
        dot: "bg-slate-500",
        desc: "Revenue opportunity",
      },
    };
  });

  // Sort descending by value
  entries.sort((a, b) => b.value - a.value);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-2">
        <div>
          <h3 className="text-base font-bold text-slate-900">
            Revenue Opportunity Breakdown
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Distribution of identified merchant expansion value across core drivers
          </p>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-xs text-slate-500">Total Unlocked Potential:</span>
          <span className="text-lg font-bold text-emerald-600">
            {formatCompactINR(total)}
          </span>
        </div>
      </div>

      {/* Multi-segmented Horizontal Progress Bar */}
      <div className="mt-5">
        <div className="h-3.5 w-full rounded-full bg-slate-100 overflow-hidden flex shadow-inner">
          {entries.map((item) => (
            <div
              key={item.key}
              style={{ width: `${Math.max(item.percentage, 2)}%` }}
              className={`${item.config.color} transition-all duration-500 first:rounded-l-full last:rounded-r-full relative group cursor-pointer`}
              title={`${item.config.label}: ${formatINR(item.value)} (${item.percentage}%)`}
            />
          ))}
        </div>
      </div>

      {/* Breakdown Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
        {entries.map((item) => (
          <div
            key={item.key}
            className="p-4 rounded-lg border border-slate-100 bg-slate-50/50 hover:bg-slate-50 transition-colors"
          >
            <div className="flex items-center gap-2 mb-2">
              <span className={`w-2.5 h-2.5 rounded-full ${item.config.dot}`}></span>
              <span className="text-xs font-semibold text-slate-800 line-clamp-1">
                {item.config.label}
              </span>
            </div>

            <div className="flex items-baseline justify-between mt-1">
              <span className="text-lg font-bold text-slate-900">
                {formatCompactINR(item.value)}
              </span>
              <span className="text-xs font-semibold text-slate-500">
                {item.percentage}%
              </span>
            </div>

            <div className="mt-2 text-[11px] text-slate-500 leading-snug">
              {item.config.desc}
            </div>

            <div className="w-full bg-slate-200 h-1.5 rounded-full mt-3 overflow-hidden">
              <div
                className={`h-full ${item.config.color} rounded-full`}
                style={{ width: `${item.percentage}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
