import { Sidebar } from "@/components/layout/sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-slate-50/50">
      <Sidebar />
      {/* Sidebar tem w-72 (18rem). Usar o mesmo padding-left para não “cortar” conteúdo. */}
      <div className="pl-72 flex flex-col min-h-screen min-w-0">
        <main className="flex-1 flex flex-col min-w-0 overflow-x-auto">
          {children}
        </main>
      </div>
    </div>
  );
}

