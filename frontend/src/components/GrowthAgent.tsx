import React, { useState } from "react";
import { AgentAnalyzeResponse, AgentRecommendation } from "../lib/types";
import { analyzeMerchant } from "../lib/api";
import { PolicyBadge } from "./PolicyBadge";
import { formatINR, formatPercent } from "../lib/formatters";

interface GrowthAgentProps {
  merchantId: number;
  merchantName?: string;
  onActionCreated?: () => void;
}

export function GrowthAgent({
  merchantId,
  merchantName,
  onActionCreated,
}: GrowthAgentProps) {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AgentAnalyzeResponse | null>(null);
  const [hasRun, setHasRun] = useState<boolean>(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await analyzeMerchant(merchantId, 10);
      setAnalysisResult(response);
      setHasRun(true);
      if (onActionCreated) {
        onActionCreated();
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to run agent analysis. Check backend connectivity.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Agent Banner & Control Bar */}
      <div className="p-6 bg-gradient-to-r from-slate-900 to-slate-800 text-white flex flex-col md:flex-row md:items-center justify-between gap-5">
        <div className="space-y-1">
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-xs uppercase tracking-widest font-semibold text-emerald-400">
              Autonomous Growth Agent & Policy Engine
            </span>
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">
            Growth Agent {merchantName ? `— ${merchantName}` : ""}
          </h2>
          <p className="text-sm text-slate-300 max-w-2xl leading-relaxed">
            Let Revora analyze this merchant and identify the highest-value actions.
            Actions are vetted via RAG retrieval and verified against strict policy guardrails before execution.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="inline-flex items-center justify-center px-5 py-2.5 rounded-lg text-sm font-semibold bg-white text-slate-900 hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm active:scale-98 cursor-pointer"
          >
            {loading ? (
              <>
                <svg
                  className="animate-spin -ml-1 mr-2 h-4 w-4 text-slate-900"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Reasoning & Evaluating Guardrails...
              </>
            ) : (
              <>
                <svg
                  className="w-4 h-4 mr-2 text-slate-700"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
                Analyze Merchant
              </>
            )}
          </button>
        </div>
      </div>

      {/* Loading State Animation */}
      {loading && (
        <div className="p-12 text-center bg-slate-50/50">
          <div className="max-w-md mx-auto space-y-4">
            <div className="w-12 h-12 border-2 border-slate-900 border-t-transparent rounded-full animate-spin mx-auto"></div>
            <h4 className="text-sm font-semibold text-slate-800">
              Revora Growth Agent in Progress
            </h4>
            <div className="text-xs text-slate-500 space-y-1">
              <p className="flex items-center justify-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                Evaluating customer purchase frequencies & cart states
              </p>
              <p className="flex items-center justify-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
                Querying RAG policy knowledge base
              </p>
              <p className="flex items-center justify-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                Validating autonomous bounds & approval requirements
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Error Banner */}
      {error && !loading && (
        <div className="p-6 bg-rose-50 border-b border-rose-100 flex items-start gap-3">
          <svg
            className="w-5 h-5 text-rose-600 shrink-0 mt-0.5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div className="text-xs">
            <span className="font-semibold text-rose-800">Analysis Failed: </span>
            <span className="text-rose-700">{error}</span>
          </div>
        </div>
      )}

      {/* Recommendations List */}
      {analysisResult && !loading && (
        <div className="p-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 mb-6 gap-2">
            <div>
              <h3 className="text-sm font-bold text-slate-900">
                Agent Recommendations ({analysisResult.recommendations.length})
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Analyzed {analysisResult.opportunities_analyzed} opportunities for Merchant #{analysisResult.merchant_id}
              </p>
            </div>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              Policy Guardrails Enforced
            </span>
          </div>

          <div className="space-y-4">
            {analysisResult.recommendations.map((rec: AgentRecommendation, idx: number) => (
              <div
                key={idx}
                className="p-5 rounded-xl border border-slate-200 bg-white hover:border-slate-300 transition-all space-y-4 shadow-2xs"
              >
                {/* Header Row: Title & Action ID */}
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-bold text-slate-900">
                        {rec.opportunity.title}
                      </h4>
                      {rec.action_id ? (
                        <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-mono text-xs font-semibold">
                          Action #{rec.action_id}
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded bg-rose-50 text-rose-700 font-mono text-xs">
                          Action Blocked
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-600">
                      {rec.opportunity.description}
                    </p>
                  </div>

                  <div className="flex items-baseline gap-2 shrink-0">
                    <span className="text-xs text-slate-500">Est. Impact:</span>
                    <span className="text-base font-bold text-emerald-600">
                      {formatINR(rec.opportunity.estimated_revenue)}
                    </span>
                  </div>
                </div>

                {/* AI Explanation Box */}
                <div className="p-3.5 rounded-lg bg-indigo-50/50 border border-indigo-100 flex items-start gap-2.5">
                  <div className="w-5 h-5 rounded bg-indigo-600 text-white flex items-center justify-center shrink-0 mt-0.5">
                    <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <div className="space-y-0.5">
                    <div className="text-[11px] font-semibold text-indigo-900 uppercase tracking-wider">
                      Revora AI Explanation
                    </div>
                    <p className="text-xs text-slate-700 leading-relaxed font-normal">
                      {rec.llm_explanation}
                    </p>
                  </div>
                </div>

                {/* Policy Decision & Guardrails */}
                <PolicyBadge decision={rec.policy_decision} />

                {/* Footer details: Customer, Confidence, Recommended Action */}
                <div className="flex flex-wrap items-center justify-between pt-2 text-xs border-t border-slate-100 text-slate-500 gap-2">
                  <div className="flex items-center gap-4">
                    <span>
                      Target Customer:{" "}
                      <strong className="text-slate-800 font-mono">
                        #{rec.opportunity.customer_id ?? "N/A"}
                      </strong>
                    </span>
                    <span>
                      Confidence:{" "}
                      <strong className="text-slate-800 font-mono">
                        {formatPercent(rec.opportunity.confidence)}
                      </strong>
                    </span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <span className="text-slate-400">Action:</span>
                    <span className="px-2 py-0.5 rounded font-mono text-[11px] font-medium bg-slate-900 text-white">
                      {rec.opportunity.recommended_action}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State before running */}
      {!analysisResult && !loading && !error && (
        <div className="p-10 text-center text-slate-500 text-xs">
          Click <strong className="text-slate-800">Analyze Merchant</strong> above to run bounded RAG policy retrieval, predict reactivation probabilities, and generate policy-controlled growth recommendations.
        </div>
      )}
    </div>
  );
}
