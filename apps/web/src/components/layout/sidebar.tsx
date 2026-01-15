"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  Target,
  Users,
  TrendingUp,
  Zap,
  Settings,
  BarChart3,
  Filter,
  PieChart,
  AlertTriangle,
} from "lucide-react";

const navigation = [
  { name: "ROI & Análise", href: "/dashboard/roi", icon: PieChart },
  { name: "Qualidade Leads", href: "/dashboard/roi/qualidade", icon: AlertTriangle },
  // Ocultos por enquanto (dependem da API principal / integrações ainda em evolução):
  // { name: "Canais", href: "/dashboard/channels", icon: Target },
  // { name: "Campanhas", href: "/dashboard/campaigns", icon: BarChart3 },
  // { name: "Vendedores", href: "/dashboard/vendedores", icon: Users },
  // { name: "Funil CRM", href: "/dashboard/funnel", icon: Filter },
  // { name: "IA Analista", href: "/dashboard/ai", icon: Zap },
];

const secondaryNav = [
  // Oculto por enquanto (está em construção)
  // { name: "Configurações", href: "/dashboard/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 z-50 w-72 bg-white/80 backdrop-blur-xl border-r border-slate-200/50">
      {/* Brand Logo */}
      <div className="flex h-28 items-center gap-4 px-10">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-600 shadow-xl shadow-blue-100 transform -rotate-3 transition-transform hover:rotate-0">
          <TrendingUp className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-sm font-black tracking-[0.2em] text-slate-900 uppercase">Automark</h1>
          <p className="text-[10px] font-bold text-blue-600 uppercase tracking-widest">Analytics iA</p>
        </div>
      </div>

      {/* Navigation Groups */}
      <div className="px-6 space-y-10 mt-6">
        <div>
          <h3 className="px-4 mb-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.3em]">
            Principal
          </h3>
          <nav className="space-y-1.5">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "group flex items-center gap-3.5 rounded-2xl px-5 py-3.5 text-xs transition-all duration-300",
                    isActive
                      ? "bg-blue-600 text-white font-bold shadow-lg shadow-blue-100"
                      : "text-slate-500 hover:text-slate-900 hover:bg-slate-50"
                  )}
                >
                  <item.icon className={cn(
                    "h-4 w-4 transition-colors",
                    isActive ? "text-white" : "text-slate-400 group-hover:text-slate-900"
                  )} />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>

        <div>
          <h3 className="px-4 mb-4 text-[10px] font-black text-slate-400 uppercase tracking-[0.3em]">
            Sistema
          </h3>
          <nav className="space-y-1.5">
            {secondaryNav.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "group flex items-center gap-3.5 rounded-2xl px-5 py-3.5 text-xs transition-all duration-300",
                    isActive
                      ? "bg-blue-600 text-white font-bold shadow-lg shadow-blue-100"
                      : "text-slate-500 hover:text-slate-900 hover:bg-slate-50"
                  )}
                >
                  <item.icon className={cn(
                    "h-4 w-4 transition-colors",
                    isActive ? "text-white" : "text-slate-400 group-hover:text-slate-900"
                  )} />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* User Card */}
      <div className="absolute bottom-10 left-6 right-6">
        <div className="flex items-center gap-4 rounded-[2rem] border border-slate-200/50 p-3 bg-white shadow-premium">
          <div className="h-10 w-10 rounded-full bg-slate-900 flex items-center justify-center border-2 border-white ring-1 ring-slate-100">
            <span className="text-[10px] font-black text-white">MM</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-black text-slate-900 truncate">Marcelo M.</p>
            <p className="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Diretor Comercial</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
