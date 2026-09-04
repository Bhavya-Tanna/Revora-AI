import React from "react";

export function LoadingState({ message = "Loading revenue intelligence..." }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center">
      <div className="relative w-12 h-12 mb-4">
        <div className="absolute inset-0 rounded-full border-2 border-slate-200 animate-ping opacity-25"></div>
        <div className="w-12 h-12 rounded-full border-2 border-slate-900 border-t-transparent animate-spin"></div>
      </div>
      <p className="text-sm font-medium text-slate-600">{message}</p>
      <p className="text-xs text-slate-400 mt-1">Retrieving bounded merchant data & ML models</p>
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm animate-pulse">
      <div className="h-4 bg-slate-100 rounded w-1/3 mb-3"></div>
      <div className="h-8 bg-slate-200 rounded w-1/2 mb-4"></div>
      <div className="h-3 bg-slate-100 rounded w-2/3"></div>
    </div>
  );
}

export function ErrorState({
  title = "Failed to load data",
  message,
  onRetry,
}: {
  title?: string;
  message?: string;
  onRetry?: () => void;
}) {
  return (
    <div className="bg-white rounded-xl border border-rose-200 p-8 shadow-sm text-center max-w-lg mx-auto my-8">
      <div className="w-12 h-12 rounded-full bg-rose-50 text-rose-600 flex items-center justify-center mx-auto mb-4">
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <h3 className="text-base font-semibold text-slate-900 mb-1">{title}</h3>
      <p className="text-sm text-slate-600 mb-6">
        {message || "Could not connect to the Revora AI backend service. Please check if the FastAPI server is running on http://127.0.0.1:8000."}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg text-white bg-slate-900 hover:bg-slate-800 transition-colors shadow-sm"
        >
          <svg className="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Retry Connection
        </button>
      )}
    </div>
  );
}
