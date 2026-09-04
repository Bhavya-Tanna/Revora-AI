import React from "react";

interface SettingsViewProps {
  merchantId: number;
}

export function SettingsView({ merchantId }: SettingsViewProps) {
  return (
    <div className="space-y-6 max-w-4xl">
      {/* Overview Card */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
        <h3 className="text-base font-bold text-slate-900 mb-1">
          Policy Guardrails & Agentic Configuration
        </h3>
        <p className="text-xs text-slate-500 leading-relaxed">
          Configure bounded constraints, human-in-the-loop approval gating, and RAG policy retrieval thresholds for Merchant #{merchantId}.
        </p>
      </div>

      {/* Safety Guardrails */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-6">
        <h4 className="text-sm font-bold text-slate-900 pb-3 border-b border-slate-100 flex items-center gap-2">
          <svg className="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          Active Safety Guardrails
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-900">Minimum ML Confidence Threshold</span>
              <span className="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded border border-slate-200">
                0.40 (40%)
              </span>
            </div>
            <p className="text-slate-500 leading-normal">
              Opportunities below this confidence level are automatically blocked by the policy engine to prevent spurious recommendations.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-900">Financial Value Constraint</span>
              <span className="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded border border-slate-200">
                &gt; ₹0.00
              </span>
            </div>
            <p className="text-slate-500 leading-normal">
              All estimated recovery revenues must be strictly positive and grounded in actual order/cart database records.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-900">High-Impact Action Approval Gating</span>
              <span className="font-mono font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                ENFORCED
              </span>
            </div>
            <p className="text-slate-500 leading-normal">
              Actions such as <code className="font-mono">RETRY_PAYMENT</code>, <code className="font-mono">SEND_CART_RECOVERY_OFFER</code>, and <code className="font-mono">SEND_REACTIVATION_OFFER</code> require explicit merchant approval.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-900">LLM Deterministic Fallback</span>
              <span className="font-mono font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                ACTIVE
              </span>
            </div>
            <p className="text-slate-500 leading-normal">
              If the external LLM is offline or unconfigured, the agent falls back to deterministic structured explanations without failure.
            </p>
          </div>
        </div>
      </div>

      {/* RAG Knowledge Base Documents */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-4">
        <h4 className="text-sm font-bold text-slate-900 pb-3 border-b border-slate-100 flex items-center gap-2">
          <svg className="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          Active RAG Policy Knowledge Base Documents
        </h4>

        <div className="space-y-3 text-xs">
          {[
            {
              id: "cart_recovery",
              title: "Cart Recovery Policy",
              desc: "Abandoned cart recovery may use a targeted offer when the estimated recovery value justifies the incentive. Discounts must remain within merchant-configured limits.",
            },
            {
              id: "payment_recovery",
              title: "Payment Recovery Policy",
              desc: "Failed payments may be retried when the failure is temporary, such as gateway errors or timeouts. Insufficient-funds failures should not be repeatedly retried.",
            },
            {
              id: "customer_reactivation",
              title: "Customer Reactivation Policy",
              desc: "Dormant customers may receive personalized reactivation offers. High-value customers receive priority. Offers must be relevant to past behavior.",
            },
            {
              id: "agent_safety",
              title: "AI Agent Safety Policy",
              desc: "The AI agent must never execute financial actions without policy validation. High-impact actions require explicit approval. Every event is written to the audit log.",
            },
          ].map((doc) => (
            <div key={doc.id} className="p-3.5 rounded-lg border border-slate-100 bg-slate-50 flex items-start gap-3">
              <span className="font-mono text-xs font-semibold px-2 py-0.5 rounded bg-slate-200 text-slate-700">
                #{doc.id}
              </span>
              <div>
                <div className="font-semibold text-slate-900">{doc.title}</div>
                <div className="text-slate-600 mt-0.5 leading-relaxed">{doc.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
