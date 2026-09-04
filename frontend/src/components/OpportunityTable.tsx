import React, { useState } from "react";
import { RevenueOpportunity } from "../lib/types";
import {
  formatActionName,
  formatINR,
  formatOpportunityType,
  formatPercent,
} from "../lib/formatters";

interface OpportunityTableProps {
  opportunities: RevenueOpportunity[];
  onAnalyzeSpecific?: (opportunity: RevenueOpportunity) => void;
}

export function OpportunityTable({
  opportunities,
  onAnalyzeSpecific,
}: OpportunityTableProps) {
  const [filterPriority, setFilterPriority] = useState<string>("ALL");
  const [filterType, setFilterType] = useState<string>("ALL");

  const filtered = opportunities.filter((item) => {
    if (filterPriority !== "ALL" && item.priority !== filterPriority) {
      return false;
    }
    if (filterType !== "ALL" && item.opportunity_type !== filterType) {
      return false;
    }
    return true;
  });

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case "HIGH":
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
            HIGH
          </span>
        );
      case "MEDIUM":
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            MEDIUM
          </span>
        );
      case "LOW":
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
            LOW
          </span>
        );
    }
  };

  const getActionBadge = (action: string) => {
    const isFinancial =
      action.includes("PAYMENT") || action.includes("CART") || action.includes("OFFER");
    return (
      <span
        className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium font-mono border ${
          isFinancial
            ? "bg-slate-900 text-white border-slate-900"
            : "bg-slate-100 text-slate-800 border-slate-200"
        }`}
      >
        {action}
      </span>
    );
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Table Header & Controls */}
      <div className="p-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-base font-bold text-slate-900">
            Top Revenue Opportunities
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Ranked by expected recovery value and machine learning confidence
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <div className="flex items-center bg-slate-100 p-1 rounded-lg">
            {["ALL", "HIGH", "MEDIUM", "LOW"].map((p) => (
              <button
                key={p}
                onClick={() => setFilterPriority(p)}
                className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                  filterPriority === p
                    ? "bg-white text-slate-900 shadow-xs"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                {p}
              </button>
            ))}
          </div>

          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white text-slate-700 text-xs focus:outline-none focus:ring-1 focus:ring-slate-900"
          >
            <option value="ALL">All Categories</option>
            <option value="ABANDONED_CART_RECOVERY">Abandoned Cart</option>
            <option value="CROSS_SELL">Cross-Sell</option>
            <option value="FAILED_PAYMENT_RECOVERY">Failed Payment</option>
            <option value="DORMANT_CUSTOMER_REACTIVATION">Dormant Reactivation</option>
          </select>
        </div>
      </div>

      {/* Desktop & Tablet Table */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/75 border-b border-slate-200 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              <th className="py-3 px-5">Opportunity & Context</th>
              <th className="py-3 px-4">Customer</th>
              <th className="py-3 px-4 text-right">Est. Revenue</th>
              <th className="py-3 px-4">Confidence</th>
              <th className="py-3 px-4">Priority</th>
              <th className="py-3 px-5">Recommended Bounded Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-12 text-center text-slate-500 text-sm">
                  No opportunities match the selected filters.
                </td>
              </tr>
            ) : (
              filtered.map((item, idx) => (
                <tr
                  key={`${item.source_id}-${idx}`}
                  className="hover:bg-slate-50/50 transition-colors"
                >
                  <td className="py-3.5 px-5">
                    <div className="font-semibold text-slate-900">{item.title}</div>
                    <div className="text-xs text-slate-500 mt-0.5 line-clamp-1">
                      {item.description}
                    </div>
                  </td>

                  <td className="py-3.5 px-4 whitespace-nowrap">
                    <div className="flex items-center gap-1.5">
                      <span className="w-6 h-6 rounded-full bg-slate-100 text-slate-600 font-mono text-xs flex items-center justify-center font-bold">
                        C
                      </span>
                      <span className="text-xs font-mono text-slate-700">
                        #{item.customer_id ?? "N/A"}
                      </span>
                    </div>
                  </td>

                  <td className="py-3.5 px-4 text-right whitespace-nowrap">
                    <div className="font-bold text-slate-900">
                      {formatINR(item.estimated_revenue)}
                    </div>
                  </td>

                  <td className="py-3.5 px-4 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <div className="w-16 bg-slate-100 h-2 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-emerald-500 rounded-full"
                          style={{ width: `${Math.round(item.confidence * 100)}%` }}
                        ></div>
                      </div>
                      <span className="text-xs font-mono font-medium text-slate-700">
                        {formatPercent(item.confidence)}
                      </span>
                    </div>
                  </td>

                  <td className="py-3.5 px-4 whitespace-nowrap">
                    {getPriorityBadge(item.priority)}
                  </td>

                  <td className="py-3.5 px-5 whitespace-nowrap">
                    {getActionBadge(item.recommended_action)}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Mobile Card List */}
      <div className="md:hidden divide-y divide-slate-100">
        {filtered.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-sm">
            No opportunities match the selected filters.
          </div>
        ) : (
          filtered.map((item, idx) => (
            <div key={`${item.source_id}-${idx}`} className="p-4 space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <h4 className="font-semibold text-slate-900 text-sm">{item.title}</h4>
                  <p className="text-xs text-slate-500 mt-0.5">{item.description}</p>
                </div>
                {getPriorityBadge(item.priority)}
              </div>

              <div className="flex items-center justify-between text-xs pt-1">
                <span className="text-slate-500">Est. Revenue:</span>
                <span className="font-bold text-slate-900">
                  {formatINR(item.estimated_revenue)}
                </span>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500">Confidence:</span>
                <span className="font-mono font-semibold text-slate-800">
                  {formatPercent(item.confidence)}
                </span>
              </div>

              <div className="pt-1">{getActionBadge(item.recommended_action)}</div>
            </div>
          ))
        )}
      </div>

      {/* Table Footer */}
      <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <span>Showing {filtered.length} bounded opportunities</span>
        <span>Bounded by Revora Policy Engine & RAG Guardrails</span>
      </div>
    </div>
  );
}
