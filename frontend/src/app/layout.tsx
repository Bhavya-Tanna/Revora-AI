import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Revora AI — Merchant Growth Intelligence & Agentic Commerce",
  description:
    "AI-powered revenue opportunity detection, bounded growth agent, RAG policy engine, and merchant approval gating for the Razorpay AI Buildathon.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900 selection:bg-slate-900 selection:text-white">
        {children}
      </body>
    </html>
  );
}
