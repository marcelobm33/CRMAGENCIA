'use client';

import { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Users, 
  Target,
  AlertTriangle,
  Lightbulb,
  BarChart3,
  ArrowRight,
  CheckCircle2,
  XCircle,
  Minus,
  RefreshCw
} from 'lucide-react';

interface DashboardData {
  periodo: string;
  periodo_inicio?: string;
  periodo_fim?: string;
  investimento_total: number;
  leads_agencia: number;
  leads_crm: number;
  leads_crm_total: number;
  vendas_crm: number;
  vendas_crm_total: number;
  valor_vendido: number;
  valor_vendido_total: number;
  custo_por_lead_agencia: number;
  custo_por_lead_real: number;
  custo_por_venda: number;
  roi_percentual: number;
  meta: {
    investimento: number;
    leads_agencia: number;
    leads_crm: number;
    leads_instagram: number;
    leads_facebook: number;
    vendas: number;
    vendas_instagram: number;
    vendas_facebook: number;
    valor_vendido: number;
    custo_por_lead: number;
    custo_por_venda: number;
    roi: number;
    alcance: number;
    cliques: number;
  };
  google: {
    investimento: number;
    leads_agencia: number;
    leads_crm: number;
    vendas: number;
    valor_vendido: number;
    custo_por_lead: number;
    custo_por_venda: number;
    roi: number;
    cliques: number;
    whatsapp: number;
  };
  funil: {
    leads_total: number;
    leads_midia: number;
    em_andamento: number;
    ganhos: number;
    ganhos_midia: number;
    perdidos: number;
    taxa_conversao: number;
  };
  alertas: string[];
  insights: string[];
  observacao_agencia?: string;
}

interface VendaDetalhe {
  id: number;
  plataforma: string;
  origem: string;
  canal: string;
  veiculo: string;
  cliente: string;
  vendedor: string;
  valor: number;
  dias: number;
  entrada: string;
  fechamento: string;
}

interface VendasData {
  periodo: string;
  total_vendas: number;
  valor_total: number;
  vendas: VendaDetalhe[];
}

function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

function formatNumber(value: number): string {
  return new Intl.NumberFormat('pt-BR').format(value);
}

function formatDateBR(d: Date): string {
  const dd = String(d.getDate()).padStart(2, '0');
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const yyyy = d.getFullYear();
  return `${dd}/${mm}/${yyyy}`;
}

function MetricCard({ 
  title, 
  value, 
  subtitle,
  icon: Icon,
  trend,
  color = 'default'
}: { 
  title: string; 
  value: string; 
  subtitle?: string;
  icon?: any;
  trend?: 'up' | 'down' | 'neutral';
  color?: 'default' | 'success' | 'warning' | 'danger';
}) {
  const colorClasses = {
    default: 'bg-white',
    success: 'bg-emerald-50 border-emerald-200',
    warning: 'bg-amber-50 border-amber-200',
    danger: 'bg-red-50 border-red-200'
  };

  const iconColorClasses = {
    default: 'text-gray-500',
    success: 'text-emerald-600',
    warning: 'text-amber-600',
    danger: 'text-red-600'
  };

  return (
    <div className={`rounded-xl border p-5 ${colorClasses[color]} transition-all hover:shadow-md`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">{title}</p>
          <p className="mt-2 text-2xl font-semibold text-gray-900">{value}</p>
          {subtitle && <p className="mt-1 text-sm text-gray-500">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={`p-2 rounded-lg bg-gray-100 ${iconColorClasses[color]}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
      {trend && (
        <div className="mt-3 flex items-center gap-1">
          {trend === 'up' && <TrendingUp className="w-4 h-4 text-emerald-500" />}
          {trend === 'down' && <TrendingDown className="w-4 h-4 text-red-500" />}
          {trend === 'neutral' && <Minus className="w-4 h-4 text-gray-400" />}
        </div>
      )}
    </div>
  );
}

function ComparisonCard({
  title,
  platform,
  data,
  color
}: {
  title: string;
  platform: 'meta' | 'google';
  data: any;
  color: string;
}) {
  const bgColor = platform === 'meta' ? 'from-blue-500 to-indigo-600' : 'from-emerald-500 to-teal-600';
  const lightBg = platform === 'meta' ? 'bg-blue-50' : 'bg-emerald-50';
  
  return (
    <div className="bg-white rounded-xl border overflow-hidden">
      <div className={`bg-gradient-to-r ${bgColor} px-5 py-4`}>
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        <p className="text-white/80 text-sm">
          Investimento: {formatCurrency(data.investimento)}
        </p>
      </div>
      
      <div className="p-5 space-y-4">
        {/* Leads Comparison */}
        <div className={`${lightBg} rounded-lg p-4`}>
          <p className="text-xs font-medium text-gray-500 uppercase">Leads</p>
          <div className="mt-2 flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Agência reporta</p>
              <p className="text-xl font-semibold">{formatNumber(data.leads_agencia)}</p>
            </div>
            <ArrowRight className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-500">CRM real</p>
              <p className="text-xl font-semibold">{formatNumber(data.leads_crm)}</p>
            </div>
          </div>
        </div>

        {/* Vendas */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase">Vendas</p>
            <p className="text-2xl font-bold text-gray-900">{data.vendas}</p>
            <p className="text-sm text-gray-500">{formatCurrency(data.valor_vendido)}</p>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase">ROI</p>
            <p className={`text-2xl font-bold ${data.roi > 100 ? 'text-emerald-600' : 'text-gray-900'}`}>
              {data.roi.toFixed(0)}%
            </p>
            <p className="text-sm text-gray-500">retorno</p>
          </div>
        </div>

        {/* Custos */}
        <div className="border-t pt-4 grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs font-medium text-gray-500">Custo/Lead</p>
            <p className="text-lg font-semibold">{formatCurrency(data.custo_por_lead)}</p>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500">Custo/Venda</p>
            <p className="text-lg font-semibold">{formatCurrency(data.custo_por_venda)}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function FunnelVisualization({ funil }: { funil: DashboardData['funil'] }) {
  const total = funil.leads_total || 1;
  
  const stages = [
    { label: 'Leads', value: funil.leads_total, color: 'bg-blue-500', width: '100%' },
    { label: 'Em Andamento', value: funil.em_andamento, color: 'bg-amber-500', width: `${(funil.em_andamento / total) * 100}%` },
    { label: 'Ganhos', value: funil.ganhos, color: 'bg-emerald-500', width: `${(funil.ganhos / total) * 100}%` },
    { label: 'Perdidos', value: funil.perdidos, color: 'bg-red-500', width: `${(funil.perdidos / total) * 100}%` },
  ];

  return (
    <div className="bg-white rounded-xl border p-5">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Funil de Vendas</h3>
      
      <div className="space-y-3">
        {stages.map((stage, index) => (
          <div key={stage.label} className="flex items-center gap-4">
            <div className="w-28 text-sm text-gray-600">{stage.label}</div>
            <div className="flex-1 bg-gray-100 rounded-full h-8 overflow-hidden">
              <div 
                className={`${stage.color} h-full rounded-full flex items-center justify-end pr-3 transition-all duration-500`}
                style={{ width: stage.width, minWidth: stage.value > 0 ? '60px' : '0' }}
              >
                <span className="text-white text-sm font-medium">{formatNumber(stage.value)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 pt-4 border-t">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">Taxa de Conversão</span>
          <span className={`text-2xl font-bold ${funil.taxa_conversao >= 15 ? 'text-emerald-600' : funil.taxa_conversao >= 10 ? 'text-amber-600' : 'text-red-600'}`}>
            {funil.taxa_conversao.toFixed(1)}%
          </span>
        </div>
      </div>
    </div>
  );
}

export default function ROIDashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [vendas, setVendas] = useState<VendasData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState<string>('consolidado');

  const periods = [
    { value: 'consolidado', label: 'Consolidado (01/10/2025 a 14/01/2026)' },
    { value: '2025-10', label: 'Outubro 2025' },
    { value: '2025-11', label: 'Novembro 2025' },
    { value: '2025-12', label: 'Dezembro 2025' },
    { value: '2026-01', label: 'Janeiro 2026 (mês)' },
  ] as const;

  useEffect(() => {
    fetchData();
  }, [selectedPeriod]);

  async function fetchData() {
    setLoading(true);
    try {
      const isConsolidado = selectedPeriod === 'consolidado';
      const dashboardUrl = isConsolidado
        ? 'http://localhost:8000/api/roi/consolidado'
        : `http://localhost:8000/api/roi/dashboard/${selectedPeriod.split('-')[0]}/${selectedPeriod.split('-')[1]}`;

      const vendasUrl = isConsolidado
        ? 'http://localhost:8000/api/roi/vendas/consolidado'
        : `http://localhost:8000/api/roi/vendas/${selectedPeriod.split('-')[0]}/${selectedPeriod.split('-')[1]}`;

      const [dashboardRes, vendasRes] = await Promise.all([
        fetch(dashboardUrl),
        fetch(vendasUrl)
      ]);
      
      if (dashboardRes.ok) {
        const result = await dashboardRes.json();
        setData(result);
      }
      
      if (vendasRes.ok) {
        const vendasResult = await vendasRes.json();
        setVendas(vendasResult);
      }
    } catch (error) {
      console.error('Erro ao buscar dados:', error);
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

  if (!data) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Dados não disponíveis para este período</p>
      </div>
    );
  }

  const isConsolidado = selectedPeriod === 'consolidado';
  const periodoApurado = (() => {
    if (isConsolidado) return data.periodo;
    const [yStr, mStr] = selectedPeriod.split('-');
    const y = Number(yStr);
    const m = Number(mStr);
    const first = new Date(y, m - 1, 1);
    const last = new Date(y, m, 0);
    return `${formatDateBR(first)} a ${formatDateBR(last)}`;
  })();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            ROI & Análise de Performance
          </h1>
          <p className="text-gray-500 mt-1">
            Cruzamento de dados: CRM Real vs Agência • <span className="font-medium">Período apurado (entrada no CRM - date_create): {periodoApurado}</span>
          </p>
          {data.observacao_agencia && (
            <p className="text-xs text-gray-400 mt-1">
              {data.observacao_agencia}
            </p>
          )}
        </div>
        
        <div className="flex items-center gap-3">
          <select 
            value={selectedPeriod}
            onChange={(e) => {
              setSelectedPeriod(e.target.value);
            }}
            className="px-4 py-2 border rounded-lg bg-white text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {periods.map(p => (
              <option key={p.value} value={p.value}>
                {p.label}
              </option>
            ))}
          </select>
          
          <button 
            onClick={fetchData}
            className="p-2 rounded-lg border bg-white hover:bg-gray-50 transition-colors"
          >
            <RefreshCw className="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>

      {/* Alertas */}
      {data.alertas.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5" />
            <div>
              <h3 className="font-medium text-amber-900">Atenção</h3>
              <ul className="mt-1 space-y-1">
                {data.alertas.map((alerta, i) => (
                  <li key={i} className="text-sm text-amber-800">{alerta}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* KPIs Principais */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard
          title="Investimento Total"
          value={formatCurrency(data.investimento_total)}
          subtitle="Mídia paga"
          icon={DollarSign}
        />
        <MetricCard
          title="Leads Agência"
          value={formatNumber(data.leads_agencia)}
          subtitle="Reportados"
          icon={Users}
        />
        <MetricCard
          title="Leads CRM"
          value={formatNumber(data.leads_crm)}
          subtitle="Entrada real"
          icon={Users}
          color={data.leads_crm < data.leads_agencia * 0.8 ? 'warning' : 'default'}
        />
        <MetricCard
          title="Vendas"
          value={formatNumber(data.vendas_crm)}
          subtitle={formatCurrency(data.valor_vendido)}
          icon={Target}
          color="success"
        />
        <MetricCard
          title="ROI"
          value={`${data.roi_percentual.toFixed(0)}%`}
          subtitle="Retorno/Investimento"
          icon={TrendingUp}
          color={data.roi_percentual > 200 ? 'success' : data.roi_percentual > 100 ? 'default' : 'danger'}
        />
      </div>

      {/* Custos Reais */}
      <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-xl p-6 text-white">
        <h3 className="text-lg font-medium text-gray-300">Custos Reais (baseado no CRM)</h3>
        
        <div className="mt-4 grid grid-cols-3 gap-8">
          <div>
            <p className="text-sm text-gray-400">Custo por Lead (Agência)</p>
            <p className="text-2xl font-semibold">{formatCurrency(data.custo_por_lead_agencia)}</p>
            <p className="text-xs text-gray-500">o que a agência calcula</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Custo por Lead (Real)</p>
            <p className="text-2xl font-semibold text-amber-400">{formatCurrency(data.custo_por_lead_real)}</p>
            <p className="text-xs text-gray-500">baseado no CRM</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Custo por Venda</p>
            <p className="text-2xl font-semibold text-emerald-400">{formatCurrency(data.custo_por_venda)}</p>
            <p className="text-xs text-gray-500">o que realmente importa</p>
          </div>
        </div>
      </div>

      {/* Comparativo META vs GOOGLE */}
      <div className="grid lg:grid-cols-2 gap-6">
        <ComparisonCard
          title="META (Facebook/Instagram)"
          platform="meta"
          data={data.meta}
          color="blue"
        />
        <ComparisonCard
          title="GOOGLE Ads"
          platform="google"
          data={data.google}
          color="green"
        />
      </div>

      {/* Funil + Insights */}
      <div className="grid lg:grid-cols-2 gap-6">
        <FunnelVisualization funil={data.funil} />
        
        {/* Insights */}
        <div className="bg-white rounded-xl border p-5">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-5 h-5 text-amber-500" />
            <h3 className="text-lg font-semibold text-gray-900">Insights</h3>
          </div>
          
          {data.insights.length > 0 ? (
            <ul className="space-y-3">
              {data.insights.map((insight, i) => (
                <li key={i} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 mt-0.5 shrink-0" />
                  <span className="text-sm text-gray-700">{insight}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 text-sm">Nenhum insight disponível para este período</p>
          )}
        </div>
      </div>

      {/* Breakdown Instagram vs Facebook */}
      <div className="bg-white rounded-xl border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Detalhamento META (Instagram x Facebook)</h3>
        
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-gradient-to-br from-pink-50 to-purple-50 rounded-xl p-5 border border-pink-100">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-pink-500 to-purple-500 flex items-center justify-center">
                <span className="text-white text-xs font-bold">IG</span>
              </div>
              <span className="font-semibold text-gray-900">Instagram</span>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-500">Leads</p>
                <p className="text-xl font-bold text-gray-900">{data.meta.leads_instagram}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">Vendas</p>
                <p className="text-xl font-bold text-emerald-600">{data.meta.vendas_instagram}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-5 border border-blue-100">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-500 flex items-center justify-center">
                <span className="text-white text-xs font-bold">FB</span>
              </div>
              <span className="font-semibold text-gray-900">Facebook</span>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-500">Leads</p>
                <p className="text-xl font-bold text-gray-900">{data.meta.leads_facebook}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">Vendas</p>
                <p className="text-xl font-bold text-emerald-600">{data.meta.vendas_facebook}</p>
              </div>
            </div>
          </div>
        </div>
        
        <p className="mt-4 text-sm text-gray-500">
          * Considera tanto a origem quanto o canal para atribuição. Um cliente que veio pelo Instagram 
          mas entrou via Showroom é contabilizado como Instagram.
        </p>
      </div>

      {/* Vendas Detalhadas */}
      {vendas && vendas.vendas.length > 0 && (
        <div className="bg-white rounded-xl border overflow-hidden">
          <div className="px-6 py-4 border-b bg-emerald-50">
            <h3 className="text-lg font-semibold text-emerald-900">
              Vendas de Mídia Paga - {vendas.total_vendas} veículos
            </h3>
            <p className="text-sm text-emerald-700">
              Total: {formatCurrency(vendas.valor_total)}
            </p>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">#ID</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Plataforma</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Veículo</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vendedor</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Valor</th>
                  <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Dias</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {vendas.vendas.map((venda) => (
                  <tr key={venda.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-600">#{venda.id}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        venda.plataforma === 'INSTAGRAM' ? 'bg-pink-100 text-pink-800' :
                        venda.plataforma === 'FACEBOOK' ? 'bg-blue-100 text-blue-800' :
                        'bg-emerald-100 text-emerald-800'
                      }`}>
                        {venda.plataforma}
                      </span>
                      {venda.origem !== venda.plataforma && (
                        <span className="ml-1 text-xs text-gray-400">via {venda.canal}</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900 max-w-xs truncate">
                      {venda.veiculo}
                    </td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-700">{venda.vendedor}</td>
                    <td className="px-4 py-3 text-sm font-semibold text-gray-900 text-right">
                      {formatCurrency(venda.valor)}
                    </td>
                    <td className="px-4 py-3 text-sm text-center">
                      <span className={`font-medium ${venda.dias <= 1 ? 'text-emerald-600' : venda.dias <= 7 ? 'text-amber-600' : 'text-red-600'}`}>
                        {venda.dias}d
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Resumo Executivo */}
      <div className="bg-white rounded-xl border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Resumo Executivo</h3>
        
        <div className="prose prose-sm max-w-none text-gray-600">
          <p>
            Em <strong>{data.periodo}</strong>, foram investidos <strong>{formatCurrency(data.investimento_total)}</strong> em 
            mídia paga, gerando <strong>{formatNumber(data.leads_crm)}</strong> leads de mídia no CRM 
            (de um total de <strong>{formatNumber(data.funil.leads_total)}</strong> leads), 
            dos quais <strong>{formatNumber(data.vendas_crm)}</strong> foram convertidos em vendas, 
            totalizando <strong>{formatCurrency(data.valor_vendido)}</strong> em faturamento.
          </p>
          
          <p className="mt-3">
            O custo real por venda foi de <strong>{formatCurrency(data.custo_por_venda)}</strong>, 
            com um ROI de <strong>{data.roi_percentual.toFixed(0)}%</strong> 
            {data.roi_percentual > 100 
              ? ' - resultado positivo, cada R$1 investido retornou R$' + (data.roi_percentual / 100).toFixed(2)
              : ' - abaixo do esperado, necessário otimização'
            }.
          </p>
          
          {data.meta.roi > data.google.roi && data.meta.vendas > 0 && (
            <p className="mt-3">
              <strong>META (Facebook/Instagram)</strong> apresentou melhor performance com ROI de{' '}
              <strong>{data.meta.roi.toFixed(0)}%</strong>, gerando {data.meta.vendas} vendas 
              (Instagram: {data.meta.vendas_instagram}, Facebook: {data.meta.vendas_facebook}).
            </p>
          )}
          
          {data.google.roi > data.meta.roi && data.google.vendas > 0 && (
            <p className="mt-3">
              <strong>Google Ads</strong> apresentou melhor performance com ROI de{' '}
              <strong>{data.google.roi.toFixed(0)}%</strong> vs{' '}
              <strong>{data.meta.roi.toFixed(0)}%</strong> do Meta, 
              sugerindo possível realocação de budget.
            </p>
          )}
          
          <p className="mt-3">
            <strong>Nota importante:</strong> O mês atual considera origem E canal como fonte de mídia.
            Isso inclui clientes que vieram pelo showroom mas descobriram a loja pelo Instagram/Facebook/Google.
          </p>
        </div>
      </div>
    </div>
  );
}
