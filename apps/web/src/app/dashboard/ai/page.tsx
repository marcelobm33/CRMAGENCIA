"use client";

import { useState } from "react";
import { Header } from "@/components/layout/header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatDateTime } from "@/lib/utils";
import {
  Zap,
  AlertTriangle,
  TrendingUp,
  CheckCircle,
  Clock,
  XCircle,
  ChevronDown,
  ChevronUp,
  Play,
  Filter,
} from "lucide-react";

// Dados mock
const mockRecommendations = [
  {
    id: "1",
    data: "2024-01-20T14:30:00",
    escopo: "atendimento",
    prioridade: "critical",
    titulo: "42% dos leads perdidos por 'cliente não retornou'",
    insight: "Quase metade das perdas são por falta de retorno do cliente, indicando possível problema no follow-up.",
    explicacao: "Quando o cliente não retorna, pode significar que o contato inicial demorou muito, que o follow-up não foi feito, ou que o interesse esfriou.",
    acoes_sugeridas: [
      { acao: "Implementar SLA de primeira resposta (máx 30 min)", tipo: "imediata" },
      { acao: "Criar sequência de follow-up automatizada", tipo: "otimizacao" },
      { acao: "Treinar equipe em técnicas de reativação", tipo: "analise" },
    ],
    hipotese: "Com SLA de atendimento, podemos recuperar 30% desses leads",
    metrica_alvo: "Taxa de resposta",
    impacto_esperado: "5-10 vendas adicionais por mês",
    como_medir: "Monitorar tempo de primeira resposta e taxa de conversão",
    status: "pending",
  },
  {
    id: "2",
    data: "2024-01-20T14:30:00",
    escopo: "campanha",
    prioridade: "high",
    titulo: "CPL elevado na campanha 'Busca - Financiamento'",
    insight: "O CPL desta campanha está 120% acima da média (R$ 102 vs R$ 46).",
    explicacao: "Um CPL muito alto indica problemas com segmentação ou landing page. A campanha não gerou vendas nos últimos 30 dias.",
    acoes_sugeridas: [
      { acao: "Pausar campanha imediatamente", tipo: "imediata" },
      { acao: "Revisar palavras-chave negativas", tipo: "analise" },
      { acao: "Testar nova landing page", tipo: "teste" },
    ],
    hipotese: "Pausando e otimizando, podemos economizar R$ 1.300/mês",
    metrica_alvo: "CPL",
    impacto_esperado: "Redução de 60% no CPL ou economia do orçamento",
    como_medir: "Comparar CPL após reativação",
    status: "in_progress",
  },
  {
    id: "3",
    data: "2024-01-20T14:30:00",
    escopo: "orcamento",
    prioridade: "medium",
    titulo: "Oportunidade: campanha 'Remarketing - Visitantes' com CPL baixo",
    insight: "Esta campanha Meta tem CPL de R$ 23,21, 50% abaixo da média.",
    explicacao: "Campanhas com boa performance são oportunidades de escala. O público de remarketing está convertendo bem.",
    acoes_sugeridas: [
      { acao: "Aumentar orçamento em 30%", tipo: "otimizacao" },
      { acao: "Monitorar se CPL se mantém após aumento", tipo: "analise" },
    ],
    hipotese: "Escalando a campanha, podemos gerar mais 8-10 leads/semana",
    metrica_alvo: "Volume de leads",
    impacto_esperado: "32-40 leads adicionais por mês",
    como_medir: "Acompanhar CPL e volume diário",
    status: "pending",
  },
  {
    id: "4",
    data: "2024-01-19T10:00:00",
    escopo: "crm",
    prioridade: "high",
    titulo: "Vendedor 'João Oliveira' com taxa de conversão crítica: 6.25%",
    insight: "João tem taxa 78% menor que a média da equipe (29%).",
    explicacao: "Diferenças tão grandes podem indicar problemas de atendimento, leads mal distribuídos, ou necessidade de treinamento.",
    acoes_sugeridas: [
      { acao: "Acompanhar atendimentos do vendedor", tipo: "analise" },
      { acao: "Mentoria com Carlos Silva (top performer)", tipo: "otimizacao" },
      { acao: "Revisar distribuição de leads", tipo: "analise" },
    ],
    hipotese: "Com treinamento, João pode dobrar sua conversão",
    metrica_alvo: "Taxa de conversão por vendedor",
    impacto_esperado: "3-5 vendas adicionais por mês",
    como_medir: "Comparar taxa de conversão mensal",
    status: "pending",
  },
  {
    id: "5",
    data: "2024-01-18T16:00:00",
    escopo: "criativo",
    prioridade: "low",
    titulo: "Teste A/B sugerido: criativos de Stories",
    insight: "Criativos de Stories no Meta têm CTR 2x maior que feed.",
    explicacao: "Formatos com alto engajamento merecem mais investimento e testes.",
    acoes_sugeridas: [
      { acao: "Criar 3 novos criativos formato Stories", tipo: "teste" },
      { acao: "Testar diferentes CTAs", tipo: "teste" },
    ],
    hipotese: "Novos criativos podem aumentar CTR em 20%",
    metrica_alvo: "CTR Stories",
    impacto_esperado: "Mais cliques com mesmo investimento",
    como_medir: "Comparar CTR antes e depois",
    status: "done",
  },
];

const statusConfig = {
  pending: { label: "Pendente", icon: Clock, color: "warning" },
  in_progress: { label: "Em Andamento", icon: Play, color: "secondary" },
  done: { label: "Concluído", icon: CheckCircle, color: "success" },
  dismissed: { label: "Descartado", icon: XCircle, color: "destructive" },
};

const prioridadeConfig = {
  critical: { label: "Crítico", color: "destructive" },
  high: { label: "Alta", color: "warning" },
  medium: { label: "Média", color: "secondary" },
  low: { label: "Baixa", color: "outline" },
};

export default function AIPage() {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [filterStatus, setFilterStatus] = useState<string | null>(null);

  const filteredRecommendations = filterStatus
    ? mockRecommendations.filter((r) => r.status === filterStatus)
    : mockRecommendations;

  const pendentes = mockRecommendations.filter((r) => r.status === "pending").length;
  const criticos = mockRecommendations.filter((r) => r.prioridade === "critical" && r.status === "pending").length;

  return (
    <>
      <Header title="IA Analista" description="Insights e recomendações automatizadas" />

      <div className="p-6 space-y-6">
        {/* Resumo */}
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardContent className="flex items-center gap-4 p-4">
              <div className="rounded-full bg-primary/20 p-3">
                <Zap className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total de Insights</p>
                <p className="text-2xl font-bold">{mockRecommendations.length}</p>
              </div>
            </CardContent>
          </Card>
          <Card className={criticos > 0 ? "border-destructive/50" : ""}>
            <CardContent className="flex items-center gap-4 p-4">
              <div className="rounded-full bg-destructive/20 p-3">
                <AlertTriangle className="h-5 w-5 text-destructive" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Críticos Pendentes</p>
                <p className="text-2xl font-bold">{criticos}</p>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="flex items-center gap-4 p-4">
              <div className="rounded-full bg-warning/20 p-3">
                <Clock className="h-5 w-5 text-warning" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Pendentes</p>
                <p className="text-2xl font-bold">{pendentes}</p>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="flex items-center gap-4 p-4">
              <div className="rounded-full bg-success/20 p-3">
                <TrendingUp className="h-5 w-5 text-success" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Oportunidades</p>
                <p className="text-2xl font-bold">
                  {mockRecommendations.filter((r) => r.escopo === "orcamento").length}
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Ações */}
        <div className="flex items-center justify-between">
          <div className="flex gap-2">
            <Button
              variant={filterStatus === null ? "default" : "outline"}
              size="sm"
              onClick={() => setFilterStatus(null)}
            >
              Todos
            </Button>
            <Button
              variant={filterStatus === "pending" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilterStatus("pending")}
            >
              Pendentes
            </Button>
            <Button
              variant={filterStatus === "in_progress" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilterStatus("in_progress")}
            >
              Em Andamento
            </Button>
            <Button
              variant={filterStatus === "done" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilterStatus("done")}
            >
              Concluídos
            </Button>
          </div>
          <Button>
            <Zap className="h-4 w-4 mr-2" />
            Gerar Nova Análise
          </Button>
        </div>

        {/* Lista de recomendações */}
        <div className="space-y-4">
          {filteredRecommendations.map((rec) => {
            const isExpanded = expandedId === rec.id;
            const StatusIcon = statusConfig[rec.status as keyof typeof statusConfig].icon;
            
            return (
              <Card
                key={rec.id}
                className={
                  rec.prioridade === "critical" && rec.status === "pending"
                    ? "border-destructive/50"
                    : ""
                }
              >
                <CardHeader className="pb-2">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3 flex-1">
                      <Badge variant={prioridadeConfig[rec.prioridade as keyof typeof prioridadeConfig].color as any}>
                        {prioridadeConfig[rec.prioridade as keyof typeof prioridadeConfig].label}
                      </Badge>
                      <div className="flex-1">
                        <CardTitle className="text-base font-medium">{rec.titulo}</CardTitle>
                        <p className="text-sm text-muted-foreground mt-1">{rec.insight}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline">{rec.escopo}</Badge>
                      <Badge variant={statusConfig[rec.status as keyof typeof statusConfig].color as any}>
                        <StatusIcon className="h-3 w-3 mr-1" />
                        {statusConfig[rec.status as keyof typeof statusConfig].label}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-muted-foreground">
                      Gerado em {formatDateTime(rec.data)}
                    </p>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setExpandedId(isExpanded ? null : rec.id)}
                    >
                      {isExpanded ? (
                        <>
                          Menos detalhes
                          <ChevronUp className="h-4 w-4 ml-1" />
                        </>
                      ) : (
                        <>
                          Ver detalhes
                          <ChevronDown className="h-4 w-4 ml-1" />
                        </>
                      )}
                    </Button>
                  </div>

                  {isExpanded && (
                    <div className="mt-4 pt-4 border-t border-border space-y-4 animate-fade-in">
                      <div>
                        <h4 className="font-medium text-sm mb-2">O que isso significa</h4>
                        <p className="text-sm text-muted-foreground">{rec.explicacao}</p>
                      </div>

                      <div>
                        <h4 className="font-medium text-sm mb-2">Ações Sugeridas</h4>
                        <ul className="space-y-2">
                          {rec.acoes_sugeridas.map((acao, i) => (
                            <li key={i} className="flex items-center gap-2 text-sm">
                              <Badge variant="outline" className="text-xs">
                                {acao.tipo}
                              </Badge>
                              {acao.acao}
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="grid gap-4 md:grid-cols-2">
                        <div>
                          <h4 className="font-medium text-sm mb-1">Hipótese</h4>
                          <p className="text-sm text-muted-foreground">{rec.hipotese}</p>
                        </div>
                        <div>
                          <h4 className="font-medium text-sm mb-1">Impacto Esperado</h4>
                          <p className="text-sm text-muted-foreground">{rec.impacto_esperado}</p>
                        </div>
                      </div>

                      <div>
                        <h4 className="font-medium text-sm mb-1">Como Medir</h4>
                        <p className="text-sm text-muted-foreground">{rec.como_medir}</p>
                      </div>

                      {rec.status === "pending" && (
                        <div className="flex gap-2 pt-2">
                          <Button size="sm">Iniciar</Button>
                          <Button size="sm" variant="outline">
                            Marcar como Feito
                          </Button>
                          <Button size="sm" variant="ghost">
                            Descartar
                          </Button>
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </>
  );
}

