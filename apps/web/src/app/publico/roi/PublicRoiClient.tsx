'use client';

import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { AlertTriangle, TrendingUp, Users, DollarSign, Target, CheckCircle2 } from 'lucide-react';

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

  const title = useMemo(() => 'Relatório Público', []);

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
        <p className="text-gray-600">Carregando…</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl border p-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
            <p className="text-gray-600 mt-1">
              <strong>Período apurado:</strong> {report.periodo}
            </p>
            <p className="text-xs text-gray-400 mt-2">Gerado em {new Date(report.generated_at).toLocaleString('pt-BR')}</p>
          </div>
          <div className="px-3 py-2 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs font-medium">
            Sem dados sensíveis (CRM/telefones/clientes)
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl border p-5">
          <div className="flex items-center gap-2 text-gray-500 text-xs font-semibold uppercase">
            <DollarSign className="w-4 h-4" /> Investimento
          </div>
          <div className="mt-2 text-2xl font-bold text-gray-900">{formatCurrency(report.roi.investimento_total)}</div>
        </div>
        <div className="bg-white rounded-2xl border p-5">
          <div className="flex items-center gap-2 text-gray-500 text-xs font-semibold uppercase">
            <Users className="w-4 h-4" /> Leads (CRM)
          </div>
          <div className="mt-2 text-2xl font-bold text-gray-900">{formatNumber(report.roi.leads_crm)}</div>
        </div>
        <div className="bg-white rounded-2xl border p-5">
          <div className="flex items-center gap-2 text-gray-500 text-xs font-semibold uppercase">
            <Target className="w-4 h-4" /> Vendas (CRM)
          </div>
          <div className="mt-2 text-2xl font-bold text-gray-900">{formatNumber(report.roi.vendas_crm)}</div>
        </div>
        <div className="bg-white rounded-2xl border p-5">
          <div className="flex items-center gap-2 text-gray-500 text-xs font-semibold uppercase">
            <TrendingUp className="w-4 h-4" /> ROI
          </div>
          <div className="mt-2 text-2xl font-bold text-emerald-700">{report.roi.roi_percentual.toFixed(0)}%</div>
        </div>
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

