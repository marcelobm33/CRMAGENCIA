import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Relatório Público",
  description: "Relatório público (sem dados sensíveis) para compartilhamento",
};

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-5xl mx-auto px-4 py-10">
        {children}
      </div>
    </div>
  );
}

