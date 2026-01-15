"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/layout/header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MetricCard } from "@/components/dashboard/metric-card";
import {
  Users,
  TrendingUp,
  Trophy,
  Target,
  DollarSign,
  Percent,
  RefreshCw,
} from "lucide-react";
import { getCRMVendedores, getCRMResumo } from "@/lib/api";
import { cn } from "@/lib/utils";

interface VendedorData {
  vendedor_id: number;
  vendedor: string;
  total_leads: number;
  ganhos: number;
  perdidos: number;
  em_andamento: number;
  valor_vendido: number;
  ticket_medio: number;
  taxa_conversao: number;
}

interface CRMResumo {
  total_leads: number;
  ganhos: number;
  taxa_conversao: number;
  valor_vendido: number;
}

export default function VendedoresPage() {
  const [vendedores, setVendedores] = useState<VendedorData[]>([]);
  const [resumo, setResumo] = useState<CRMResumo | null>(null);
  const [loading, setLoading] = useState(true);
  const [dias, setDias] = useState(30);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatNumber = (value: number) => {
    return new Intl.NumberFormat('pt-BR').format(value);
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const [vendedoresData, resumoData] = await Promise.all([
        getCRMVendedores(dias),
        getCRMResumo()
      ]);
      setVendedores(vendedoresData as VendedorData[]);
      setResumo(resumoData as CRMResumo);
    } catch (err) {
      console.error('Erro ao carregar vendedores:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [dias]);

  // Ranking (ordenado por vendas)
  const ranking = [...vendedores].sort((a, b) => b.ganhos - a.ganhos);
  const topVendedor = ranking[0];

  return (
    <>
      <Header title="Sales Performance" description="Real-time Team Analytics" />

      <div className="p-12 space-y-10 max-w-[1600px] mx-auto w-full">
        {/* Filtros & Controls */}
        <div className="flex items-center justify-between bg-white p-2 rounded-2xl border border-slate-200/50 shadow-sm">
          <div className="flex items-center gap-1">
            {[7, 30, 90, 365].map((d) => (
              <button
                key={d}
                onClick={() => setDias(d)}
                className={cn(
                  "px-6 py-2.5 rounded-xl text-[11px] font-black uppercase tracking-widest transition-all",
                  dias === d 
                    ? "bg-slate-900 text-white shadow-lg shadow-slate-200" 
                    : "text-slate-400 hover:text-slate-900 hover:bg-slate-50"
                )}
              >
                {d === 365 ? '1 Year' : `${d} Days`}
              </button>
            ))}
          </div>
          <button
            onClick={loadData}
            disabled={loading}
            className="flex items-center gap-2.5 px-6 py-2.5 text-[11px] font-black uppercase tracking-widest text-slate-600 hover:text-slate-900 transition-all disabled:opacity-50"
          >
            <RefreshCw className={cn("h-3.5 w-3.5", loading && "animate-spin")} />
            Sync Stats
          </button>
        </div>

        {/* Métricas gerais */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            label="Active Agents"
            value={vendedores.length.toString()}
            icon={Users}
          />
          <MetricCard
            label="Team Conversions"
            value={resumo ? formatNumber(resumo.ganhos) : "---"}
            icon={Target}
          />
          <MetricCard
            label="Gross Volume"
            value={resumo ? formatCurrency(resumo.valor_vendido) : "---"}
            icon={DollarSign}
          />
          <MetricCard
            label="Avg Team Conv."
            value={resumo ? `${resumo.taxa_conversao}%` : "---"}
            icon={Percent}
          />
        </div>

        {/* Top Performer Spotlight */}
        {topVendedor && (
          <Card className="border-none bg-slate-900 shadow-xl shadow-slate-200 overflow-hidden relative">
             <div className="absolute top-0 right-0 p-12 opacity-5">
                <Trophy className="h-40 w-40 text-white" />
             </div>
            <CardContent className="flex flex-col md:flex-row items-center gap-10 p-10 relative z-10">
              <div className="h-20 w-20 rounded-3xl bg-white/10 flex items-center justify-center border border-white/10 shadow-inner">
                <Trophy className="h-10 w-10 text-yellow-500" />
              </div>
              <div className="flex-1 text-center md:text-left">
                <p className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500 mb-2">Period Champion</p>
                <h2 className="text-3xl font-black text-white">{topVendedor.vendedor || 'Consultant'}</h2>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-12 w-full md:w-auto">
                <div className="text-center md:text-right">
                  <p className="text-2xl font-black text-white">{topVendedor.ganhos}</p>
                  <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mt-1">Sales</p>
                </div>
                <div className="text-center md:text-right">
                  <p className="text-2xl font-black text-emerald-400">{topVendedor.taxa_conversao}%</p>
                  <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mt-1">Efficiency</p>
                </div>
                <div className="text-center md:text-right">
                  <p className="text-2xl font-black text-white">{formatCurrency(topVendedor.valor_vendido)}</p>
                  <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mt-1">Revenue</p>
                </div>
                <div className="text-center md:text-right">
                  <p className="text-2xl font-black text-white">{formatCurrency(topVendedor.ticket_medio || 0)}</p>
                  <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mt-1">Avg Deal</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Main Leaderboard */}
        <Card className="border-slate-200/50 shadow-sm bg-white overflow-hidden">
          <CardHeader className="p-8 border-b border-slate-50">
             <CardTitle className="text-xs font-black text-slate-900 uppercase tracking-[0.2em]">Consultant Leaderboard</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            {loading ? (
              <div className="py-20 flex flex-col items-center justify-center gap-4">
                <RefreshCw className="h-8 w-8 text-slate-200 animate-spin" />
                <p className="text-[11px] font-black uppercase tracking-widest text-slate-400">Fetching Data...</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-slate-50/50">
                      <th className="text-left py-4 px-8 text-[10px] font-black uppercase tracking-widest text-slate-400">Rank</th>
                      <th className="text-left py-4 px-8 text-[10px] font-black uppercase tracking-widest text-slate-400">Consultant</th>
                      <th className="text-right py-4 px-8 text-[10px] font-black uppercase tracking-widest text-slate-400">Leads</th>
                      <th className="text-right py-4 px-8 text-[10px] font-black uppercase tracking-widest text-slate-400">Won</th>
                      <th className="text-right py-4 px-8 text-[10px] font-black uppercase tracking-widest text-slate-400">Conv %</th>
                      <th className="text-right py-4 px-8 text-[10px] font-black uppercase tracking-widest text-slate-400">Revenue</th>
                      <th className="text-right py-4 px-8 text-[10px] font-black uppercase tracking-widest text-slate-400">Avg Deal</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {ranking.map((vendedor, idx) => (
                      <tr 
                        key={vendedor.vendedor_id} 
                        className="group hover:bg-slate-50/50 transition-colors"
                      >
                        <td className="py-5 px-8">
                          <div className={cn(
                            "w-7 h-7 rounded-lg flex items-center justify-center text-[11px] font-black",
                            idx === 0 ? "bg-yellow-100 text-yellow-700" :
                            idx === 1 ? "bg-slate-100 text-slate-600" :
                            idx === 2 ? "bg-orange-100 text-orange-700" :
                            "text-slate-400"
                          )}>
                            {idx + 1}
                          </div>
                        </td>
                        <td className="py-5 px-8">
                          <p className="text-sm font-black text-slate-900">{vendedor.vendedor || 'Unassigned'}</p>
                        </td>
                        <td className="py-5 px-8 text-right text-xs font-bold text-slate-600">
                          {formatNumber(vendedor.total_leads)}
                        </td>
                        <td className="py-5 px-8 text-right">
                          <span className="text-xs font-black text-emerald-600">
                            {formatNumber(vendedor.ganhos)}
                          </span>
                        </td>
                        <td className="py-5 px-8 text-right">
                          <Badge variant={
                            vendedor.taxa_conversao >= 25 ? "success" :
                            vendedor.taxa_conversao >= 15 ? "warning" :
                            "destructive"
                          } className="h-6 px-3 text-[10px] font-black">
                            {vendedor.taxa_conversao}%
                          </Badge>
                        </td>
                        <td className="py-5 px-8 text-right text-sm font-black text-slate-900">
                          {formatCurrency(vendedor.valor_vendido)}
                        </td>
                        <td className="py-5 px-8 text-right text-xs font-bold text-slate-400">
                          {formatCurrency(vendedor.ticket_medio || 0)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </>
  );
}
