"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/layout/header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MetricCard } from "@/components/dashboard/metric-card";
import {
  Facebook,
  Search,
  Globe,
  Users,
  Phone,
  UserPlus,
  Share2,
  Store,
  RefreshCw,
  TrendingUp,
  DollarSign,
  Target,
  Percent,
} from "lucide-react";
import { getCRMOrigens, getCRMMetaVsGoogle } from "@/lib/api";

interface OrigemData {
  grupo_origem: string;
  total_leads: number;
  ganhos: number;
  perdidos: number;
  valor_vendido: number;
  ticket_medio: number;
  taxa_conversao: number;
}

interface MetaVsGoogle {
  META: OrigemData | null;
  GOOGLE: OrigemData | null;
}

const origemIcons: Record<string, any> = {
  META: Facebook,
  GOOGLE: Search,
  SITE: Globe,
  PORTAIS: Store,
  PRESENCIAL: Users,
  DIRETO: Phone,
  INDICACAO: UserPlus,
  OUTROS: Share2,
};

const origemColors: Record<string, string> = {
  META: "bg-blue-500",
  GOOGLE: "bg-orange-500",
  SITE: "bg-emerald-500",
  PORTAIS: "bg-purple-500",
  PRESENCIAL: "bg-amber-500",
  DIRETO: "bg-cyan-500",
  INDICACAO: "bg-pink-500",
  OUTROS: "bg-gray-500",
};

export default function ChannelsPage() {
  const [origens, setOrigens] = useState<OrigemData[]>([]);
  const [comparativo, setComparativo] = useState<MetaVsGoogle | null>(null);
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
      const [origensData, compData] = await Promise.all([
        getCRMOrigens(dias),
        getCRMMetaVsGoogle(dias)
      ]);
      setOrigens(origensData as OrigemData[]);
      setComparativo(compData as MetaVsGoogle);
    } catch (err) {
      console.error('Erro ao carregar origens:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [dias]);

  // Totais
  const totalLeads = origens.reduce((sum, o) => sum + o.total_leads, 0);
  const totalGanhos = origens.reduce((sum, o) => sum + o.ganhos, 0);
  const totalValor = origens.reduce((sum, o) => sum + o.valor_vendido, 0);

  // Ordenar por vendas
  const origensOrdenadas = [...origens].sort((a, b) => b.ganhos - a.ganhos);

  return (
    <>
      <Header title="Canais de Aquisição" description="Performance por origem de leads" />

      <div className="p-6 space-y-6">
        {/* Filtros */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">Período:</span>
            {[7, 30, 90, 365].map((d) => (
              <button
                key={d}
                onClick={() => setDias(d)}
                className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                  dias === d 
                    ? 'bg-primary text-primary-foreground' 
                    : 'bg-secondary hover:bg-secondary/80'
                }`}
              >
                {d === 365 ? '1 ano' : `${d} dias`}
              </button>
            ))}
          </div>
          <button
            onClick={loadData}
            disabled={loading}
            className="flex items-center gap-2 text-sm font-medium text-primary hover:underline disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            Atualizar
          </button>
        </div>

        {/* Métricas gerais */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            label="Total de Origens"
            value={origens.length.toString()}
            icon={Share2}
          />
          <MetricCard
            label="Total de Leads"
            value={formatNumber(totalLeads)}
            icon={Users}
          />
          <MetricCard
            label="Total de Vendas"
            value={formatNumber(totalGanhos)}
            icon={Target}
          />
          <MetricCard
            label="Faturamento Total"
            value={formatCurrency(totalValor)}
            icon={DollarSign}
          />
        </div>

        {/* META vs GOOGLE (destaque) */}
        {comparativo && (comparativo.META || comparativo.GOOGLE) && (
          <Card>
            <CardHeader>
              <CardTitle className="text-base font-medium">
                META vs GOOGLE - Comparativo Direto
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-2">
                {/* META */}
                <div className="rounded-xl border-2 border-blue-500/30 bg-blue-500/5 p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="rounded-lg bg-blue-500 p-2">
                      <Facebook className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-bold text-lg">META</h3>
                      <p className="text-sm text-muted-foreground">Facebook + Instagram</p>
                    </div>
                  </div>
                  {comparativo.META ? (
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-background/50 rounded-lg p-3 text-center">
                        <p className="text-2xl font-bold">{formatNumber(comparativo.META.total_leads)}</p>
                        <p className="text-xs text-muted-foreground">Leads</p>
                      </div>
                      <div className="bg-background/50 rounded-lg p-3 text-center">
                        <p className="text-2xl font-bold text-green-500">{formatNumber(comparativo.META.ganhos)}</p>
                        <p className="text-xs text-muted-foreground">Vendas</p>
                      </div>
                      <div className="bg-background/50 rounded-lg p-3 text-center">
                        <p className="text-2xl font-bold">{comparativo.META.taxa_conversao}%</p>
                        <p className="text-xs text-muted-foreground">Conversão</p>
                      </div>
                      <div className="bg-background/50 rounded-lg p-3 text-center">
                        <p className="text-xl font-bold">{formatCurrency(comparativo.META.valor_vendido)}</p>
                        <p className="text-xs text-muted-foreground">Faturamento</p>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center py-8 text-muted-foreground">Sem dados no período</p>
                  )}
                </div>

                {/* GOOGLE */}
                <div className="rounded-xl border-2 border-orange-500/30 bg-orange-500/5 p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="rounded-lg bg-orange-500 p-2">
                      <Search className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-bold text-lg">GOOGLE</h3>
                      <p className="text-sm text-muted-foreground">Pesquisa + Display</p>
                    </div>
                  </div>
                  {comparativo.GOOGLE ? (
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-background/50 rounded-lg p-3 text-center">
                        <p className="text-2xl font-bold">{formatNumber(comparativo.GOOGLE.total_leads)}</p>
                        <p className="text-xs text-muted-foreground">Leads</p>
                      </div>
                      <div className="bg-background/50 rounded-lg p-3 text-center">
                        <p className="text-2xl font-bold text-green-500">{formatNumber(comparativo.GOOGLE.ganhos)}</p>
                        <p className="text-xs text-muted-foreground">Vendas</p>
                      </div>
                      <div className="bg-background/50 rounded-lg p-3 text-center">
                        <p className="text-2xl font-bold">{comparativo.GOOGLE.taxa_conversao}%</p>
                        <p className="text-xs text-muted-foreground">Conversão</p>
                      </div>
                      <div className="bg-background/50 rounded-lg p-3 text-center">
                        <p className="text-xl font-bold">{formatCurrency(comparativo.GOOGLE.valor_vendido)}</p>
                        <p className="text-xs text-muted-foreground">Faturamento</p>
                      </div>
                    </div>
                  ) : (
                    <p className="text-center py-8 text-muted-foreground">Sem dados no período</p>
                  )}
                </div>
              </div>

              {/* Vencedor */}
              {comparativo.META && comparativo.GOOGLE && (
                <div className="mt-4 p-4 rounded-lg bg-secondary/50 text-center">
                  {comparativo.META.taxa_conversao > comparativo.GOOGLE.taxa_conversao ? (
                    <p className="text-sm">
                      <span className="font-bold text-blue-500">META</span> converte{' '}
                      <span className="font-bold">
                        {(comparativo.META.taxa_conversao - comparativo.GOOGLE.taxa_conversao).toFixed(1)}%
                      </span>{' '}
                      mais que GOOGLE
                    </p>
                  ) : comparativo.GOOGLE.taxa_conversao > comparativo.META.taxa_conversao ? (
                    <p className="text-sm">
                      <span className="font-bold text-orange-500">GOOGLE</span> converte{' '}
                      <span className="font-bold">
                        {(comparativo.GOOGLE.taxa_conversao - comparativo.META.taxa_conversao).toFixed(1)}%
                      </span>{' '}
                      mais que META
                    </p>
                  ) : (
                    <p className="text-sm">Ambos têm a mesma taxa de conversão</p>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Todas as origens */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-medium">
              Todas as Origens
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8 text-muted-foreground">
                Carregando dados do CRM...
              </div>
            ) : (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {origensOrdenadas.map((origem) => {
                  const Icon = origemIcons[origem.grupo_origem] || Share2;
                  const color = origemColors[origem.grupo_origem] || "bg-gray-500";
                  
                  return (
                    <div 
                      key={origem.grupo_origem}
                      className="rounded-xl border p-4 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-center gap-3 mb-4">
                        <div className={`rounded-lg ${color} p-2`}>
                          <Icon className="h-5 w-5 text-white" />
                        </div>
                        <h3 className="font-bold">{origem.grupo_origem}</h3>
                      </div>
                      
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Leads</span>
                          <span className="font-medium">{formatNumber(origem.total_leads)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Vendas</span>
                          <span className="font-medium text-green-500">{formatNumber(origem.ganhos)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Conversão</span>
                          <Badge variant={
                            origem.taxa_conversao >= 25 ? "success" :
                            origem.taxa_conversao >= 15 ? "warning" :
                            "destructive"
                          }>
                            {origem.taxa_conversao}%
                          </Badge>
                        </div>
                        <div className="flex justify-between pt-2 border-t border-border">
                          <span className="text-muted-foreground">Faturamento</span>
                          <span className="font-bold">{formatCurrency(origem.valor_vendido)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Ticket Médio</span>
                          <span className="font-medium">{formatCurrency(origem.ticket_medio || 0)}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Gráfico de barras */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-medium">
              Ranking por Vendas
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {origensOrdenadas.map((origem) => {
                const maxGanhos = Math.max(...origensOrdenadas.map(o => o.ganhos), 1);
                const color = origemColors[origem.grupo_origem] || "bg-gray-500";
                
                return (
                  <div key={origem.grupo_origem} className="flex items-center gap-4">
                    <div className="w-24 truncate text-sm font-medium">
                      {origem.grupo_origem}
                    </div>
                    <div className="flex-1">
                      <div className="h-8 bg-secondary rounded-lg overflow-hidden">
                        <div 
                          className={`h-full ${color} rounded-lg transition-all flex items-center justify-end px-2`}
                          style={{ width: `${(origem.ganhos / maxGanhos) * 100}%` }}
                        >
                          <span className="text-xs font-bold text-white">
                            {origem.ganhos}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="w-20 text-right">
                      <Badge variant={
                        origem.taxa_conversao >= 25 ? "success" :
                        origem.taxa_conversao >= 15 ? "warning" :
                        "destructive"
                      }>
                        {origem.taxa_conversao}%
                      </Badge>
                    </div>
                    <div className="w-28 text-right">
                      <p className="text-sm font-semibold">{formatCurrency(origem.valor_vendido)}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
