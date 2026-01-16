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
  ShieldAlert,
  Scale,
  Flame,
  BarChart3,
  Send,
  Zap,
} from 'lucide-react';

type PublicReport = {
  generated_at: string;
  periodo: string;
  nota?: string;
  investimento: {
    total: number;
    lead: number;
    branding: number;
    meta_total: number;
    meta_lead: number;
    google_total: number;
    google_lead: number;
  };
  crm: {
    total_leads: number;
    total_vendas: number;
    total_valor: number;
    midia_paga: {
      leads: number;
      vendas: number;
      valor: number;
      taxa_conversao: number;
    };
    outras_fontes: {
      leads: number;
      vendas: number;
      valor: number;
      taxa_conversao: number;
    };
  };
  atribuicao_indireta?: {
    percentual: number;
    fontes: string[];
    detalhes: {
      showroom: { vendas_total: number; atribuido: number; valor: number };
      indicacao: { vendas_total: number; atribuido: number; valor: number };
      rede_relacionamento: { vendas_total: number; atribuido: number; valor: number };
    };
    total_vendas_atribuidas: number;
    total_valor_atribuido: number;
  };
  roi: {
    investimento_lead: number;
    vendas_diretas?: number;
    vendas_atribuidas?: number;
    vendas_totais?: number;
    vendas_midia?: number;
    valor_direto?: number;
    valor_atribuido?: number;
    valor_total?: number;
    valor_vendido?: number;
    cpv_direto?: number;
    cpv_com_atribuicao?: number;
    cpv_total?: number;
    roi_direto?: number;
    roi_com_atribuicao?: number;
    roi_percentual?: number;
    google: {
      investimento_lead: number;
      leads_crm: number;
      vendas: number;
      valor_vendido: number;
      cpv: number;
      roi: number;
      taxa_conversao: number;
    };
    meta: {
      investimento_lead: number;
      leads_crm: number;
      vendas: number;
      valor_vendido: number;
      cpv: number;
      roi: number;
      taxa_conversao: number;
    };
  };
  auditoria: {
    cpv_proposto: number;
    cpv_real?: number;
    cpv_real_direto?: number;
    cpv_real_com_atribuicao?: number;
    diferenca_cpv: string;
    validacao: string;
    melhoria_com_atribuicao?: {
      reducao_cpv: string;
      aumento_roi: string;
    };
    eficiencia_comparativa: {
      google_vs_meta_cpv: string;
      google_vs_meta_roi: string;
      google_vs_meta_conversao: string;
    };
  };
  qualidade: {
    midia_paga: {
      total_leads: number;
      vendas: number;
      perdidos: number;
      taxa_conversao: number;
    };
    google_via_site?: {
      leads: number;
      vendas: number;
      taxa_conversao: number;
      melhor_fonte: boolean;
    };
    comparativo_outras_fontes: {
      showroom: { leads: number; vendas: number; taxa: number };
      oferta_vendedor: { leads: number; vendas: number; taxa: number };
      indicacao: { leads: number; vendas: number; taxa: number };
    };
    insight: string;
  };
  proposta: {
    decisao: string;
    cobrancas_7_dias: string[];
    realocacao: string[];
    vendas_esperadas_novo_mix: {
      google: number;
      meta: number;
      total_mes: number;
      aumento_vs_atual: string;
    };
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

  return (
    <div className={`rounded-xl border p-5 ${colorClasses[color]} transition-all hover:shadow-md`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">{title}</p>
          <p className="mt-2 text-2xl font-semibold text-gray-900">{value}</p>
          {subtitle && <p className="mt-1 text-sm text-gray-500">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={`p-2 rounded-lg bg-gray-100`}>
            <Icon className="w-5 h-5 text-gray-600" />
          </div>
        )}
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

  if (error) {
    return (
      <div className="bg-white rounded-2xl border p-6">
        <h1 className="text-xl font-bold text-gray-900">Relatório Público</h1>
        <p className="text-gray-600 mt-2">Erro: {error}</p>
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
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">ROI & Análise de Performance</h1>
          <p className="text-gray-500 mt-1">
            Análise LEAD vs BRANDING • <span className="font-medium">Período: {report.periodo}</span>
          </p>
          <p className="text-xs text-gray-400 mt-1">
            {report.nota} • Gerado em {new Date(report.generated_at).toLocaleString('pt-BR')}
          </p>
        </div>
        <div className="px-3 py-2 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs font-medium">
          Relatório Público (sem dados sensíveis)
        </div>
      </div>

      {/* Visão Geral CRM */}
      <div className="bg-gradient-to-r from-slate-800 to-slate-700 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-4">
          <BarChart3 className="w-5 h-5 text-slate-300" />
          <h3 className="text-lg font-semibold text-white">📊 Visão Geral CRM (TODOS os Leads)</h3>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-xs text-slate-300 uppercase">Total Leads</p>
            <p className="text-3xl font-bold text-white">{formatNumber(report.crm.total_leads)}</p>
            <p className="text-xs text-slate-400 mt-1">Todas as origens</p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-xs text-slate-300 uppercase">Total Vendas</p>
            <p className="text-3xl font-bold text-emerald-400">{formatNumber(report.crm.total_vendas)}</p>
            <p className="text-xs text-slate-400 mt-1">{formatCurrency(report.crm.total_valor)}</p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-xs text-slate-300 uppercase">Taxa Conversão Geral</p>
            <p className="text-3xl font-bold text-blue-400">
              {((report.crm.total_vendas / report.crm.total_leads) * 100).toFixed(1)}%
            </p>
            <p className="text-xs text-slate-400 mt-1">Vendas ÷ Leads</p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-xs text-slate-300 uppercase">Leads Mídia Paga</p>
            <p className="text-3xl font-bold text-amber-400">{formatNumber(report.crm.midia_paga.leads)}</p>
            <p className="text-xs text-slate-400 mt-1">
              {((report.crm.midia_paga.leads / report.crm.total_leads) * 100).toFixed(0)}% do total
            </p>
          </div>
        </div>
      </div>

      {/* Investimento LEAD vs BRANDING */}
      <div className="bg-white rounded-xl border overflow-hidden">
        <div className="px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600">
          <h3 className="text-lg font-semibold text-white">💰 Investimento: LEAD vs BRANDING</h3>
        </div>
        <div className="p-6 grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="rounded-xl border-2 border-gray-200 p-4">
            <p className="text-xs font-medium text-gray-500 uppercase">Total Investido</p>
            <p className="text-2xl font-bold text-gray-900">{formatCurrency(report.investimento.total)}</p>
            <p className="text-xs text-gray-500 mt-1">Out + Nov + Dez</p>
          </div>
          <div className="rounded-xl border-2 border-emerald-200 bg-emerald-50 p-4">
            <p className="text-xs font-medium text-emerald-600 uppercase">Campanhas LEAD</p>
            <p className="text-2xl font-bold text-emerald-700">{formatCurrency(report.investimento.lead)}</p>
            <p className="text-xs text-emerald-600 mt-1">
              {((report.investimento.lead / report.investimento.total) * 100).toFixed(0)}% do total
            </p>
          </div>
          <div className="rounded-xl border-2 border-amber-200 bg-amber-50 p-4">
            <p className="text-xs font-medium text-amber-600 uppercase">Campanhas BRANDING</p>
            <p className="text-2xl font-bold text-amber-700">{formatCurrency(report.investimento.branding)}</p>
            <p className="text-xs text-amber-600 mt-1">
              {((report.investimento.branding / report.investimento.total) * 100).toFixed(0)}% do total
            </p>
          </div>
          <div className="rounded-xl border-2 border-blue-200 bg-blue-50 p-4">
            <p className="text-xs font-medium text-blue-600 uppercase">Vendas Totais (Mídia)</p>
            <p className="text-2xl font-bold text-blue-700">{formatNumber(report.roi.vendas_totais || report.roi.vendas_midia || 0)}</p>
            <p className="text-xs text-blue-600 mt-1">{formatCurrency(report.roi.valor_total || report.roi.valor_vendido || 0)}</p>
          </div>
        </div>
      </div>

      {/* Atribuição Indireta */}
      {report.atribuicao_indireta && (
        <div className="bg-gradient-to-r from-purple-900 to-indigo-900 rounded-xl p-6 text-white">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-purple-300" />
            <h3 className="text-lg font-medium text-purple-200">📊 Atribuição Indireta ({report.atribuicao_indireta.percentual}%)</h3>
          </div>
          <p className="text-sm text-purple-300 mb-4">
            {report.atribuicao_indireta.percentual}% das vendas de Showroom, Indicação e Rede de Relacionamento são atribuídas ao tráfego pago (impacto de branding).
          </p>
          <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
            <div className="bg-white/10 rounded-lg p-4">
              <p className="text-xs text-purple-300">Showroom</p>
              <p className="text-xl font-bold">{report.atribuicao_indireta.detalhes.showroom.vendas_total} → {report.atribuicao_indireta.detalhes.showroom.atribuido}</p>
              <p className="text-xs text-purple-400">{formatCurrency(report.atribuicao_indireta.detalhes.showroom.valor)}</p>
            </div>
            <div className="bg-white/10 rounded-lg p-4">
              <p className="text-xs text-purple-300">Indicação</p>
              <p className="text-xl font-bold">{report.atribuicao_indireta.detalhes.indicacao.vendas_total} → {report.atribuicao_indireta.detalhes.indicacao.atribuido}</p>
              <p className="text-xs text-purple-400">{formatCurrency(report.atribuicao_indireta.detalhes.indicacao.valor)}</p>
            </div>
            <div className="bg-white/10 rounded-lg p-4">
              <p className="text-xs text-purple-300">Rede Relacionamento</p>
              <p className="text-xl font-bold">{report.atribuicao_indireta.detalhes.rede_relacionamento.vendas_total} → {report.atribuicao_indireta.detalhes.rede_relacionamento.atribuido}</p>
              <p className="text-xs text-purple-400">{formatCurrency(report.atribuicao_indireta.detalhes.rede_relacionamento.valor)}</p>
            </div>
            <div className="bg-emerald-500/30 rounded-lg p-4 border border-emerald-400">
              <p className="text-xs text-emerald-300">Total Atribuído</p>
              <p className="text-xl font-bold text-emerald-400">+{report.atribuicao_indireta.total_vendas_atribuidas} vendas</p>
              <p className="text-xs text-emerald-400">{formatCurrency(report.atribuicao_indireta.total_valor_atribuido)}</p>
            </div>
            <div className="bg-amber-500/30 rounded-lg p-4 border border-amber-400">
              <p className="text-xs text-amber-300">Melhoria CPV</p>
              <p className="text-xl font-bold text-amber-400">{report.auditoria.melhoria_com_atribuicao?.reducao_cpv || '-30%'}</p>
              <p className="text-xs text-amber-400">ROI {report.auditoria.melhoria_com_atribuicao?.aumento_roi || '+2.233%'}</p>
            </div>
          </div>
        </div>
      )}

      {/* CPV Real */}
      <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-xl p-6 text-white">
        <div className="flex items-center gap-2 mb-4">
          <Scale className="w-5 h-5 text-gray-400" />
          <h3 className="text-lg font-medium text-gray-300">CPV Real (Só Campanhas de LEAD)</h3>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
          <div>
            <p className="text-sm text-gray-400">CPV (só direto)</p>
            <p className="text-2xl font-semibold text-gray-400">{formatCurrency(report.roi.cpv_direto || report.roi.cpv_total || 0)}</p>
            <p className="text-xs text-gray-500">{report.roi.vendas_diretas || 26} vendas</p>
          </div>
          <div className="bg-emerald-500/20 rounded-lg p-4 border border-emerald-400/50">
            <p className="text-sm text-emerald-300">CPV (com atribuição)</p>
            <p className="text-2xl font-semibold text-emerald-400">{formatCurrency(report.roi.cpv_com_atribuicao || report.roi.cpv_total || 0)}</p>
            <p className="text-xs text-emerald-500">{report.roi.vendas_totais || 37} vendas</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">CPV Google</p>
            <p className="text-2xl font-semibold text-emerald-400">{formatCurrency(report.roi.google.cpv)}</p>
            <p className="text-xs text-emerald-500">⭐ Mais eficiente</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">CPV Meta</p>
            <p className="text-2xl font-semibold text-red-400">{formatCurrency(report.roi.meta.cpv)}</p>
            <p className="text-xs text-red-500">3x mais caro</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">ROI (com atribuição)</p>
            <p className="text-2xl font-semibold text-blue-400">{formatNumber(report.roi.roi_com_atribuicao || report.roi.roi_percentual || 0)}%</p>
            <p className="text-xs text-gray-500">retorno/investimento</p>
          </div>
        </div>
      </div>

      {/* Comparativo Google vs Meta */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Google */}
        <div className="bg-white rounded-xl border overflow-hidden">
          <div className="bg-gradient-to-r from-emerald-500 to-teal-600 px-5 py-4">
            <h3 className="text-lg font-semibold text-white">🟢 GOOGLE Ads</h3>
            <p className="text-white/80 text-sm">Invest. LEAD: {formatCurrency(report.roi.google.investimento_lead)}</p>
          </div>
          <div className="p-5 space-y-4">
            <div className="bg-emerald-50 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Leads</p>
                  <p className="text-xl font-semibold">{formatNumber(report.roi.google.leads_crm)}</p>
                </div>
                <ArrowRight className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Vendas</p>
                  <p className="text-xl font-semibold text-emerald-600">{formatNumber(report.roi.google.vendas)}</p>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-xs text-gray-500">Conversão</p>
                <p className="text-lg font-bold text-emerald-600">{report.roi.google.taxa_conversao}%</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">CPV</p>
                <p className="text-lg font-bold">{formatCurrency(report.roi.google.cpv)}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">ROI</p>
                <p className="text-lg font-bold text-emerald-600">{formatNumber(report.roi.google.roi)}%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Meta */}
        <div className="bg-white rounded-xl border overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 to-indigo-600 px-5 py-4">
            <h3 className="text-lg font-semibold text-white">🔵 META Ads</h3>
            <p className="text-white/80 text-sm">Invest. LEAD: {formatCurrency(report.roi.meta.investimento_lead)}</p>
          </div>
          <div className="p-5 space-y-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Leads</p>
                  <p className="text-xl font-semibold">{formatNumber(report.roi.meta.leads_crm)}</p>
                </div>
                <ArrowRight className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Vendas</p>
                  <p className="text-xl font-semibold text-blue-600">{formatNumber(report.roi.meta.vendas)}</p>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-xs text-gray-500">Conversão</p>
                <p className="text-lg font-bold text-blue-600">{report.roi.meta.taxa_conversao}%</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">CPV</p>
                <p className="text-lg font-bold">{formatCurrency(report.roi.meta.cpv)}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">ROI</p>
                <p className="text-lg font-bold text-blue-600">{formatNumber(report.roi.meta.roi)}%</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Auditoria CPV */}
      <div className="bg-gradient-to-r from-red-900 to-red-800 rounded-xl p-6 text-white">
        <div className="flex items-center gap-3 mb-4">
          <ShieldAlert className="w-6 h-6 text-red-300" />
          <h3 className="text-lg font-bold">🔍 Auditoria: CPV Proposto vs CPV Real</h3>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-sm text-red-200">CPV Proposto</p>
            <p className="text-2xl font-bold">{formatCurrency(report.auditoria.cpv_proposto)}</p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <p className="text-sm text-red-200">CPV (só direto)</p>
            <p className="text-2xl font-bold text-red-300">{formatCurrency(report.auditoria.cpv_real_direto || report.auditoria.cpv_real || 0)}</p>
          </div>
          <div className="bg-amber-500/30 rounded-lg p-4 border border-amber-400">
            <p className="text-sm text-amber-200">CPV (com atribuição)</p>
            <p className="text-2xl font-bold text-amber-300">{formatCurrency(report.auditoria.cpv_real_com_atribuicao || report.auditoria.cpv_real || 0)}</p>
          </div>
          <div className="bg-white/10 rounded-lg p-4 col-span-2">
            <p className="text-sm text-red-200">Status</p>
            <p className="text-lg font-bold text-amber-400">{report.auditoria.diferenca_cpv}</p>
          </div>
        </div>

        <div className="mt-4 p-4 bg-red-950/50 rounded-lg">
          <p className="text-sm text-red-200">
            <strong>⚠️ Problema:</strong> {report.auditoria.validacao}
          </p>
        </div>

        <div className="mt-4 grid lg:grid-cols-3 gap-4">
          <div className="bg-white/5 rounded-lg p-3">
            <p className="text-xs text-red-300">CPV</p>
            <p className="text-sm">{report.auditoria.eficiencia_comparativa.google_vs_meta_cpv}</p>
          </div>
          <div className="bg-white/5 rounded-lg p-3">
            <p className="text-xs text-red-300">ROI</p>
            <p className="text-sm">{report.auditoria.eficiencia_comparativa.google_vs_meta_roi}</p>
          </div>
          <div className="bg-white/5 rounded-lg p-3">
            <p className="text-xs text-red-300">Conversão</p>
            <p className="text-sm">{report.auditoria.eficiencia_comparativa.google_vs_meta_conversao}</p>
          </div>
        </div>
      </div>

      {/* Comparativo Outras Fontes */}
      <div className="bg-white rounded-xl border overflow-hidden">
        <div className="px-6 py-4 bg-gradient-to-r from-purple-600 to-indigo-600">
          <h3 className="text-lg font-semibold text-white">📊 Comparativo: Mídia Paga vs Outras Fontes</h3>
        </div>
        <div className="p-6">
          <div className="grid lg:grid-cols-4 gap-4">
            <div className="rounded-xl border-2 border-red-200 bg-red-50 p-4">
              <div className="flex items-center gap-2 mb-2">
                <Zap className="w-4 h-4 text-red-500" />
                <span className="font-semibold text-red-900">Mídia Paga</span>
              </div>
              <p className="text-2xl font-bold text-red-700">{report.qualidade.midia_paga.taxa_conversao}%</p>
              <p className="text-xs text-red-600">{report.qualidade.midia_paga.vendas} vendas de {report.qualidade.midia_paga.total_leads} leads</p>
            </div>
            <div className="rounded-xl border-2 border-emerald-200 bg-emerald-50 p-4">
              <div className="flex items-center gap-2 mb-2">
                <Flame className="w-4 h-4 text-emerald-500" />
                <span className="font-semibold text-emerald-900">Showroom</span>
              </div>
              <p className="text-2xl font-bold text-emerald-700">{report.qualidade.comparativo_outras_fontes.showroom.taxa}%</p>
              <p className="text-xs text-emerald-600">{report.qualidade.comparativo_outras_fontes.showroom.vendas} vendas</p>
            </div>
            <div className="rounded-xl border-2 border-emerald-200 bg-emerald-50 p-4">
              <div className="flex items-center gap-2 mb-2">
                <Flame className="w-4 h-4 text-emerald-500" />
                <span className="font-semibold text-emerald-900">Oferta Vendedor</span>
              </div>
              <p className="text-2xl font-bold text-emerald-700">{report.qualidade.comparativo_outras_fontes.oferta_vendedor.taxa}%</p>
              <p className="text-xs text-emerald-600">{report.qualidade.comparativo_outras_fontes.oferta_vendedor.vendas} vendas</p>
            </div>
            <div className="rounded-xl border-2 border-emerald-200 bg-emerald-50 p-4">
              <div className="flex items-center gap-2 mb-2">
                <Flame className="w-4 h-4 text-emerald-500" />
                <span className="font-semibold text-emerald-900">Indicação</span>
              </div>
              <p className="text-2xl font-bold text-emerald-700">{report.qualidade.comparativo_outras_fontes.indicacao.taxa}%</p>
              <p className="text-xs text-emerald-600">{report.qualidade.comparativo_outras_fontes.indicacao.vendas} vendas</p>
            </div>
          </div>
          <div className="mt-4 p-4 bg-amber-50 rounded-lg">
            <p className="text-sm text-amber-800">
              <strong>💡 Insight:</strong> {report.qualidade.insight}
            </p>
          </div>
        </div>
      </div>

      {/* Proposta de Redistribuição */}
      <div className="bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 rounded-xl p-6 text-white">
        <div className="flex items-center gap-3 mb-6">
          <Send className="w-6 h-6 text-purple-300" />
          <div>
            <h3 className="text-xl font-bold">📋 Proposta de Redistribuição</h3>
            <p className="text-purple-300 text-sm">{report.proposta.decisao}</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Cobranças */}
          <div className="bg-white/10 rounded-xl p-5">
            <h4 className="font-semibold text-purple-200 mb-4 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" />
              Cobranças para Agência (7 dias)
            </h4>
            <ul className="space-y-3">
              {report.proposta.cobrancas_7_dias.map((c, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="w-6 h-6 rounded-full bg-red-500 flex items-center justify-center text-xs font-bold shrink-0">{i + 1}</span>
                  <p className="text-sm">{c}</p>
                </li>
              ))}
            </ul>
          </div>

          {/* Realocação */}
          <div className="bg-white/10 rounded-xl p-5">
            <h4 className="font-semibold text-purple-200 mb-4 flex items-center gap-2">
              <Target className="w-4 h-4" />
              Nova Distribuição Sugerida
            </h4>
            <ul className="space-y-3">
              {report.proposta.realocacao.map((r, i) => (
                <li key={i} className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                  <p className="text-sm">{r}</p>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Vendas Esperadas */}
        <div className="mt-6 bg-emerald-500/20 rounded-xl p-5 border border-emerald-400/30">
          <h4 className="font-semibold text-emerald-300 mb-3">📈 Vendas Esperadas (Novo Mix)</h4>
          <div className="grid grid-cols-4 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-white">{report.proposta.vendas_esperadas_novo_mix.google}</p>
              <p className="text-xs text-emerald-300">Google/mês</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{report.proposta.vendas_esperadas_novo_mix.meta}</p>
              <p className="text-xs text-emerald-300">Meta/mês</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-emerald-400">{report.proposta.vendas_esperadas_novo_mix.total_mes}</p>
              <p className="text-xs text-emerald-300">Total/mês</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-amber-400">+{report.proposta.vendas_esperadas_novo_mix.aumento_vs_atual}</p>
              <p className="text-xs text-emerald-300">vs atual</p>
            </div>
          </div>
        </div>

        {/* KPIs */}
        <div className="mt-6 p-4 bg-white/10 rounded-xl">
          <h4 className="font-semibold text-purple-200 mb-3">KPIs para decidir manter/cortar</h4>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-2">
            {report.proposta.kpis_para_decidir.map((kpi, i) => (
              <div key={i} className="bg-white/5 rounded-lg p-2 text-xs text-center">
                {kpi}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="text-center text-xs text-gray-400">
        Relatório gerado automaticamente • Dados do CRM cruzados com relatórios da agência
      </div>
    </div>
  );
}
