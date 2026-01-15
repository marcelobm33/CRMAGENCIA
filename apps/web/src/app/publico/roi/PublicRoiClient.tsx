'use client';

import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  DollarSign,
  RefreshCw,
  Target,
  TrendingUp,
  Users,
} from 'lucide-react';

type PublicReport = {
  generated_at: string;
  brand?: string;
  periodo: string;
  roi: {
    investimento_total: number;
    leads_agencia: number;
    leads_crm: number;
    vendas_crm: number;
    valor_vendido: number;
    custo_por_lead_real: number;
    custo_por_venda: number;
    roi_percentual: number;
    meta: { investimento: number; leads_crm: number; vendas: number; valor_vendido: number; roi: number };
    google: { investimento: number; leads_crm: number; vendas: number; valor_vendido: number; roi: number };
  };
  qualidade: {
    resumo_midia: { total_leads: number; ganhos: number; perdidos: number; taxa_conversao: number; custo_por_venda: number };
    leads_frios_percentual: number;
    top_motivos_perda: Array<{ motivo: string; percentual: number }>;
  };
  proposta: {
    decisao: string;
    cobrancas_7_dias: string[];
    realocacao: string[];
    kpis_para_decidir: string[];
  };
};

function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0,
  }).format(value);
}

function formatNumber(value: number): string {
  return new Intl.NumberFormat('pt-BR').format(value);
}

function MetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  color = 'default',
}: {
  title: string;
  value: string;
  subtitle?: string;
  icon?: any;
  color?: 'default' | 'success' | 'warning' | 'danger';
}) {
  const colorClasses: Record<string, string> = {
    default: 'bg-white',
    success: 'bg-emerald-50 border-emerald-200',
    warning: 'bg-amber-50 border-amber-200',
    danger: 'bg-red-50 border-red-200',
  };

  const iconColorClasses: Record<string, string> = {
    default: 'text-gray-600',
    success: 'text-emerald-600',
    warning: 'text-amber-600',
    danger: 'text-red-600',
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
    </div>
  );
}

function ComparisonCard({
  title,
  platform,
  data,
}: {
  title: string;
  platform: 'meta' | 'google';
  data: PublicReport['roi']['meta'] | PublicReport['roi']['google'];
}) {
  const bgColor = platform === 'meta' ? 'from-blue-500 to-indigo-600' : 'from-emerald-500 to-teal-600';
  const lightBg = platform === 'meta' ? 'bg-blue-50' : 'bg-emerald-50';

  return (
    <div className="bg-white rounded-xl border overflow-hidden">
      <div className={`bg-gradient-to-r ${bgColor} px-5 py-4`}>
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        <p className="text-white/80 text-sm">Investimento: {formatCurrency(data.investimento)}</p>
      </div>

      <div className="p-5 space-y-4">
        <div className={`${lightBg} rounded-lg p-4`}>
          <p className="text-xs font-medium text-gray-500 uppercase">Leads (CRM)</p>
          <div className="mt-2 flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Leads</p>
              <p className="text-xl font-semibold">{formatNumber(data.leads_crm)}</p>
            </div>
            <ArrowRight className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-500">Vendas</p>
              <p className="text-xl font-semibold">{formatNumber(data.vendas)}</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase">Valor vendido</p>
            <p className="text-lg font-semibold text-gray-900">{formatCurrency(data.valor_vendido)}</p>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase">ROI</p>
            <p className={`text-2xl font-bold ${data.roi > 100 ? 'text-emerald-600' : 'text-gray-900'}`}>{data.roi.toFixed(0)}%</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function PublicRoiClient() {
  const [report, setReport] = useState<PublicReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const searchParams = useSearchParams();
  const token = searchParams.get('t') ?? '';

  useEffect(() => {
    (async () => {
      try {
        const url = token ? `/public-report.json?t=${encodeURIComponent(token)}` : '/public-report.json';
        const res = await fetch(url, { cache: 'no-store' });
        if (!res.ok) throw new Error('public-report.json não encontrado');
        const data = (await res.json()) as PublicReport;
        setReport(data);
      } catch (e: any) {
        setError(e?.message ?? 'Erro ao carregar relatório');
      }
    })();
  }, [token]);

  const title = useMemo(() => 'ROI & Análise de Performance', []);

  if (error) {
    return (
      <div className="bg-white rounded-2xl border p-6">
        <h1 className="text-xl font-bold text-gray-900">Relatório Público</h1>
        <p className="text-gray-600 mt-2">Erro: {error}</p>
        <p className="text-xs text-gray-400 mt-4">
          Dica: gere o arquivo `public/public-report.json` (use `public-report.example.json` como modelo).
        </p>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="bg-white rounded-2xl border p-6">
        <div className="flex items-center gap-2 text-gray-600">
          <RefreshCw className="w-4 h-4 animate-spin" />
          <span>Carregando…</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header (igual ao dashboard local) */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">{title}</h1>
          <p className="text-gray-500 mt-1">
            Cruzamento de dados: CRM Real vs Agência • <span className="font-medium">Período apurado: {report.periodo}</span>
          </p>
          <p className="text-xs text-gray-400 mt-1">Gerado em {new Date(report.generated_at).toLocaleString('pt-BR')}</p>
        </div>
        <div className="px-3 py-2 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs font-medium">
          Sem dados sensíveis (CRM/telefones/clientes)
        </div>
      </div>

      {/* KPIs (mesma “pegada” do dashboard) */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard title="Investimento Total" value={formatCurrency(report.roi.investimento_total)} subtitle="Mídia paga" icon={DollarSign} />
        <MetricCard title="Leads Agência" value={formatNumber(report.roi.leads_agencia)} subtitle="Reportados" icon={Users} />
        <MetricCard
          title="Leads CRM"
          value={formatNumber(report.roi.leads_crm)}
          subtitle="Entrada real"
          icon={Users}
          color={report.roi.leads_crm < report.roi.leads_agencia * 0.8 ? 'warning' : 'default'}
        />
        <MetricCard
          title="Vendas"
          value={formatNumber(report.roi.vendas_crm)}
          subtitle={formatCurrency(report.roi.valor_vendido)}
          icon={Target}
          color="success"
        />
        <MetricCard
          title="ROI"
          value={`${report.roi.roi_percentual.toFixed(0)}%`}
          subtitle="Retorno/Investimento"
          icon={TrendingUp}
          color={report.roi.roi_percentual > 200 ? 'success' : report.roi.roi_percentual > 100 ? 'default' : 'danger'}
        />
      </div>

      {/* Custos Reais */}
      <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-xl p-6 text-white">
        <h3 className="text-lg font-medium text-gray-300">Custos Reais (baseado no CRM)</h3>
        <div className="mt-4 grid grid-cols-3 gap-8">
          <div>
            <p className="text-sm text-gray-400">Custo por Lead (Real)</p>
            <p className="text-2xl font-semibold text-amber-400">{formatCurrency(report.roi.custo_por_lead_real)}</p>
            <p className="text-xs text-gray-500">baseado no CRM</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Custo por Venda</p>
            <p className="text-2xl font-semibold text-emerald-400">{formatCurrency(report.roi.custo_por_venda)}</p>
            <p className="text-xs text-gray-500">o que realmente importa</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Taxa conversão (mídia)</p>
            <p className="text-2xl font-semibold text-red-300">{report.qualidade.resumo_midia.taxa_conversao.toFixed(1)}%</p>
            <p className="text-xs text-gray-500">ganhos / leads</p>
          </div>
        </div>
      </div>

      {/* Comparativo Meta vs Google (sanitizado) */}
      <div className="grid lg:grid-cols-2 gap-6">
        <ComparisonCard title="META (Facebook/Instagram)" platform="meta" data={report.roi.meta} />
        <ComparisonCard title="GOOGLE Ads" platform="google" data={report.roi.google} />
      </div>

      <div className="bg-white rounded-2xl border overflow-hidden">
        <div className="px-6 py-4 bg-gray-900 text-white">
          <h2 className="text-lg font-bold">Qualidade do Lead (sinal de esforço da equipe)</h2>
        </div>
        <div className="p-6 grid md:grid-cols-3 gap-4">
          <div className="rounded-2xl border p-5 bg-red-50 border-red-100">
            <div className="text-xs font-semibold uppercase text-red-700 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" /> Conversão mídia paga
            </div>
            <div className="mt-2 text-3xl font-bold text-red-700">{report.qualidade.resumo_midia.taxa_conversao}%</div>
            <div className="text-sm text-gray-700 mt-2">
              Perdidos: <strong>{formatNumber(report.qualidade.resumo_midia.perdidos)}</strong> (esforço sem retorno)
            </div>
          </div>
          <div className="rounded-2xl border p-5">
            <div className="text-xs font-semibold uppercase text-gray-500">Leads frios (top 2)</div>
            <div className="mt-2 text-sm text-gray-800 space-y-2">
              {report.qualidade.top_motivos_perda.slice(0, 2).map((m) => (
                <div key={m.motivo} className="flex items-center justify-between gap-2">
                  <span className="truncate">{m.motivo}</span>
                  <span className="font-semibold">{m.percentual}%</span>
                </div>
              ))}
            </div>
            <div className="mt-3 text-xs text-gray-500">
              Leads frios: <strong>{report.qualidade.leads_frios_percentual}%</strong> dos perdidos
            </div>
          </div>
          <div className="rounded-2xl border p-5 bg-emerald-50 border-emerald-100">
            <div className="text-xs font-semibold uppercase text-emerald-700">Custo por venda (CRM)</div>
            <div className="mt-2 text-3xl font-bold text-emerald-700">{formatCurrency(report.roi.custo_por_venda)}</div>
            <div className="mt-2 text-sm text-gray-700">
              Meta: reduzir com <strong>qualificação</strong> + <strong>alta intenção</strong>.
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl border overflow-hidden">
        <div className="px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-700 text-white">
          <h2 className="text-lg font-bold flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5" /> Proposição (o que fazer com a agência)
          </h2>
          <p className="text-white/80 text-sm mt-1">{report.proposta.decisao}</p>
        </div>
        <div className="p-6 grid md:grid-cols-3 gap-4">
          <div className="rounded-2xl border p-5">
            <div className="text-xs font-semibold uppercase text-gray-500">Cobranças (7 dias)</div>
            <ul className="mt-3 text-sm text-gray-800 space-y-2 list-disc pl-5">
              {report.proposta.cobrancas_7_dias.map((x, i) => (
                <li key={i}>{x}</li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border p-5">
            <div className="text-xs font-semibold uppercase text-gray-500">Pra onde ir (estratégia)</div>
            <ul className="mt-3 text-sm text-gray-800 space-y-2 list-disc pl-5">
              {report.proposta.realocacao.map((x, i) => (
                <li key={i}>{x}</li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border p-5">
            <div className="text-xs font-semibold uppercase text-gray-500">KPIs pra decidir manter/cortar</div>
            <ul className="mt-3 text-sm text-gray-800 space-y-2 list-disc pl-5">
              {report.proposta.kpis_para_decidir.map((x, i) => (
                <li key={i}>{x}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="text-center text-xs text-gray-400">
        Este link exige um token (ex.: <span className="font-mono">?t=...</span>). Compartilhe somente com quem deve ver.
      </div>
    </div>
  );
}

