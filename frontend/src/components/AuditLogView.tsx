import React, { useEffect, useState } from "react";
import { AuditLogItem } from "../lib/types";
import { fetchAuditLogs } from "../lib/api";
import { formatDate } from "../lib/formatters";
import { LoadingState } from "./LoadingState";

interface AuditLogViewProps {
  merchantId: number;
}

export function AuditLogView({ merchantId }: AuditLogViewProps) {
  const [logs, setLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedLogId, setExpandedLogId] = useState<number | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function loadLogs() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchAuditLogs(merchantId, 100);
        if (isMounted) setLogs(data);
      } catch (err: unknown) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : "Failed to load audit logs");
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    loadLogs();
    return () => {
      isMounted = false;
    };
  }, [merchantId]);

  return (
    <div className="space-y-6">
      {/* Header Info */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-indigo-600"></span>
            <h3 className="text-base font-bold text-slate-900">
              Audit Logs & Traceability Trail
            </h3>
          </div>
          <p className="text-xs text-slate-500 max-w-2xl leading-relaxed">
            Immutable audit record of every opportunity evaluated, policy decision executed, and merchant approval trigger.
            Provides end-to-end explainability and regulatory compliance for agentic commerce operations.
          </p>
        </div>
      </div>

      {/* Logs Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <LoadingState message="Fetching audit trail from database..." />
        ) : error ? (
          <div className="p-8 text-center text-rose-600 text-sm">{error}</div>
        ) : logs.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            No audit logs recorded for this merchant yet.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50/75 border-b border-slate-200 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                  <th className="py-3.5 px-5">Timestamp</th>
                  <th className="py-3.5 px-4">Event Type</th>
                  <th className="py-3.5 px-4">Action Reference</th>
                  <th className="py-3.5 px-5">Message / Context</th>
                  <th className="py-3.5 px-5 text-right">Metadata Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {logs.map((log) => {
                  const isExpanded = expandedLogId === log.id;
                  const hasMetadata =
                    log.metadata && Object.keys(log.metadata).length > 0;

                  return (
                    <React.Fragment key={log.id}>
                      <tr className="hover:bg-slate-50/50 transition-colors">
                        <td className="py-3.5 px-5 whitespace-nowrap text-xs font-mono text-slate-500">
                          {formatDate(log.created_at)}
                        </td>

                        <td className="py-3.5 px-4 whitespace-nowrap">
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-mono font-semibold bg-indigo-50 text-indigo-700 border border-indigo-100">
                            {log.event_type}
                          </span>
                        </td>

                        <td className="py-3.5 px-4 whitespace-nowrap">
                          <span className="font-mono text-xs font-semibold text-slate-800">
                            Action #{log.agent_action_id}
                          </span>
                        </td>

                        <td className="py-3.5 px-5 text-xs text-slate-700 max-w-md">
                          {log.message}
                        </td>

                        <td className="py-3.5 px-5 text-right whitespace-nowrap">
                          {hasMetadata ? (
                            <button
                              onClick={() =>
                                setExpandedLogId(isExpanded ? null : log.id)
                              }
                              className="inline-flex items-center gap-1 text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors cursor-pointer"
                            >
                              <span>{isExpanded ? "Hide JSON" : "View JSON"}</span>
                              <svg
                                className={`w-3.5 h-3.5 transition-transform ${
                                  isExpanded ? "rotate-180" : ""
                                }`}
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M19 9l-7 7-7-7"
                                />
                              </svg>
                            </button>
                          ) : (
                            <span className="text-xs text-slate-400 font-mono">-</span>
                          )}
                        </td>
                      </tr>

                      {isExpanded && hasMetadata && (
                        <tr className="bg-slate-900 text-slate-200">
                          <td colSpan={5} className="p-4 px-6">
                            <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800 text-xs text-slate-400">
                              <span className="font-mono">
                                Audit Log #{log.id} Payload
                              </span>
                              <span className="text-[11px]">JSON Schema</span>
                            </div>
                            <pre className="text-xs font-mono text-emerald-400 overflow-x-auto whitespace-pre-wrap leading-relaxed">
                              {JSON.stringify(log.metadata, null, 2)}
                            </pre>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span>Displaying {logs.length} audit trail records</span>
          <span className="italic">
            Source table: <code className="font-mono">audit_logs</code>
          </span>
        </div>
      </div>
    </div>
  );
}
