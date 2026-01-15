"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Header } from "@/components/layout/header";
import { MetricCard } from "@/components/dashboard/metric-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  DollarSign,
  Users,
  Target,
  TrendingUp,
  ShoppingCart,
  Percent,
  Zap,
  RefreshCw,
  Wifi,
  WifiOff,
  ChevronRight,
  ArrowUpRight,
} from "lucide-react";
import { getCRMResumo, getCRMSyncStatus, getCRMOrigens, getCRMFunil } from "@/lib/api";
import { cn } from "@/lib/utils";

interface CRMResumo {
  periodo: string;
  total_leads: number;
  ganhos: number;
  perdidos: number;
  em_andamento: number;
  taxa_conversao: number;
  valor_vendido: number;
  ticket_medio: number;
}

interface CRMSyncStatus {
  crm_externo: {
    host: string;
    database: string;
    conexao: boolean;
  };
  sincronizacao: {
    total_sincronizado: number;
    total_crm_externo: number;
    ultima_sincronizacao: string | null;
  };
}

interface OrigemData {
  grupo_origem: string;
  total_leads: number;
  ganhos: number;
  perdidos: number;
  valor_vendido: number;
  taxa_conversao: number;
}

interface FunilData {
  id_state: number;
  etapa: string;
  quantidade: number;
  valor_total: number;
  ticket_medio: number;
}

export default function DashboardPage() {
  const router = useRouter();
  const [resumo, setResumo] = useState<CRMResumo | null>(null);
  const [status, setStatus] = useState<CRMSyncStatus | null>(null);
  const [origens, setOrigens] = useState<OrigemData[]>([]);
  const [funil, setFunil] = useState<FunilData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      maximumFractionDigits: 0
    }).format(value);
  };

  const formatNumber = (value: number) => {
    return new Intl.NumberFormat('pt-BR').format(value);
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const [resumoData, statusData, origensData, funilData] = await Promise.allSettled([
        getCRMResumo(),
        getCRMSyncStatus(),
        getCRMOrigens(30),
        getCRMFunil()
      ]);

      if (resumoData.status === 'fulfilled') setResumo(resumoData.value as CRMResumo);
      if (statusData.status === 'fulfilled') setStatus(statusData.value as CRMSyncStatus);
      if (origensData.status === 'fulfilled') setOrigens(origensData.value as OrigemData[]);
      if (funilData.status === 'fulfilled') setFunil(funilData.value as FunilData[]);
    } catch (err) {
      setError('Erro ao sincronizar dados');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Enquanto a API principal não estiver ligada, direciona para o dashboard de ROI
    // (evita páginas “sem dados” durante a apresentação)
    router.replace("/dashboard/roi");
    return;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 120000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <Header title="Visão Geral" description="Métricas de desempenho em tempo real" />

      <div className="p-8 lg:p-12 space-y-12 max-w-[1600px] mx-auto animate-fade-up">
        
        {/* Superior: Status e IA */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
          <Card className="lg:col-span-8 overflow-hidden border-none shadow-premium bg-white group">
            <CardContent className="p-0 flex h-full">
              <div className={cn(
                "w-2 transition-colors duration-500",
                status?.crm_externo?.conexao ? "bg-emerald-500" : "bg-rose-500"
              )} />
              <div className="flex-1 p-8 flex items-center justify-between">
                <div className="flex items-center gap-6">
                  <div className={cn(
                    "h-16 w-16 rounded-2xl flex items-center justify-center transition-all duration-500",
                    status?.crm_externo?.conexao ? "bg-emerald-50 text-emerald-600" : "bg-rose-50 text-rose-500"
                  )}>
                    {status?.crm_externo?.conexao ? <Wifi className="h-8 w-8" /> : <WifiOff className="h-8 w-8" />}
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-slate-900 tracking-tight">
                      {status?.crm_externo?.conexao ? "Base de Dados Conectada" : "Erro na Conexão"}
                    </h2>
                    <p className="text-sm font-medium text-slate-500 mt-1">
                      {status?.crm_externo?.conexao 
                        ? `Sincronizando em tempo real com ${status.crm_externo.database}`
                        : "Verifique as configurações de acesso ao MySQL"}
                    </p>
                  </div>
                </div>
                <button 
                  onClick={loadData}
                  disabled={loading}
                  className="flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-900 text-white text-xs font-bold uppercase tracking-widest hover:bg-slate-800 transition-all disabled:opacity-50 shadow-lg shadow-slate-200"
                >
                  <RefreshCw className={cn("h-4 w-4", loading && "animate-spin")} />
                  {loading ? "Sincronizando..." : "Sincronizar Agora"}
                </button>
              </div>
            </CardContent>
          </Card>

          <Card className="lg:col-span-4 border-none bg-blue-600 shadow-xl shadow-blue-100 overflow-hidden relative group cursor-pointer">
            <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform duration-500">
              <Zap className="h-40 w-40 text-white" />
            </div>
            <CardContent className="p-8 relative z-10 flex flex-col h-full justify-between">
              <div>
                <Badge className="bg-white/20 text-white border-none text-[9px] font-black uppercase tracking-widest mb-4">
                  IA Analista
                </Badge>
                <h3 className="text-2xl font-bold text-white leading-tight">
                  Descubra insights com Inteligência Artificial
                </h3>
              </div>
              <div className="flex items-center gap-2 text-white/90 text-sm font-bold group-hover:gap-4 transition-all mt-6">
                Acessar Analista <ArrowUpRight className="h-4 w-4" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Métricas Principais */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Indicadores de Performance</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            <MetricCard label="Total de Leads" value={resumo ? formatNumber(resumo.total_leads) : "---"} icon={Users} color="blue" />
            <MetricCard label="Vendas Fechadas" value={resumo ? formatNumber(resumo.ganhos) : "---"} icon={ShoppingCart} color="emerald" />
            <MetricCard label="Taxa Conversão" value={resumo ? `${resumo.taxa_conversao}%` : "---"} icon={Percent} color="indigo" />
            <MetricCard label="Receita Total" value={resumo ? formatCurrency(resumo.valor_vendido) : "---"} icon={DollarSign} color="slate" />
            <MetricCard label="Ticket Médio" value={resumo ? formatCurrency(resumo.ticket_medio) : "---"} icon={TrendingUp} color="blue" />
          </div>
        </div>

        {/* Gráficos e Detalhes */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Funil de Vendas */}
          <Card className="lg:col-span-8 border-none shadow-premium bg-white">
            <CardHeader className="p-8 border-b border-slate-50 flex flex-row items-center justify-between">
              <div>
                <CardTitle className="text-sm font-bold text-slate-900 uppercase tracking-widest">Fluxo do Funil</CardTitle>
                <p className="text-xs font-medium text-slate-400 mt-1">Distribuição de leads por etapa</p>
              </div>
              <Badge variant="secondary" className="bg-slate-50 text-slate-400 border-none font-bold">Últimos 30 dias</Badge>
            </CardHeader>
            <CardContent className="p-8">
              <div className="space-y-6">
                {funil.map((etapa, idx) => {
                  const maxVal = Math.max(...funil.map(f => f.quantidade), 1);
                  const width = (etapa.quantidade / maxVal) * 100;
                  return (
                    <div key={etapa.id_state} className="group cursor-default">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-[11px] font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                          <span className="h-5 w-5 rounded-md bg-slate-100 flex items-center justify-center text-[10px] text-slate-500">{idx + 1}</span>
                          {etapa.etapa.split('.')[1] || etapa.etapa}
                        </span>
                        <span className="text-xs font-black text-slate-900">{formatNumber(etapa.quantidade)}</span>
                      </div>
                      <div className="h-2.5 w-full bg-slate-50 rounded-full overflow-hidden border border-slate-100">
                        <div 
                          className={cn(
                            "h-full rounded-full transition-all duration-1000 ease-out group-hover:opacity-80",
                            etapa.id_state === 6 ? "bg-emerald-500" : etapa.id_state === 7 ? "bg-slate-300" : "bg-blue-500"
                          )}
                          style={{ width: `${width}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Melhores Canais */}
          <div className="lg:col-span-4 space-y-8">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Canais de Conversão</h3>
              <button className="text-[10px] font-bold text-blue-600 uppercase tracking-widest hover:underline">Ver Todos</button>
            </div>
            <div className="space-y-4">
              {origens.slice(0, 5).map((origem, idx) => (
                <Card key={origem.grupo_origem} className="border-none shadow-sm bg-white hover:translate-x-1 transition-all group">
                  <CardContent className="p-5 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="h-12 w-12 rounded-2xl bg-slate-50 flex items-center justify-center text-[11px] font-black text-slate-400 group-hover:bg-slate-900 group-hover:text-white transition-colors">
                        {origem.grupo_origem.substring(0, 2)}
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-slate-900">{origem.grupo_origem}</h4>
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">{formatNumber(origem.total_leads)} Leads</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-black text-slate-900">{origem.taxa_conversao}%</p>
                      <div className="flex items-center gap-1 justify-end text-[9px] font-black text-emerald-500 uppercase">
                        <TrendingUp className="h-2 w-2" /> Eficiente
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

        </div>
      </div>
    </>
  );
}
