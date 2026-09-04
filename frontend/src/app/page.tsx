"use client";

import React, { useCallback, useEffect, useState } from "react";
import {
  Merchant,
  NavigationView,
  RevenueOpportunity,
  RevenueOverview,
} from "../lib/types";
import {
  fetchAgentActions,
  fetchAgentActionsCount,
  fetchMerchants,
  fetchOpportunities,
  fetchRevenueOverview,
} from "../lib/api";
import { formatCompactINR, formatINR } from "../lib/formatters";
import { Sidebar } from "../components/Sidebar";
import { Header } from "../components/Header";
import { KpiCard } from "../components/KpiCard";
import { OpportunityBreakdown } from "../components/OpportunityBreakdown";
import { OpportunityTable } from "../components/OpportunityTable";
import { GrowthAgent } from "../components/GrowthAgent";
import { ActionsView } from "../components/ActionsView";
import { AuditLogView } from "../components/AuditLogView";
import { SettingsView } from "../components/SettingsView";
import { ErrorState, LoadingState } from "../components/LoadingState";

export default function Home() {
  const [currentView, setCurrentView] = useState<NavigationView>("dashboard");
  const [selectedMerchantId, setSelectedMerchantId] = useState<number>(10);
  const [merchants, setMerchants] = useState<Merchant[]>([]);
  const [overview, setOverview] = useState<RevenueOverview | null>(null);
  const [opportunities, setOpportunities] = useState<RevenueOpportunity[]>([]);
  const [actionsCount, setActionsCount] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);

  // Load merchants list once
  useEffect(() => {
    let isMounted = true;
    async function loadMerchants() {
      try {
        const list = await fetchMerchants();
        if (isMounted && list.length > 0) {
          setMerchants(list);
        }
      } catch {
        // Fallback default merchant if list fails
        if (isMounted) {
          setMerchants([
            {
              id: 10,
              name: "Lumen Jewels",
              category: "Jewelry",
              monthly_revenue: 1250000,
              conversion_rate: 0.024,
              average_order_value: 8400,
              cart_abandonment_rate: 0.68,
              repeat_purchase_rate: 0.18,
            },
          ]);
        }
      }
    }
    loadMerchants();
    return () => {
      isMounted = false;
    };
  }, []);

  // Fetch live merchant metrics
  const loadMerchantData = useCallback(async (merchantId: number, isSilent = false) => {
    if (!isSilent) setLoading(true);
    setRefreshing(true);
    setError(null);

    try {
      const [overviewData, oppsData, totalActions] = await Promise.all([
        fetchRevenueOverview(merchantId),
        fetchOpportunities({ merchantId, limit: 50 }),
        fetchAgentActionsCount(merchantId),
      ]);

      setOverview(overviewData);
      setOpportunities(oppsData);
      setActionsCount(totalActions);
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to retrieve revenue intelligence data. Please verify the backend is running."
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadMerchantData(selectedMerchantId);
  }, [selectedMerchantId, loadMerchantData]);

  const handleRefresh = () => {
    loadMerchantData(selectedMerchantId, true);
  };

  const selectedMerchant = merchants.find((m) => m.id === selectedMerchantId);

  // Dynamic header titles based on view
  const viewHeaders: Record<NavigationView, { title: string; subtitle: string }> = {
    dashboard: {
      title: "Revenue Intelligence",
      subtitle: `AI-powered opportunities to grow merchant revenue (${selectedMerchant?.name ?? "Merchant #10"}).`,
    },
    agent: {
      title: "Growth Agent",
      subtitle: "Autonomous revenue agent with RAG policy validation and bounded execution.",
    },
    opportunities: {
      title: "Identified Opportunities",
      subtitle: "High-intent recovery and cross-sell opportunities detected by machine learning.",
    },
    actions: {
      title: "Actions & Approvals",
      subtitle: "Bounded agent actions, human-in-the-loop approval gating, and execution audit.",
    },
    audit: {
      title: "Audit Trail",
      subtitle: "Immutable event logs capturing every AI decision and guardrail evaluation.",
    },
    settings: {
      title: "Platform Settings",
      subtitle: "Configure autonomous limits, policy rules, and RAG knowledge base parameters.",
    },
  };

  return (
    <div className="min-h-screen flex bg-slate-50 text-slate-900">
      {/* Persistent Sidebar */}
      <Sidebar
        currentView={currentView}
        onSelectView={setCurrentView}
        isOpenMobile={mobileMenuOpen}
        onCloseMobile={() => setMobileMenuOpen(false)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title={viewHeaders[currentView].title}
          subtitle={viewHeaders[currentView].subtitle}
          merchants={merchants}
          selectedMerchantId={selectedMerchantId}
          onSelectMerchant={setSelectedMerchantId}
          onRefresh={handleRefresh}
          isRefreshing={refreshing}
          onToggleMobileMenu={() => setMobileMenuOpen(!mobileMenuOpen)}
        />

        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto space-y-8">
          {loading && !overview ? (
            <LoadingState message={`Analyzing live commerce data for ${selectedMerchant?.name ?? "Merchant #10"}...`} />
          ) : error && !overview ? (
            <ErrorState
              title="Connection Error"
              message={error}
              onRetry={() => loadMerchantData(selectedMerchantId)}
            />
          ) : (
            <>
              {/* DASHBOARD VIEW */}
              {currentView === "dashboard" && overview && (
                <div className="space-y-8">
                  {/* KPI Section (4 Cards) */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                    {/* KPI 1: Current Revenue */}
                    <KpiCard
                      title="Current Revenue"
                      value={formatCompactINR(overview.total_current_revenue)}
                      subtitle={`Total Order Spend: ${formatINR(overview.total_current_revenue)}`}
                      badgeText="Live Orders"
                      badgeVariant="emerald"
                      icon={
                        <svg className="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      }
                    />

                    {/* KPI 2: Estimated Opportunity */}
                    <KpiCard
                      title="Estimated Opportunity"
                      value={formatCompactINR(overview.total_estimated_opportunity)}
                      subtitle={`Potential Gain: ${formatINR(overview.total_estimated_opportunity)}`}
                      badgeText="ML Grounded"
                      badgeVariant="indigo"
                      icon={
                        <svg className="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                        </svg>
                      }
                    />

                    {/* KPI 3: High Priority Opportunities */}
                    <KpiCard
                      title="High Priority"
                      value={overview.high_priority_count.toString()}
                      subtitle="Requires prompt recovery attention"
                      badgeText="Actionable"
                      badgeVariant="amber"
                      icon={
                        <svg className="w-4 h-4 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                      }
                    />

                    {/* KPI 4: AI Actions Generated */}
                    <KpiCard
                      title="AI Actions Generated"
                      value={actionsCount.toString()}
                      subtitle={`Total actions for ${selectedMerchant?.name ?? "Merchant #" + selectedMerchantId}`}
                      badgeText="Audited"
                      badgeVariant="slate"
                      icon={
                        <svg className="w-4 h-4 text-slate-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                        </svg>
                      }
                    />
                  </div>

                  {/* Revenue Opportunity Breakdown */}
                  <OpportunityBreakdown
                    breakdown={overview.opportunity_breakdown}
                    totalOpportunity={overview.total_estimated_opportunity}
                  />

                  {/* Interactive Growth Agent Card */}
                  <GrowthAgent
                    merchantId={selectedMerchantId}
                    merchantName={selectedMerchant?.name}
                    onActionCreated={() => loadMerchantData(selectedMerchantId, true)}
                  />

                  {/* Top Opportunities List */}
                  <OpportunityTable
                    opportunities={
                      opportunities.length > 0
                        ? opportunities
                        : overview.top_opportunities
                    }
                  />
                </div>
              )}

              {/* GROWTH AGENT DEDICATED VIEW */}
              {currentView === "agent" && (
                <div className="space-y-6">
                  <GrowthAgent
                    merchantId={selectedMerchantId}
                    merchantName={selectedMerchant?.name}
                    onActionCreated={() => loadMerchantData(selectedMerchantId, true)}
                  />
                </div>
              )}

              {/* OPPORTUNITIES DEDICATED VIEW */}
              {currentView === "opportunities" && (
                <div className="space-y-6">
                  <OpportunityTable
                    opportunities={
                      opportunities.length > 0
                        ? opportunities
                        : overview?.top_opportunities ?? []
                    }
                  />
                </div>
              )}

              {/* ACTIONS & APPROVALS VIEW */}
              {currentView === "actions" && (
                <ActionsView merchantId={selectedMerchantId} />
              )}

              {/* AUDIT LOGS VIEW */}
              {currentView === "audit" && (
                <AuditLogView merchantId={selectedMerchantId} />
              )}

              {/* SETTINGS VIEW */}
              {currentView === "settings" && (
                <SettingsView merchantId={selectedMerchantId} />
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}
