"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/layout/header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MetricCard } from "@/components/dashboard/metric-card";
import {
  Users,
  MessageSquare,
  FileText,
  HandCoins,
  CheckCircle,
  XCircle,
  Archive,
  RefreshCw,
  AlertTriangle,
  Clock,
  LucideIcon,
} from "lucide-react";
import { getCRMFunil, getCRMLeadsParados, getCRMMotivosPerda } from "@/lib/api";

interface FunilData {
  id_state: number;
  etapa: string;
  quantidade: number;
  valor_total: number;
  ticket_medio: number;
}

interface LeadParado {
  id: number;
  veiculo: string;
  nome_cliente: string;
  origem: string;
  vendedor: string;
  estado: number;
  valor: number;
  dias_parado: number;
}

interface MotivoPerda {
  motivo_perda: string;
  quantidade: number;
  percentual: number;
}

const etapaInfo: Record<number, { nome: string; cor: string; Icon: LucideIcon }> = {
  1: { nome: "Novo", cor: "bg-blue-500", Icon: Users },
  2: { nome: "Em Atendimento", cor: "bg-cyan-500", Icon: MessageSquare },
  3: { nome: "Proposta Enviada", cor: "bg-indigo-500", Icon: FileText },
  4: { nome: "Em Negociação", cor: "bg-purple-500", Icon: HandCoins },
  5: { nome: "Fechamento", cor: "bg-amber-500", Icon: Clock },
  6: { nome: "GANHO", cor: "bg-green-500", Icon: CheckCircle },
  7: { nome: "PERDIDO", cor: "bg-red-500", Icon: XCircle },
  8: { nome: "Arquivado", cor: "bg-gray-500", Icon: Archive },
};

export default function FunnelPage() {
  const [funil, setFunil] = useState<FunilData[]>([]);
  const [leadsParados, setLeadsParados] = useState<LeadParado[]>([]);
  const [motivosPerda, setMotivosPerda] = useState<MotivoPerda[]>([]);
  const [loading, setLoading] = useState(true);
  const [diasParados, setDiasParados] = useState(7);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact'
    }).format(value);
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const [funilData, paradosData, motivosData] = await Promise.all([
        getCRMFunil(),
        getCRMLeadsParados(diasParados),
        getCRMMotivosPerda(30)
      ]);
      setFunil(funilData as FunilData[]);
      setLeadsParados(paradosData as LeadParado[]);
      setMotivosPerda(motivosData as MotivoPerda[]);
    } catch (err) {
      console.error('Erro ao carregar funil:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [diasParados]);

  // Separar etapas ativas das finalizadas
  const etapasAtivas = funil.filter(e => e.id_state >= 1 && e.id_state <= 5);
  const totalAtivos = etapasAtivas.reduce((sum, e) => sum + e.quantidade, 0);
  const valorPotencial = etapasAtivas.reduce((sum, e) => sum + (e.valor_total || 0), 0);

  const ganhos = funil.find(e => e.id_state === 6);
  const perdidos = funil.find(e => e.id_state === 7);

  return (
    <>
      <Header title="Funil de Vendas" description="Estado atual do pipeline" />

      <div className="p-6 space-y-6">
        {/* Métricas do Funil */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            label="Leads Ativos"
            value={totalAtivos.toString()}
            icon={Users}
          />
          <MetricCard
            label="Valor Potencial"
            value={formatCurrency(valorPotencial)}
            icon={Clock}
          />
          <MetricCard
            label="Ganhos (Total)"
            value={ganhos?.quantidade.toString() || "0"}
            icon={CheckCircle}
          />
          <MetricCard
            label="Perdidos (Total)"
            value={perdidos?.quantidade.toString() || "0"}
            icon={XCircle}
          />
        </div>

        {/* Funil Visual */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-base font-medium">
              Funil de Vendas
            </CardTitle>
            <button
              onClick={loadData}
              disabled={loading}
              className="flex items-center gap-2 text-sm font-medium text-primary hover:underline disabled:opacity-50"
            >
              <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
              Atualizar
            </button>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Etapas ativas (1-5) */}
              <div className="relative">
                {[1, 2, 3, 4, 5].map((state) => {
                  const etapa = funil.find(e => e.id_state === state);
                  const info = etapaInfo[state];
                  const maxQtd = Math.max(...etapasAtivas.map(e => e.quantidade), 1);
                  const width = etapa ? Math.max((etapa.quantidade / maxQtd) * 100, 20) : 20;
                  const IconComponent = info.Icon;

                  return (
                    <div key={state} className="flex items-center gap-4 mb-3">
                      <div className="w-40 flex items-center gap-2">
                        <IconComponent className="h-4 w-4 text-muted-foreground" />
                        <span className="text-sm font-medium">{info.nome}</span>
                      </div>
                      <div className="flex-1">
                        <div 
                          className={`${info.cor} h-10 rounded-lg flex items-center px-4 transition-all`}
                          style={{ width: `${width}%` }}
                        >
                          <span className="text-white font-bold">
                            {etapa?.quantidade || 0}
                          </span>
                        </div>
                      </div>
                      <div className="w-32 text-right">
                        <p className="text-sm font-medium">
                          {formatCurrency(etapa?.valor_total || 0)}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Separador */}
              <div className="flex items-center gap-4 py-4">
                <div className="flex-1 border-t border-border"></div>
                <span className="text-sm text-muted-foreground">Finalizados</span>
                <div className="flex-1 border-t border-border"></div>
              </div>

              {/* Resultado final */}
              <div className="grid grid-cols-2 gap-4">
                <div className="rounded-xl bg-green-500/10 border border-green-500/30 p-6 text-center">
                  <CheckCircle className="h-8 w-8 mx-auto text-green-500 mb-2" />
                  <p className="text-4xl font-bold text-green-500">
                    {ganhos?.quantidade || 0}
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">Ganhos</p>
                  <p className="text-lg font-medium mt-2">
                    {formatCurrency(ganhos?.valor_total || 0)}
                  </p>
                </div>
                <div className="rounded-xl bg-red-500/10 border border-red-500/30 p-6 text-center">
                  <XCircle className="h-8 w-8 mx-auto text-red-500 mb-2" />
                  <p className="text-4xl font-bold text-red-500">
                    {perdidos?.quantidade || 0}
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">Perdidos</p>
                  <p className="text-lg font-medium mt-2">
                    {formatCurrency(perdidos?.valor_total || 0)}
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Leads Parados */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-base font-medium flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-warning" />
              Leads Parados há mais de {diasParados} dias
            </CardTitle>
            <div className="flex gap-2">
              {[3, 7, 14, 30].map((d) => (
                <button
                  key={d}
                  onClick={() => setDiasParados(d)}
                  className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${
                    diasParados === d 
                      ? 'bg-primary text-primary-foreground' 
                      : 'bg-secondary hover:bg-secondary/80'
                  }`}
                >
                  {d}d
                </button>
              ))}
            </div>
          </CardHeader>
          <CardContent>
            {leadsParados.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                Nenhum lead parado há mais de {diasParados} dias 🎉
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="text-left py-3 px-4 font-medium text-muted-foreground">Veículo</th>
                      <th className="text-left py-3 px-4 font-medium text-muted-foreground">Cliente</th>
                      <th className="text-left py-3 px-4 font-medium text-muted-foreground">Vendedor</th>
                      <th className="text-left py-3 px-4 font-medium text-muted-foreground">Origem</th>
                      <th className="text-right py-3 px-4 font-medium text-muted-foreground">Valor</th>
                      <th className="text-right py-3 px-4 font-medium text-muted-foreground">Dias Parado</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leadsParados.slice(0, 20).map((lead) => (
                      <tr 
                        key={lead.id} 
                        className="border-b border-border/50 hover:bg-secondary/50 transition-colors"
                      >
                        <td className="py-3 px-4">
                          <p className="font-medium truncate max-w-[200px]">{lead.veiculo || 'N/A'}</p>
                        </td>
                        <td className="py-3 px-4 text-sm">{lead.nome_cliente || 'N/A'}</td>
                        <td className="py-3 px-4 text-sm">{lead.vendedor || 'N/A'}</td>
                        <td className="py-3 px-4">
                          <Badge variant="outline">{lead.origem || 'N/A'}</Badge>
                        </td>
                        <td className="py-3 px-4 text-right font-medium">
                          {formatCurrency(lead.valor || 0)}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <Badge variant={
                            lead.dias_parado > 14 ? "destructive" :
                            lead.dias_parado > 7 ? "warning" :
                            "secondary"
                          }>
                            {lead.dias_parado} dias
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {leadsParados.length > 20 && (
                  <p className="text-center py-4 text-sm text-muted-foreground">
                    E mais {leadsParados.length - 20} leads...
                  </p>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Motivos de Perda */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-medium">
              Top Motivos de Perda (últimos 30 dias)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {motivosPerda.slice(0, 10).map((motivo, idx) => (
                <div key={idx} className="flex items-center gap-4">
                  <div className="w-8 h-8 rounded-full bg-red-500/20 flex items-center justify-center text-sm font-bold text-red-500">
                    {idx + 1}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{motivo.motivo_perda || 'Não informado'}</p>
                    <div className="h-2 rounded-full bg-secondary mt-1 overflow-hidden">
                      <div 
                        className="h-full bg-red-500 rounded-full"
                        style={{ width: `${motivo.percentual}%` }}
                      />
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold">{motivo.quantidade}</p>
                    <p className="text-xs text-muted-foreground">{motivo.percentual}%</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
