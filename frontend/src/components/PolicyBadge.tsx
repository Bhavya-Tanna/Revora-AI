import React from "react";
import { PolicyDecision } from "../lib/types";

interface PolicyBadgeProps {
  decision: PolicyDecision;
  compact?: boolean;
}

export function PolicyBadge({ decision, compact = false }: PolicyBadgeProps) {
  const { allowed, requires_approval, reason, policy_ids } = decision;

  if (compact) {
    if (!allowed) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-50 text-rose-700 border border-rose-200">
          <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
          Blocked
        </span>
      );
    }
    if (requires_approval) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
          Approval Gated
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
        Auto-Allowed
      </span>
    );
  }

  return (
    <div className="flex flex-col gap-2 p-3 rounded-lg bg-slate-50 border border-slate-200 text-xs">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          {allowed ? (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md font-semibold bg-emerald-100 text-emerald-800">
              <svg className="w-3.5 h-3.5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
              Policy Allowed
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md font-semibold bg-rose-100 text-rose-800">
              <svg className="w-3.5 h-3.5 text-rose-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Policy Blocked
            </span>
          )}

          {requires_approval ? (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md font-medium bg-amber-100 text-amber-800">
              <svg className="w-3.5 h-3.5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              Merchant Approval Required
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md font-medium bg-slate-200 text-slate-700">
              No Approval Needed
            </span>
          )}
        </div>

        {policy_ids && policy_ids.length > 0 && (
          <div className="flex items-center gap-1">
            <span className="text-slate-400 font-medium">RAG Policies:</span>
            {policy_ids.map((id) => (
              <span
                key={id}
                className="px-1.5 py-0.5 rounded bg-slate-200 text-slate-700 font-mono text-[10px]"
              >
                #{id}
              </span>
            ))}
          </div>
        )}
      </div>

      <p className="text-slate-600 leading-relaxed font-normal">{reason}</p>
    </div>
  );
}
