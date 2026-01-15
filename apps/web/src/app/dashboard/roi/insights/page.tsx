'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  ArrowLeft,
  Lightbulb, 
  AlertTriangle, 
  TrendingUp,
  TrendingDown,
  Target,
  Users,
  DollarSign,
  CheckCircle2,
  Clock,
  ArrowRight,
  RefreshCw,
  Star,
  Zap
} from 'lucide-react';

interface Insight {
  tipo: 'oportunidade' | 'alerta' | 'info';
  titulo: string;
  descricao: string;
  impacto: string;
}

interface Recomendacao {
  acao: string;
  expectativa: string;
  prioridade: 'alta' | 'media' | 'baixa';
}

interface InsightsData {
  periodo: string;
  insights: Insight[];
  recomendacoes: Recomendacao[];
  dados: {
    por_origem: any[];
    por_vendedor: any[];
    motivos_perda: any[];
    resumo_mes: any;
  };
}

function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

function PriorityBadge({ priority }: { priority: string }) {
  const colors = {
    alta: 'bg-red-100 text-red-700 border-red-200',
    media: 'bg-amber-100 text-amber-700 border-amber-200',
    baixa: 'bg-blue-100 text-blue-700 border-blue-200'
  };
  
  return (
    <span className={`px-2 py-0.5 text-xs font-medium rounded-full border ${colors[priority as keyof typeof colors] || colors.baixa}`}>
      {priority.toUpperCase()}
    </span>
  );
}

function InsightCard({ insight }: { insight: Insight }) {
  const icons = {
    oportunidade: <TrendingUp className="w-5 h-5 text-emerald-600" />,
    alerta: <AlertTriangle className="w-5 h-5 text-amber-600" />,
    info: <Lightbulb className="w-5 h-5 text-blue-600" />
  };

  const bgColors = {
    oportunidade: 'bg-emerald-50 border-emerald-200',
    alerta: 'bg-amber-50 border-amber-200',
    info: 'bg-blue-50 border-blue-200'
  };

  return (
    <div className={`rounded-xl border p-5 ${bgColors[insight.tipo]}`}>
      <div className="flex items-start gap-4">
        <div className="p-2 bg-white rounded-lg shadow-sm">
          {icons[insight.tipo]}
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900">{insight.titulo}</h4>
          <p className="mt-1 text-sm text-gray-600">{insight.descricao}</p>
          <p className="mt-2 text-sm font-medium text-gray-800">
            💡 {insight.impacto}
          </p>
        </div>
      </div>
    </div>
  );
}

export default function InsightsPage() {
  const [data, setData] = useState<InsightsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedMonth, setSelectedMonth] = useState({ ano: 2025, mes: 12 });

  useEffect(() => {
    fetchData();
  }, [selectedMonth]);

  async function fetchData() {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/roi/insights/${selectedMonth.ano}/${selectedMonth.mes}`
      );
      if (response.ok) {
        const result = await response.json();
        setData(result);
      }
    } catch (error) {
      console.error('Erro:', error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <RefreshCw className="w-8 h-8 animate-spin text-gray-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link 
            href="/dashboard/roi"
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-gray-600" />
          </Link>
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">
              Insights & Recomendações
            </h1>
            <p className="text-gray-500 mt-1">
              Análise detalhada e ações sugeridas
            </p>
          </div>
        </div>
        
        <select 
          value={`${selectedMonth.ano}-${selectedMonth.mes}`}
          onChange={(e) => {
            const [ano, mes] = e.target.value.split('-').map(Number);
            setSelectedMonth({ ano, mes });
          }}
          className="px-4 py-2 border rounded-lg bg-white text-sm font-medium"
        >
          <option value="2025-10">Outubro 2025</option>
          <option value="2025-11">Novembro 2025</option>
          <option value="2025-12">Dezembro 2025</option>
        </select>
      </div>

      {/* Insights */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-amber-500" />
          Insights Identificados
        </h2>
        
        <div className="grid gap-4">
          {data?.insights.map((insight, i) => (
            <InsightCard key={i} insight={insight} />
          ))}
          
          {(!data?.insights || data.insights.length === 0) && (
            <div className="text-center py-8 text-gray-500">
              Nenhum insight disponível para este período
            </div>
          )}
        </div>
      </div>

      {/* Recomendações */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Target className="w-5 h-5 text-blue-500" />
          Plano de Ação
        </h2>
        
        <div className="bg-white rounded-xl border divide-y">
          {data?.recomendacoes.map((rec, i) => (
            <div key={i} className="p-5 flex items-start gap-4">
              <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-bold text-sm shrink-0">
                {i + 1}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-3">
                  <h4 className="font-medium text-gray-900">{rec.acao}</h4>
                  <PriorityBadge priority={rec.prioridade} />
                </div>
                <p className="mt-1 text-sm text-gray-500">{rec.expectativa}</p>
              </div>
              <button className="px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                Iniciar
              </button>
            </div>
          ))}
          
          {(!data?.recomendacoes || data.recomendacoes.length === 0) && (
            <div className="text-center py-8 text-gray-500">
              Nenhuma recomendação disponível
            </div>
          )}
        </div>
      </div>

      {/* Dados Detalhados */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Top Vendedores */}
        <div className="bg-white rounded-xl border p-5">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-gray-400" />
            Performance por Vendedor
          </h3>
          
          <div className="space-y-3">
            {data?.dados.por_vendedor?.slice(0, 5).map((v, i) => (
              <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  {i === 0 && <Star className="w-4 h-4 text-amber-500" />}
                  <span className="font-medium text-gray-900">{v.vendedor || 'N/A'}</span>
                </div>
                <div className="flex items-center gap-4 text-sm">
                  <span className="text-gray-500">{v.total_leads} leads</span>
                  <span className="font-medium text-emerald-600">{v.ganhos} vendas</span>
                  <span className="text-gray-400">{v.taxa_conversao}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Motivos de Perda */}
        <div className="bg-white rounded-xl border p-5">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingDown className="w-5 h-5 text-red-400" />
            Principais Motivos de Perda
          </h3>
          
          <div className="space-y-3">
            {data?.dados.motivos_perda?.slice(0, 5).map((m, i) => (
              <div key={i} className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                <span className="text-sm text-gray-700">{m.motivo_perda || 'Não informado'}</span>
                <div className="flex items-center gap-3">
                  <span className="text-sm font-medium text-gray-900">{m.quantidade}</span>
                  <span className="text-xs text-gray-500">{m.percentual}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Resumo por Origem */}
      <div className="bg-white rounded-xl border p-5">
        <h3 className="font-semibold text-gray-900 mb-4">Performance por Origem</h3>
        
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4 font-medium text-gray-500">Origem</th>
                <th className="text-right py-3 px-4 font-medium text-gray-500">Leads</th>
                <th className="text-right py-3 px-4 font-medium text-gray-500">Vendas</th>
                <th className="text-right py-3 px-4 font-medium text-gray-500">Perdidos</th>
                <th className="text-right py-3 px-4 font-medium text-gray-500">Valor</th>
                <th className="text-right py-3 px-4 font-medium text-gray-500">Conversão</th>
              </tr>
            </thead>
            <tbody>
              {data?.dados.por_origem?.map((o, i) => (
                <tr key={i} className="border-b last:border-0 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium text-gray-900">{o.grupo_origem}</td>
                  <td className="py-3 px-4 text-right text-gray-600">{o.total_leads}</td>
                  <td className="py-3 px-4 text-right font-medium text-emerald-600">{o.ganhos}</td>
                  <td className="py-3 px-4 text-right text-red-500">{o.perdidos}</td>
                  <td className="py-3 px-4 text-right text-gray-900">{formatCurrency(o.valor_vendido || 0)}</td>
                  <td className="py-3 px-4 text-right">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                      o.taxa_conversao >= 20 ? 'bg-emerald-100 text-emerald-700' :
                      o.taxa_conversao >= 10 ? 'bg-amber-100 text-amber-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {o.taxa_conversao}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
