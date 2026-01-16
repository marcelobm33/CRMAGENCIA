'use client';

import { useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  TrendingUp,
  TrendingDown,
  Target,
  Zap,
  XCircle,
  DollarSign,
  Users,
  BarChart3,
  Lightbulb,
  ArrowUpRight,
  ArrowDownRight,
  Flame,
  Snowflake,
} from 'lucide-react';

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

export default function ReuniaoAgenciaPage() {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    // Slide 0: Capa
    <div key="capa" className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-8">
      <div className="text-center max-w-4xl">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-amber-500/20 rounded-full text-amber-400 text-sm mb-8">
          <BarChart3 className="w-4 h-4" />
          Análise de Performance
        </div>
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
          Reunião de<br />
          <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
            Alinhamento
          </span>
        </h1>
        <p className="text-xl text-slate-400 mb-8">
          Netcar × Agência Voren
        </p>
        <div className="text-slate-500 text-sm">
          Período analisado: <span className="text-white font-medium">Outubro, Novembro e Dezembro 2025</span>
        </div>
        <div className="mt-12 flex items-center justify-center gap-4 text-slate-500">
          <span>Clique para avançar</span>
          <ArrowRight className="w-5 h-5 animate-pulse" />
        </div>
      </div>
    </div>,

    // Slide 1: Resumo Executivo
    <div key="resumo" className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-8 md:p-16">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-white mb-2">📊 Resumo Executivo</h2>
        <p className="text-slate-400 mb-12">Visão geral dos 3 meses de campanha</p>
        
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-white/10">
            <DollarSign className="w-8 h-8 text-emerald-400 mb-4" />
            <p className="text-slate-400 text-sm">Investido (LEAD)</p>
            <p className="text-3xl font-bold text-white">R$ 40.931</p>
            <p className="text-xs text-slate-500 mt-1">Campanhas de conversão</p>
          </div>
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-white/10">
            <Users className="w-8 h-8 text-blue-400 mb-4" />
            <p className="text-slate-400 text-sm">Leads Mídia Paga</p>
            <p className="text-3xl font-bold text-white">502</p>
            <p className="text-xs text-slate-500 mt-1">53% do total CRM</p>
          </div>
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-white/10">
            <Target className="w-8 h-8 text-amber-400 mb-4" />
            <p className="text-slate-400 text-sm">Vendas (com atribuição)</p>
            <p className="text-3xl font-bold text-white">37</p>
            <p className="text-xs text-slate-500 mt-1">26 diretas + 11 indiretas</p>
          </div>
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-white/10">
            <TrendingUp className="w-8 h-8 text-purple-400 mb-4" />
            <p className="text-slate-400 text-sm">ROI</p>
            <p className="text-3xl font-bold text-white">8.518%</p>
            <p className="text-xs text-slate-500 mt-1">Faturamento ÷ Investimento</p>
          </div>
        </div>

        <div className="bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-2xl p-6 border border-emerald-500/30">
          <div className="flex items-center gap-3 mb-4">
            <CheckCircle2 className="w-6 h-6 text-emerald-400" />
            <span className="text-lg font-semibold text-emerald-400">Resultado Geral: Positivo</span>
          </div>
          <p className="text-slate-300">
            Investimento de R$ 40.931 gerou R$ 3.486.620 em faturamento. 
            <strong className="text-white"> Retorno de R$ 85 para cada R$ 1 investido.</strong>
          </p>
        </div>
      </div>
    </div>,

    // Slide 2: O Que Vai Bem
    <div key="vai-bem" className="min-h-screen bg-gradient-to-br from-emerald-900 to-slate-900 p-8 md:p-16">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-emerald-500/20 rounded-xl flex items-center justify-center">
            <TrendingUp className="w-6 h-6 text-emerald-400" />
          </div>
          <h2 className="text-3xl font-bold text-white">O Que Vai Bem</h2>
        </div>
        <p className="text-emerald-300/60 mb-12">Pontos fortes a manter e potencializar</p>
        
        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white/5 backdrop-blur rounded-2xl p-8 border border-emerald-500/30">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-16 h-16 bg-emerald-500 rounded-2xl flex items-center justify-center">
                <span className="text-2xl">🟢</span>
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">Google Ads</h3>
                <p className="text-emerald-400">Melhor performance</p>
              </div>
            </div>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">ROI</span>
                <span className="text-2xl font-bold text-emerald-400">9.521%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Taxa de Conversão</span>
                <span className="text-2xl font-bold text-emerald-400">7,3%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">CPV</span>
                <span className="text-2xl font-bold text-emerald-400">R$ 1.035</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Vendas</span>
                <span className="text-2xl font-bold text-white">20</span>
              </div>
            </div>
          </div>

          <div className="bg-white/5 backdrop-blur rounded-2xl p-8 border border-emerald-500/30">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-16 h-16 bg-emerald-500/50 rounded-2xl flex items-center justify-center">
                <span className="text-2xl">🌐</span>
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">SITE (via Google)</h3>
                <p className="text-emerald-400">Maior volume</p>
              </div>
            </div>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Leads</span>
                <span className="text-2xl font-bold text-white">207</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Vendas</span>
                <span className="text-2xl font-bold text-white">19</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Taxa de Conversão</span>
                <span className="text-2xl font-bold text-emerald-400">9,2%</span>
              </div>
            </div>
            <div className="mt-6 p-4 bg-emerald-500/20 rounded-xl">
              <p className="text-sm text-emerald-300">
                <strong>73% das vendas de mídia</strong> vieram do Google
              </p>
            </div>
          </div>
        </div>

        <div className="mt-8 bg-white/5 rounded-2xl p-6 border border-white/10">
          <div className="flex items-center gap-3">
            <Lightbulb className="w-5 h-5 text-amber-400" />
            <span className="text-amber-400 font-medium">Insight</span>
          </div>
          <p className="mt-2 text-slate-300">
            Google (Pesquisa + PMax) é <strong className="text-white">3x mais eficiente</strong> que Meta em conversão.
            Com investimento similar, Google gera 3x mais vendas.
          </p>
        </div>
      </div>
    </div>,

    // Slide 3: Gargalos Críticos
    <div key="gargalos" className="min-h-screen bg-gradient-to-br from-red-900 to-slate-900 p-8 md:p-16">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-red-500/20 rounded-xl flex items-center justify-center">
            <AlertTriangle className="w-6 h-6 text-red-400" />
          </div>
          <h2 className="text-3xl font-bold text-white">Gargalos Críticos</h2>
        </div>
        <p className="text-red-300/60 mb-12">Pontos que precisam de atenção imediata</p>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Gargalo 1 */}
          <div className="bg-white/5 backdrop-blur rounded-2xl p-8 border border-red-500/30">
            <div className="flex items-center gap-3 mb-6">
              <XCircle className="w-8 h-8 text-red-400" />
              <h3 className="text-xl font-bold text-white">Meta Ads: Baixa Conversão</h3>
            </div>
            <div className="space-y-4 mb-6">
              <div className="flex justify-between items-center p-3 bg-red-500/10 rounded-lg">
                <span className="text-slate-400">Taxa de Conversão</span>
                <span className="text-2xl font-bold text-red-400">2,5%</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-red-500/10 rounded-lg">
                <span className="text-slate-400">CPV</span>
                <span className="text-2xl font-bold text-red-400">R$ 3.373</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Vendas</span>
                <span className="text-xl font-bold text-white">Apenas 6</span>
              </div>
            </div>
            <div className="p-4 bg-red-500/20 rounded-xl border border-red-500/30">
              <p className="text-sm text-red-200">
                <strong>Meta custa 3x mais</strong> que Google por venda.
                Investimento similar, resultado muito inferior.
              </p>
            </div>
          </div>

          {/* Gargalo 2 */}
          <div className="bg-white/5 backdrop-blur rounded-2xl p-8 border border-red-500/30">
            <div className="flex items-center gap-3 mb-6">
              <Snowflake className="w-8 h-8 text-blue-400" />
              <h3 className="text-xl font-bold text-white">Leads Frios Demais</h3>
            </div>
            <div className="space-y-4 mb-6">
              <div className="flex justify-between items-center p-3 bg-blue-500/10 rounded-lg">
                <span className="text-slate-400">Sem Interesse</span>
                <span className="text-xl font-bold text-blue-400">~30%</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-blue-500/10 rounded-lg">
                <span className="text-slate-400">Não Responde</span>
                <span className="text-xl font-bold text-blue-400">~27%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Total Leads Frios</span>
                <span className="text-xl font-bold text-red-400">~57%</span>
              </div>
            </div>
            <div className="p-4 bg-blue-500/20 rounded-xl border border-blue-500/30">
              <p className="text-sm text-blue-200">
                Mais da metade dos leads são <strong>curiosos ou não qualificados</strong>.
                Anúncios atraindo público errado.
              </p>
            </div>
          </div>
        </div>

        {/* Comparativo visual */}
        <div className="mt-8 bg-white/5 rounded-2xl p-6 border border-white/10">
          <h4 className="text-lg font-semibold text-white mb-4">Comparativo: Investimento vs Resultado</h4>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="flex items-center gap-4 p-4 bg-emerald-500/10 rounded-xl">
              <div className="w-20 h-20 bg-emerald-500 rounded-xl flex items-center justify-center text-3xl">
                🟢
              </div>
              <div>
                <p className="text-slate-400 text-sm">Google</p>
                <p className="text-white font-bold">R$ 20.693 → 20 vendas</p>
                <p className="text-emerald-400 text-sm">R$ 1.035/venda</p>
              </div>
            </div>
            <div className="flex items-center gap-4 p-4 bg-red-500/10 rounded-xl">
              <div className="w-20 h-20 bg-blue-500 rounded-xl flex items-center justify-center text-3xl">
                🔵
              </div>
              <div>
                <p className="text-slate-400 text-sm">Meta</p>
                <p className="text-white font-bold">R$ 20.238 → 6 vendas</p>
                <p className="text-red-400 text-sm">R$ 3.373/venda</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>,

    // Slide 4: O Que Precisa Mudar
    <div key="mudar" className="min-h-screen bg-gradient-to-br from-amber-900 to-slate-900 p-8 md:p-16">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-amber-500/20 rounded-xl flex items-center justify-center">
            <Zap className="w-6 h-6 text-amber-400" />
          </div>
          <h2 className="text-3xl font-bold text-white">O Que Precisa Mudar</h2>
        </div>
        <p className="text-amber-300/60 mb-12">Ajustes necessários para melhorar resultados</p>

        <div className="space-y-6">
          {/* Mudança 1 */}
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-amber-500/30 flex items-start gap-6">
            <div className="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center text-xl font-bold text-white shrink-0">
              1
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-white mb-2">Redistribuir o Budget</h3>
              <p className="text-slate-400 mb-4">
                Google performa 3x melhor, mas recebe o mesmo investimento que Meta.
              </p>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 bg-red-500/10 rounded-xl border border-red-500/30">
                  <p className="text-red-400 text-sm font-medium mb-2">❌ ATUAL</p>
                  <p className="text-white">Google 45% | Meta 55%</p>
                </div>
                <div className="p-4 bg-emerald-500/10 rounded-xl border border-emerald-500/30">
                  <p className="text-emerald-400 text-sm font-medium mb-2">✅ PROPOSTA</p>
                  <p className="text-white">Google 60% | Meta 25% | Branding 15%</p>
                </div>
              </div>
            </div>
          </div>

          {/* Mudança 2 */}
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-amber-500/30 flex items-start gap-6">
            <div className="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center text-xl font-bold text-white shrink-0">
              2
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-white mb-2">Qualificar os Anúncios</h3>
              <p className="text-slate-400 mb-4">
                57% dos leads são frios. Precisamos filtrar curiosos antes do clique.
              </p>
              <div className="flex flex-wrap gap-3">
                <span className="px-4 py-2 bg-amber-500/20 rounded-full text-amber-300 text-sm">Mostrar preço no anúncio</span>
                <span className="px-4 py-2 bg-amber-500/20 rounded-full text-amber-300 text-sm">Mencionar entrada/financiamento</span>
                <span className="px-4 py-2 bg-amber-500/20 rounded-full text-amber-300 text-sm">Segmentar por intenção</span>
                <span className="px-4 py-2 bg-amber-500/20 rounded-full text-amber-300 text-sm">Remarketing agressivo</span>
              </div>
            </div>
          </div>

          {/* Mudança 3 */}
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-amber-500/30 flex items-start gap-6">
            <div className="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center text-xl font-bold text-white shrink-0">
              3
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-white mb-2">Melhorar Rastreamento</h3>
              <p className="text-slate-400 mb-4">
                Garantir que todos os leads cheguem ao CRM com origem correta.
              </p>
              <div className="flex flex-wrap gap-3">
                <span className="px-4 py-2 bg-amber-500/20 rounded-full text-amber-300 text-sm">UTMs em todos os links</span>
                <span className="px-4 py-2 bg-amber-500/20 rounded-full text-amber-300 text-sm">Padronizar origem/canal</span>
                <span className="px-4 py-2 bg-amber-500/20 rounded-full text-amber-300 text-sm">Integração WhatsApp → CRM</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>,

    // Slide 5: Recomendações
    <div key="recomendacoes" className="min-h-screen bg-gradient-to-br from-indigo-900 to-slate-900 p-8 md:p-16">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-indigo-500/20 rounded-xl flex items-center justify-center">
            <Target className="w-6 h-6 text-indigo-400" />
          </div>
          <h2 className="text-3xl font-bold text-white">Recomendações</h2>
        </div>
        <p className="text-indigo-300/60 mb-12">Ações concretas para os próximos 30 dias</p>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Curto prazo */}
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-red-500/30">
            <div className="flex items-center gap-2 mb-4">
              <Flame className="w-5 h-5 text-red-400" />
              <span className="text-red-400 font-semibold">Imediato (7 dias)</span>
            </div>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
                <span className="text-slate-300 text-sm">Pausar campanhas de Meta com CPV &gt; R$ 4.000</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
                <span className="text-slate-300 text-sm">Aumentar budget de Google Pesquisa em 30%</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
                <span className="text-slate-300 text-sm">Adicionar preço nos criativos</span>
              </li>
            </ul>
          </div>

          {/* Médio prazo */}
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-amber-500/30">
            <div className="flex items-center gap-2 mb-4">
              <Zap className="w-5 h-5 text-amber-400" />
              <span className="text-amber-400 font-semibold">Curto prazo (14 dias)</span>
            </div>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <span className="text-slate-300 text-sm">Implementar remarketing no Google</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <span className="text-slate-300 text-sm">Criar campanhas segmentadas por intenção</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <span className="text-slate-300 text-sm">Testar YouTube com extensão WhatsApp</span>
              </li>
            </ul>
          </div>

          {/* Longo prazo */}
          <div className="bg-white/5 backdrop-blur rounded-2xl p-6 border border-emerald-500/30">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              <span className="text-emerald-400 font-semibold">Médio prazo (30 dias)</span>
            </div>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <span className="text-slate-300 text-sm">Relatório semanal com CPV por canal</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <span className="text-slate-300 text-sm">Meta de CPV &lt; R$ 1.500</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <span className="text-slate-300 text-sm">Integração completa CRM ↔ Ads</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Projeção */}
        <div className="mt-8 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-2xl p-6 border border-emerald-500/30">
          <h4 className="text-lg font-semibold text-white mb-4">📈 Projeção com Novo Mix</h4>
          <div className="grid md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-4xl font-bold text-emerald-400">~10</p>
              <p className="text-slate-400 text-sm">vendas/mês</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-emerald-400">+15%</p>
              <p className="text-slate-400 text-sm">vs atual</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-amber-400">R$ 1.106</p>
              <p className="text-slate-400 text-sm">CPV alvo</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-blue-400">10.000%+</p>
              <p className="text-slate-400 text-sm">ROI esperado</p>
            </div>
          </div>
        </div>
      </div>
    </div>,

    // Slide 6: Conclusão
    <div key="conclusao" className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-8">
      <div className="max-w-4xl text-center">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-8">
          Conclusão
        </h2>
        
        <div className="bg-white/5 backdrop-blur rounded-3xl p-8 border border-white/10 mb-8">
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="p-4">
              <div className="w-16 h-16 bg-emerald-500/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="w-8 h-8 text-emerald-400" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">O Que Funciona</h3>
              <p className="text-slate-400 text-sm">Google Ads com ROI de 9.521% e conversão de 7,3%</p>
            </div>
            <div className="p-4">
              <div className="w-16 h-16 bg-red-500/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <AlertTriangle className="w-8 h-8 text-red-400" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">O Que Ajustar</h3>
              <p className="text-slate-400 text-sm">Meta Ads com CPV 3x maior e leads frios demais</p>
            </div>
            <div className="p-4">
              <div className="w-16 h-16 bg-amber-500/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Target className="w-8 h-8 text-amber-400" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Próximo Passo</h3>
              <p className="text-slate-400 text-sm">Redistribuir: 60% Google, 25% Meta, 15% Branding</p>
            </div>
          </div>
          
          <div className="border-t border-white/10 pt-6">
            <p className="text-xl text-white">
              <strong className="text-emerald-400">Manter investimento</strong>, mas realocar para onde converte mais.
            </p>
            <p className="text-slate-400 mt-2">
              Foco em qualidade do lead, não quantidade.
            </p>
          </div>
        </div>

        <div className="flex items-center justify-center gap-4 text-slate-500">
          <span>Netcar × Voren</span>
          <span>•</span>
          <span>Janeiro 2026</span>
        </div>
      </div>
    </div>,
  ];

  const nextSlide = () => {
    if (currentSlide < slides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    }
  };

  const prevSlide = () => {
    if (currentSlide > 0) {
      setCurrentSlide(currentSlide - 1);
    }
  };

  return (
    <div 
      className="relative cursor-pointer select-none"
      onClick={nextSlide}
    >
      {slides[currentSlide]}
      
      {/* Navigation */}
      <div className="fixed bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-4 z-50">
        <button 
          onClick={(e) => { e.stopPropagation(); prevSlide(); }}
          disabled={currentSlide === 0}
          className="w-10 h-10 rounded-full bg-white/10 backdrop-blur flex items-center justify-center text-white disabled:opacity-30 hover:bg-white/20 transition-all"
        >
          ←
        </button>
        
        <div className="flex gap-2">
          {slides.map((_, i) => (
            <button
              key={i}
              onClick={(e) => { e.stopPropagation(); setCurrentSlide(i); }}
              className={`w-2 h-2 rounded-full transition-all ${
                i === currentSlide ? 'bg-white w-6' : 'bg-white/30'
              }`}
            />
          ))}
        </div>
        
        <button 
          onClick={(e) => { e.stopPropagation(); nextSlide(); }}
          disabled={currentSlide === slides.length - 1}
          className="w-10 h-10 rounded-full bg-white/10 backdrop-blur flex items-center justify-center text-white disabled:opacity-30 hover:bg-white/20 transition-all"
        >
          →
        </button>
      </div>

      {/* Slide counter */}
      <div className="fixed top-8 right-8 text-white/50 text-sm z-50">
        {currentSlide + 1} / {slides.length}
      </div>
    </div>
  );
}
