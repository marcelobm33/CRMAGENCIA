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
  Flame,
  Snowflake,
  Clock,
  ThumbsUp,
  ThumbsDown,
  MessageCircle,
  ChevronRight,
  Star,
  Info,
  Rocket,
  Wrench,
  Bot,
  RefreshCw,
  FileSearch,
  Smartphone,
} from 'lucide-react';

function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0,
  }).format(value);
}

// Componente de Tooltip
function Tooltip({ 
  children, 
  content,
  formula,
  source 
}: { 
  children: React.ReactNode; 
  content: string;
  formula?: string;
  source?: string;
}) {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div className="relative inline-flex items-center gap-1 group">
      {children}
      <button
        type="button"
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onClick={() => setIsVisible(!isVisible)}
        className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-slate-200 hover:bg-slate-300 transition-colors cursor-help shrink-0"
        aria-label="Ver detalhes do cálculo"
      >
        <Info className="w-2.5 h-2.5 text-slate-600" />
      </button>
      {isVisible && (
        <div className="absolute z-[100] bottom-full left-0 mb-2 w-80 p-4 bg-slate-900 text-white text-sm rounded-xl shadow-2xl border border-slate-700">
          <p className="font-medium text-slate-100 leading-relaxed">{content}</p>
          {formula && (
            <div className="mt-3 p-3 bg-slate-800 rounded-lg border border-slate-700">
              <p className="text-[10px] uppercase text-slate-400 mb-1 font-semibold">Fórmula</p>
              <p className="text-slate-200 font-mono text-xs break-all">
                {formula}
              </p>
            </div>
          )}
          {source && (
            <div className="mt-3 pt-3 border-t border-slate-700 flex items-center gap-2">
              <span className="text-base">📊</span>
              <p className="text-slate-400 text-xs">
                <span className="font-medium text-slate-300">Fonte:</span> {source}
              </p>
            </div>
          )}
          <div className="absolute top-full left-4 border-8 border-transparent border-t-slate-900"></div>
        </div>
      )}
    </div>
  );
}

export default function ReuniaoAgenciaPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white">
        <div className="max-w-6xl mx-auto px-6 py-12">
          <div className="flex items-center gap-3 text-amber-400 text-sm mb-4">
            <BarChart3 className="w-4 h-4" />
            <span>Análise de Performance • Out/Nov/Dez 2025</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Relatório de Alinhamento
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl">
            Cruzamento de dados entre relatórios da agência e vendas reais do CRM. 
            Base para tomada de decisão sobre estratégia de mídia paga.
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-12 space-y-12">
        
        {/* Contexto */}
        <section>
          <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
            <div className="px-6 py-4 bg-slate-100 border-b">
              <h2 className="text-lg font-semibold text-slate-800 flex items-center gap-2">
                <MessageCircle className="w-5 h-5 text-slate-600" />
                Contexto da Análise
              </h2>
            </div>
            <div className="p-6">
              <div className="prose prose-slate max-w-none">
                <p className="text-slate-600 leading-relaxed">
                  Nos últimos 3 meses, investimos aproximadamente <strong className="text-slate-900">R$ 46.598</strong> em mídia paga, 
                  sendo <strong className="text-slate-900">R$ 40.931</strong> em campanhas de geração de leads (WhatsApp, Site, Pesquisa, PMax) 
                  e <strong className="text-slate-900">R$ 5.667</strong> em branding (alcance, visitas ao perfil, TikTok).
                </p>
                <p className="text-slate-600 leading-relaxed mt-4">
                  Este relatório cruza os dados reportados pela agência com as vendas efetivamente registradas no CRM, 
                  permitindo uma visão real do retorno sobre investimento e identificação de oportunidades de otimização.
                </p>
              </div>
              
              <div className="grid md:grid-cols-4 gap-4 mt-8">
                <div className="bg-slate-50 rounded-xl p-4">
                  <Tooltip 
                    content="Soma do investimento em Meta Ads e Google Ads (Out/Nov/Dez)"
                    formula="Meta (R$ 25.585) + Google (R$ 21.693) = R$ 46.598"
                    source="Relatórios mensais da agência Voren"
                  >
                    <p className="text-xs text-slate-500 uppercase font-medium">Investimento Total</p>
                  </Tooltip>
                  <p className="text-2xl font-bold text-slate-900 mt-1">R$ 46.598</p>
                </div>
                <div className="bg-slate-50 rounded-xl p-4">
                  <Tooltip 
                    content="Total de leads de mídia paga registrados no CRM (WhatsApp, Site, Facebook, Instagram)"
                    formula="WhatsApp + Site + Facebook + Instagram = 502 leads"
                    source="CRM Netcar - filtro por origem de mídia paga"
                  >
                    <p className="text-xs text-slate-500 uppercase font-medium">Leads no CRM</p>
                  </Tooltip>
                  <p className="text-2xl font-bold text-slate-900 mt-1">502</p>
                </div>
                <div className="bg-slate-50 rounded-xl p-4">
                  <Tooltip 
                    content="Vendas de leads diretos de mídia paga + 20% das vendas de Showroom, Indicação e Relacionamento (atribuição indireta)"
                    formula="Vendas diretas (26) + Atribuição indireta (11) = 37 vendas"
                    source="CRM Netcar - status 'Ganho' + modelo de atribuição"
                  >
                    <p className="text-xs text-slate-500 uppercase font-medium">Vendas Atribuídas</p>
                  </Tooltip>
                  <p className="text-2xl font-bold text-slate-900 mt-1">37</p>
                </div>
                <div className="bg-slate-50 rounded-xl p-4">
                  <Tooltip 
                    content="Valor total das 37 vendas atribuídas à mídia paga"
                    formula="Soma dos valores de venda das 37 unidades"
                    source="CRM Netcar - campo 'valor_venda' dos negócios ganhos"
                  >
                    <p className="text-xs text-slate-500 uppercase font-medium">Faturamento</p>
                  </Tooltip>
                  <p className="text-2xl font-bold text-slate-900 mt-1">R$ 3,4M</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* O que vai bem */}
        <section>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-emerald-100 rounded-xl flex items-center justify-center">
              <ThumbsUp className="w-5 h-5 text-emerald-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">O Que Está Funcionando</h2>
              <p className="text-slate-500">Pontos fortes que devemos manter e potencializar</p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Google */}
            <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
              <div className="px-6 py-4 bg-gradient-to-r from-emerald-500 to-teal-500">
                <div className="flex items-center gap-3">
                  <Star className="w-6 h-6 text-white" />
                  <h3 className="text-xl font-semibold text-white">Google Ads</h3>
                </div>
                <p className="text-emerald-100 text-sm mt-1">Melhor canal de conversão</p>
              </div>
              <div className="p-6">
                <div className="flex items-center gap-4 mb-6">
                  <div className="flex-1">
                    <Tooltip 
                      content="Retorno sobre investimento: quanto faturamos para cada R$ 1 investido"
                      formula="(Faturamento / Investimento) × 100 = (R$ 1.970.100 / R$ 20.693) × 100"
                      source="CRM (vendas) + Relatório agência (investimento)"
                    >
                      <p className="text-sm text-slate-500">ROI</p>
                    </Tooltip>
                    <p className="text-3xl font-bold text-emerald-600">9.521%</p>
                  </div>
                  <div className="flex-1">
                    <Tooltip 
                      content="Taxa de conversão: percentual de leads que viraram venda"
                      formula="(Vendas / Leads) × 100 = (20 / 273) × 100 = 7,3%"
                      source="CRM Netcar - leads e vendas de origem Google/Site"
                    >
                      <p className="text-sm text-slate-500">Conversão</p>
                    </Tooltip>
                    <p className="text-3xl font-bold text-emerald-600">7,3%</p>
                  </div>
                </div>
                
                <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-100">
                  <p className="text-sm text-emerald-800">
                    <strong>Por que funciona:</strong> Google captura pessoas com intenção de compra real - 
                    quem pesquisa "comprar carro seminovo" já está no momento de decisão. 
                    A conversão é naturalmente maior porque o público está qualificado.
                  </p>
                </div>

                <div className="mt-4 space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <Tooltip 
                      content="Investimento em campanhas de LEAD do Google Ads (Pesquisa + PMax)"
                      formula="R$ 20.693 (apenas campanhas de geração de lead)"
                      source="Relatório mensal Voren - Google Ads"
                    >
                      <span className="text-slate-600">Investimento</span>
                    </Tooltip>
                    <span className="font-medium text-slate-900">R$ 20.693</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <Tooltip 
                      content="Vendas de leads que vieram do Google (Site + WhatsApp via Google)"
                      formula="19 (Site) + 1 (WhatsApp Google) = 20 vendas"
                      source="CRM Netcar - origem Google/Site"
                    >
                      <span className="text-slate-600">Vendas geradas</span>
                    </Tooltip>
                    <span className="font-medium text-slate-900">20 unidades</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <Tooltip 
                      content="Custo por Venda: quanto gastamos em média para cada venda"
                      formula="Investimento / Vendas = R$ 20.693 / 20 = R$ 1.035"
                      source="Cálculo: investimento Google / vendas Google"
                    >
                      <span className="text-slate-600">Custo por venda</span>
                    </Tooltip>
                    <span className="font-medium text-emerald-600">R$ 1.035</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Site */}
            <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
              <div className="px-6 py-4 bg-gradient-to-r from-blue-500 to-indigo-500">
                <div className="flex items-center gap-3">
                  <TrendingUp className="w-6 h-6 text-white" />
                  <h3 className="text-xl font-semibold text-white">Tráfego via Site</h3>
                </div>
                <p className="text-blue-100 text-sm mt-1">Principal fonte de leads qualificados</p>
              </div>
              <div className="p-6">
                <div className="flex items-center gap-4 mb-6">
                  <div className="flex-1">
                    <Tooltip 
                      content="Leads que entraram no CRM com origem 'Site' (formulário ou WhatsApp via site)"
                      formula="Total de leads com origem_lead = 'Site'"
                      source="CRM Netcar - campo origem_lead"
                    >
                      <p className="text-sm text-slate-500">Leads</p>
                    </Tooltip>
                    <p className="text-3xl font-bold text-blue-600">207</p>
                  </div>
                  <div className="flex-1">
                    <Tooltip 
                      content="Taxa de conversão específica dos leads que vieram pelo site"
                      formula="(Vendas Site / Leads Site) × 100 = (19 / 207) × 100 = 9,2%"
                      source="CRM Netcar - leads e vendas com origem 'Site'"
                    >
                      <p className="text-sm text-slate-500">Conversão</p>
                    </Tooltip>
                    <p className="text-3xl font-bold text-blue-600">9,2%</p>
                  </div>
                </div>
                
                <div className="bg-blue-50 rounded-xl p-4 border border-blue-100">
                  <p className="text-sm text-blue-800">
                    <strong>Por que funciona:</strong> O site funciona como filtro natural - 
                    só quem tem interesse real navega, escolhe um veículo e entra em contato. 
                    Esse comportamento elimina curiosos antes do lead chegar ao vendedor.
                  </p>
                </div>

                <div className="mt-4 space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <Tooltip 
                      content="Vendas fechadas de leads que vieram pelo site"
                      formula="Leads Site com status = 'Ganho'"
                      source="CRM Netcar - negócios ganhos com origem 'Site'"
                    >
                      <span className="text-slate-600">Vendas geradas</span>
                    </Tooltip>
                    <span className="font-medium text-slate-900">19 unidades</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <Tooltip 
                      content="Participação do Site no total de vendas de mídia paga"
                      formula="(Vendas Site / Vendas Mídia Paga) × 100 = (19 / 26) × 100 ≈ 73%"
                      source="Cálculo: vendas site vs total vendas diretas de mídia"
                    >
                      <span className="text-slate-600">% do total de vendas</span>
                    </Tooltip>
                    <span className="font-medium text-blue-600">73% das vendas de mídia</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Insight */}
          <div className="mt-6 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-2xl p-6 border border-emerald-100">
            <div className="flex items-start gap-4">
              <Lightbulb className="w-6 h-6 text-emerald-600 shrink-0 mt-1" />
              <div>
                <h4 className="font-semibold text-emerald-900">Conclusão</h4>
                <p className="text-emerald-800 mt-1">
                  O Google Ads, especialmente quando direciona para o site, é responsável por <strong>73% das vendas</strong> de mídia paga. 
                  Isso indica que o funil de conversão está funcionando bem quando o cliente tem tempo para explorar os veículos antes de entrar em contato.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* O que precisa melhorar */}
        <section>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center">
              <ThumbsDown className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">O Que Precisa Melhorar</h2>
              <p className="text-slate-500">Gargalos identificados que impactam o resultado</p>
            </div>
          </div>

          <div className="space-y-6">
            {/* Meta */}
            <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
              <div className="px-6 py-4 bg-gradient-to-r from-red-500 to-orange-500">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <AlertTriangle className="w-6 h-6 text-white" />
                    <h3 className="text-xl font-semibold text-white">Meta Ads (Facebook/Instagram)</h3>
                  </div>
                  <span className="px-3 py-1 bg-white/20 rounded-full text-white text-sm">Atenção</span>
                </div>
              </div>
              <div className="p-6">
                <div className="grid md:grid-cols-3 gap-6 mb-6">
                  <div className="text-center p-4 bg-red-50 rounded-xl">
                    <Tooltip 
                      content="Taxa de conversão de leads Meta Ads para vendas"
                      formula="(Vendas / Leads) × 100 = (6 / 238) × 100 = 2,5%"
                      source="CRM Netcar - leads de Facebook, Instagram e WhatsApp via Meta"
                    >
                      <p className="text-sm text-red-600 font-medium">Conversão</p>
                    </Tooltip>
                    <p className="text-3xl font-bold text-red-700">2,5%</p>
                    <p className="text-xs text-red-500 mt-1">vs 7,3% do Google</p>
                  </div>
                  <div className="text-center p-4 bg-red-50 rounded-xl">
                    <Tooltip 
                      content="Custo por Venda no Meta Ads (quanto gastamos para cada venda)"
                      formula="Investimento Lead Meta / Vendas Meta = R$ 20.238 / 6 = R$ 3.373"
                      source="Relatório agência (investimento) + CRM (vendas)"
                    >
                      <p className="text-sm text-red-600 font-medium">Custo por Venda</p>
                    </Tooltip>
                    <p className="text-3xl font-bold text-red-700">R$ 3.373</p>
                    <p className="text-xs text-red-500 mt-1">3x mais caro que Google</p>
                  </div>
                  <div className="text-center p-4 bg-red-50 rounded-xl">
                    <Tooltip 
                      content="Total de vendas geradas por leads do Meta Ads"
                      formula="Leads Meta com status = 'Ganho'"
                      source="CRM Netcar - negócios ganhos com origem Facebook/Instagram/WhatsApp"
                    >
                      <p className="text-sm text-red-600 font-medium">Vendas</p>
                    </Tooltip>
                    <p className="text-3xl font-bold text-red-700">6</p>
                    <p className="text-xs text-red-500 mt-1">vs 20 do Google</p>
                  </div>
                </div>

                <div className="bg-slate-50 rounded-xl p-5">
                  <h4 className="font-semibold text-slate-900 mb-3">Por que está acontecendo?</h4>
                  <div className="space-y-3">
                    <div className="flex items-start gap-3">
                      <ChevronRight className="w-5 h-5 text-slate-400 shrink-0 mt-0.5" />
                      <p className="text-slate-600">
                        <strong className="text-slate-800">Público frio:</strong> Instagram e Facebook atingem pessoas que não estão necessariamente procurando comprar um carro. 
                        Elas veem o anúncio enquanto rolam o feed, gerando curiosidade, mas não intenção de compra.
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <ChevronRight className="w-5 h-5 text-slate-400 shrink-0 mt-0.5" />
                      <p className="text-slate-600">
                        <strong className="text-slate-800">WhatsApp direto:</strong> Campanhas de WhatsApp geram volume, mas sem filtro de qualificação. 
                        O vendedor recebe muitos contatos que "só querem saber o preço" sem real interesse em comprar.
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <ChevronRight className="w-5 h-5 text-slate-400 shrink-0 mt-0.5" />
                      <p className="text-slate-600">
                        <strong className="text-slate-800">Concorrência de atenção:</strong> No Instagram, o anúncio compete com fotos de amigos, memes e reels. 
                        A atenção do usuário é dispersa, diferente do Google onde ele está ativamente buscando.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Leads Frios */}
            <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
              <div className="px-6 py-4 bg-gradient-to-r from-blue-600 to-cyan-600">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Snowflake className="w-6 h-6 text-white" />
                    <h3 className="text-xl font-semibold text-white">Qualidade dos Leads</h3>
                  </div>
                  <span className="px-3 py-1 bg-white/20 rounded-full text-white text-sm">Crítico</span>
                </div>
              </div>
              <div className="p-6">
                <div className="grid md:grid-cols-2 gap-6 mb-6">
                  <div className="p-5 bg-blue-50 rounded-xl border border-blue-100">
                    <div className="flex items-center gap-3 mb-3">
                      <Tooltip 
                        content="Percentual de leads perdidos por falta de interesse ou não resposta"
                        formula="(Sem Interesse + Não Responde) / Total Perdidos = (105 + 98) / 353 ≈ 57%"
                        source="CRM Netcar - campo motivo_perda dos negócios perdidos"
                      >
                        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-xl font-bold text-blue-700">57%</span>
                        </div>
                      </Tooltip>
                      <div>
                        <p className="font-semibold text-blue-900">Leads Frios</p>
                        <p className="text-sm text-blue-600">dos leads são perdidos por "Sem Interesse" ou "Não Responde"</p>
                      </div>
                    </div>
                  </div>
                  <div className="p-5 bg-slate-50 rounded-xl border border-slate-200">
                    <Tooltip 
                      content="Ranking dos motivos mais frequentes de perda de negócio"
                      formula="Contagem por motivo / Total de perdidos × 100"
                      source="CRM Netcar - tabela de motivos de perda"
                    >
                      <p className="font-semibold text-slate-900 mb-2">Principais motivos de perda:</p>
                    </Tooltip>
                    <ul className="space-y-2">
                      <li className="flex items-center justify-between text-sm">
                        <span className="text-slate-600">Sem Interesse</span>
                        <span className="font-medium text-slate-900">~30%</span>
                      </li>
                      <li className="flex items-center justify-between text-sm">
                        <span className="text-slate-600">Cliente Não Responde</span>
                        <span className="font-medium text-slate-900">~27%</span>
                      </li>
                    </ul>
                  </div>
                </div>

                <div className="bg-slate-50 rounded-xl p-5">
                  <h4 className="font-semibold text-slate-900 mb-3">O que isso significa?</h4>
                  <p className="text-slate-600">
                    Mais da metade dos leads que chegam ao CRM não têm real intenção de compra. 
                    Isso gera trabalho para a equipe comercial sem retorno, aumenta o custo operacional 
                    e desmotiva os vendedores que gastam tempo com contatos que não vão converter.
                  </p>
                  <p className="text-slate-600 mt-3">
                    <strong>O problema não é só a quantidade de leads, mas a qualidade.</strong> 
                    Prefira 100 leads qualificados a 500 curiosos.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Recomendações */}
        <section>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center">
              <Zap className="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">Recomendações</h2>
              <p className="text-slate-500">Mudanças sugeridas para os próximos 30 dias</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
            <div className="p-6">
              {/* Recomendação 1 */}
              <div className="flex gap-6 pb-6 border-b">
                <div className="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center text-white font-bold text-lg shrink-0">
                  1
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-slate-900 mb-2">Redistribuir o Investimento</h3>
                  <p className="text-slate-600 mb-4">
                    Google performa 3x melhor que Meta, mas recebe investimento similar. 
                    Faz sentido direcionar mais verba para onde converte mais.
                  </p>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="p-4 bg-red-50 rounded-xl border border-red-100">
                      <p className="text-sm font-medium text-red-700 mb-2">Atual</p>
                      <p className="text-slate-700">Google ~45% | Meta ~55%</p>
                    </div>
                    <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-100">
                      <p className="text-sm font-medium text-emerald-700 mb-2">Sugerido</p>
                      <p className="text-slate-700">Google 60% | Meta 25% | Branding 15%</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recomendação 2 */}
              <div className="flex gap-6 py-6 border-b">
                <div className="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center text-white font-bold text-lg shrink-0">
                  2
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-slate-900 mb-2">Qualificar nos Anúncios</h3>
                  <p className="text-slate-600 mb-4">
                    Adicionar informações que filtram curiosos antes do clique: preço, condições de financiamento, 
                    exigência de análise de crédito. Quem não tiver perfil já desiste antes de ocupar o tempo do vendedor.
                  </p>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1.5 bg-amber-50 text-amber-700 rounded-lg text-sm border border-amber-200">
                      Mostrar faixa de preço
                    </span>
                    <span className="px-3 py-1.5 bg-amber-50 text-amber-700 rounded-lg text-sm border border-amber-200">
                      Mencionar entrada mínima
                    </span>
                    <span className="px-3 py-1.5 bg-amber-50 text-amber-700 rounded-lg text-sm border border-amber-200">
                      "Sujeito à análise de crédito"
                    </span>
                    <span className="px-3 py-1.5 bg-amber-50 text-amber-700 rounded-lg text-sm border border-amber-200">
                      Remarketing para quem visitou
                    </span>
                  </div>
                </div>
              </div>

              {/* Recomendação 3 */}
              <div className="flex gap-6 py-6 border-b">
                <div className="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center text-white font-bold text-lg shrink-0">
                  3
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-slate-900 mb-2">Priorizar Site sobre WhatsApp Direto</h3>
                  <p className="text-slate-600 mb-4">
                    Campanhas que levam ao site têm conversão de 9,2%, enquanto WhatsApp direto tem muito mais abandono. 
                    O site funciona como filtro: quem navega, escolhe um carro e então entra em contato já está mais qualificado.
                  </p>
                  <div className="p-4 bg-blue-50 rounded-xl border border-blue-100">
                    <p className="text-sm text-blue-800">
                      <strong>Sugestão:</strong> Direcionar campanhas para página de estoque/veículo específico, 
                      não direto para WhatsApp. O cliente que navega e escolhe converte mais.
                    </p>
                  </div>
                </div>
              </div>

              {/* Recomendação 4 */}
              <div className="flex gap-6 pt-6">
                <div className="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center text-white font-bold text-lg shrink-0">
                  4
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-slate-900 mb-2">Acompanhamento por CPV, não CPL</h3>
                  <p className="text-slate-600 mb-4">
                    O custo por lead (CPL) não reflete a realidade. Um lead de R$ 50 que não converte é mais caro que um de R$ 200 que vira venda. 
                    O indicador que importa é o Custo por Venda (CPV).
                  </p>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="p-4 bg-slate-50 rounded-xl">
                      <Tooltip 
                        content="Custo por Venda real calculado com base no investimento em LEAD"
                        formula="Investimento Lead / Vendas = R$ 40.931 / 37 = R$ 1.106"
                        source="Relatório agência (verba lead) + CRM (vendas atribuídas)"
                      >
                        <p className="text-sm text-slate-500 mb-1">CPV atual (com atribuição)</p>
                      </Tooltip>
                      <p className="text-2xl font-bold text-slate-900">R$ 1.106</p>
                    </div>
                    <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-100">
                      <Tooltip 
                        content="Meta de CPV sugerida para manter rentabilidade saudável"
                        formula="Considerando ticket médio ~R$ 94k e margem operacional"
                        source="Análise de rentabilidade do setor automotivo"
                      >
                        <p className="text-sm text-emerald-600 mb-1">Meta sugerida</p>
                      </Tooltip>
                      <p className="text-2xl font-bold text-emerald-700">&lt; R$ 1.500</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Conclusão */}
        <section>
          <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-2xl p-8 text-white">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-3xl font-bold mb-6">Conclusão</h2>
              
              <p className="text-lg text-slate-300 mb-8">
                O investimento em mídia paga está gerando retorno positivo, com ROI de <strong className="text-white">8.518%</strong>. 
                No entanto, existe uma disparidade clara entre os canais: <strong className="text-emerald-400">Google funciona</strong>, 
                <strong className="text-amber-400"> Meta precisa de ajustes</strong>.
              </p>

              <div className="grid md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white/10 rounded-xl p-5">
                  <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto mb-3" />
                  <h4 className="font-semibold mb-2">Manter</h4>
                  <p className="text-sm text-slate-400">Google Ads com foco em Pesquisa e Site</p>
                </div>
                <div className="bg-white/10 rounded-xl p-5">
                  <Zap className="w-8 h-8 text-amber-400 mx-auto mb-3" />
                  <h4 className="font-semibold mb-2">Otimizar</h4>
                  <p className="text-sm text-slate-400">Meta Ads com qualificação e remarketing</p>
                </div>
                <div className="bg-white/10 rounded-xl p-5">
                  <Target className="w-8 h-8 text-blue-400 mx-auto mb-3" />
                  <h4 className="font-semibold mb-2">Medir</h4>
                  <p className="text-sm text-slate-400">CPV por canal, não apenas CPL</p>
                </div>
              </div>

              <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                <p className="text-xl font-medium">
                  Proposta: <span className="text-emerald-400">manter o investimento total</span>, mas 
                  <span className="text-amber-400"> realocar para onde converte mais</span>.
                </p>
                <p className="text-slate-400 mt-2">
                  Google 60% | Meta 25% | Branding 15%
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Direcionamento Estratégico 2026 */}
        <section>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
              <Flame className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">Direcionamento Estratégico 2026</h2>
              <p className="text-slate-500">Modelo de 3 pistas para tratamento de leads</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
            <div className="p-6 space-y-6">
              
              {/* Princípio Base */}
              <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white rounded-xl p-6">
                <p className="text-lg font-medium mb-2">🎯 Princípio-Base</p>
                <p className="text-slate-300 mb-4">
                  O problema <strong className="text-white">não é falta de lead</strong> — é falta de progressão do lead dentro do funil.
                </p>
                <div className="bg-white/10 rounded-lg p-4 border border-white/20">
                  <p className="text-amber-300 font-medium">
                    "A gente não quer menos lead. A gente quer lead andando mais dentro do funil."
                  </p>
                </div>
              </div>

              {/* Nova Leitura de Orçamento */}
              <div className="pb-6 border-b">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">📊 Nova Leitura de Orçamento</h3>
                <p className="text-slate-600 mb-4">
                  Em vez de pensar só em "canal", pensar em <strong>momento do cliente</strong>:
                </p>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-slate-100">
                        <th className="text-left p-3 font-semibold text-slate-700 rounded-tl-lg">Momento</th>
                        <th className="text-left p-3 font-semibold text-slate-700">Canal</th>
                        <th className="text-left p-3 font-semibold text-slate-700 rounded-tr-lg">Função da Campanha</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      <tr className="bg-emerald-50">
                        <td className="p-3">
                          <Tooltip
                            content="Cliente já decidiu comprar, está comparando opções"
                            source="Comportamento: pesquisa 'comprar carro usado [cidade]'"
                          >
                            <span className="flex items-center gap-2">
                              <span className="w-3 h-3 bg-emerald-500 rounded-full"></span>
                              <strong className="text-emerald-800">Alta intenção</strong>
                            </span>
                          </Tooltip>
                        </td>
                        <td className="p-3 text-slate-700">Google Search / Site</td>
                        <td className="p-3 text-emerald-700 font-medium">🎯 Fechamento direto</td>
                      </tr>
                      <tr className="bg-amber-50">
                        <td className="p-3">
                          <Tooltip
                            content="Cliente interessado mas ainda não decidiu, quer ver opções"
                            source="Comportamento: clica em anúncio de carro, pede info"
                          >
                            <span className="flex items-center gap-2">
                              <span className="w-3 h-3 bg-amber-500 rounded-full"></span>
                              <strong className="text-amber-800">Média intenção</strong>
                            </span>
                          </Tooltip>
                        </td>
                        <td className="p-3 text-slate-700">Meta WhatsApp</td>
                        <td className="p-3 text-amber-700 font-medium">🔥 Aquecimento + avanço</td>
                      </tr>
                      <tr className="bg-blue-50">
                        <td className="p-3">
                          <Tooltip
                            content="Cliente curioso, só pesquisando, sem urgência"
                            source="Comportamento: vê post, não responde perguntas-chave"
                          >
                            <span className="flex items-center gap-2">
                              <span className="w-3 h-3 bg-blue-500 rounded-full"></span>
                              <strong className="text-blue-800">Baixa intenção</strong>
                            </span>
                          </Tooltip>
                        </td>
                        <td className="p-3 text-slate-700">Meta Branding / Instagram</td>
                        <td className="p-3 text-blue-700 font-medium">💭 Construção de desejo</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Modelo de 3 Pistas */}
              <div className="pb-6 border-b">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">🔥 Modelo de 3 Pistas</h3>
                <p className="text-slate-600 mb-4">
                  Cada lead recebe tratamento diferente conforme sua temperatura:
                </p>
                <div className="grid md:grid-cols-3 gap-4">
                  {/* Pista 1 - Quente */}
                  <div className="bg-emerald-50 border-2 border-emerald-200 rounded-xl p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="w-4 h-4 bg-emerald-500 rounded-full"></span>
                      <h4 className="font-bold text-emerald-800">PISTA 1 — Quente</h4>
                    </div>
                    <p className="text-sm text-emerald-700 mb-3">Google Search / Site</p>
                    <ul className="text-xs text-emerald-600 space-y-1">
                      <li>• Vai direto para fechamento</li>
                      <li>• Script curto e objetivo</li>
                      <li>• Vendedor com melhor taxa</li>
                    </ul>
                    <div className="mt-4 pt-3 border-t border-emerald-200">
                      <p className="text-xs font-medium text-emerald-800">Meta: <span className="text-emerald-600">fechar rápido</span></p>
                    </div>
                  </div>

                  {/* Pista 2 - Morno */}
                  <div className="bg-amber-50 border-2 border-amber-200 rounded-xl p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="w-4 h-4 bg-amber-500 rounded-full"></span>
                      <h4 className="font-bold text-amber-800">PISTA 2 — Morno</h4>
                    </div>
                    <p className="text-sm text-amber-700 mb-3">Meta WhatsApp</p>
                    <ul className="text-xs text-amber-600 space-y-1">
                      <li>• Script de descoberta</li>
                      <li>• Apresentar opções</li>
                      <li>• Test drive, simulação</li>
                    </ul>
                    <div className="mt-4 pt-3 border-t border-amber-200">
                      <p className="text-xs font-medium text-amber-800">Meta: <span className="text-amber-600">aquecer + avançar</span></p>
                    </div>
                    <div className="mt-2 bg-amber-100 rounded-lg p-2">
                      <p className="text-[10px] text-amber-700">⚡ Aqui está onde se ganha volume</p>
                    </div>
                  </div>

                  {/* Pista 3 - Frio */}
                  <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="w-4 h-4 bg-blue-500 rounded-full"></span>
                      <h4 className="font-bold text-blue-800">PISTA 3 — Frio</h4>
                    </div>
                    <p className="text-sm text-blue-700 mb-3">Branding / Instagram</p>
                    <ul className="text-xs text-blue-600 space-y-1">
                      <li>• NÃO passa direto pro vendedor</li>
                      <li>• Resposta automática (IA)</li>
                      <li>• Pergunta de intenção</li>
                    </ul>
                    <div className="mt-4 pt-3 border-t border-blue-200">
                      <p className="text-xs font-medium text-blue-800">Meta: <span className="text-blue-600">preparar, não vender</span></p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Regra de Ouro */}
              <div className="pb-6 border-b">
                <div className="bg-gradient-to-r from-rose-50 to-orange-50 border border-rose-200 rounded-xl p-5">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="text-2xl">📌</span>
                    <h4 className="font-bold text-rose-800 text-lg">Regra de Ouro</h4>
                  </div>
                  <p className="text-rose-700 font-medium mb-3">
                    "Vendedor só recebe lead quando existe ação possível. IA cuida do resto."
                  </p>
                  <div className="grid md:grid-cols-3 gap-3 text-sm">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      <span className="text-slate-600">Protege conversão</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      <span className="text-slate-600">Protege moral do time</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      <span className="text-slate-600">Melhora CPV real</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Briefing para Criativos */}
              <div className="pb-6 border-b">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">🎨 Briefing para Criativos</h3>
                <p className="text-slate-600 mb-4">
                  O branding deve funcionar como <strong>pré-venda silenciosa</strong>, não isolado do comercial:
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="bg-slate-50 rounded-xl p-4 border">
                    <p className="font-medium text-slate-900 mb-2">🔹 Conteúdo com Filtro Embutido</p>
                    <ul className="text-sm text-slate-600 space-y-2">
                      <li>"Quem compra carro assim é quem..."</li>
                      <li>"Esse carro não é pra quem..."</li>
                      <li>"Esse perfil de cliente normalmente procura..."</li>
                    </ul>
                    <p className="text-xs text-slate-500 mt-3 pt-3 border-t">
                      👉 Afasta curioso e atrai comprador real
                    </p>
                  </div>
                  <div className="bg-slate-50 rounded-xl p-4 border">
                    <p className="font-medium text-slate-900 mb-2">🔹 Reforço de Autoridade</p>
                    <ul className="text-sm text-slate-600 space-y-2">
                      <li>Pós-venda e garantia</li>
                      <li>Bastidores da loja</li>
                      <li>Processos de qualidade</li>
                      <li>Transparência</li>
                    </ul>
                    <p className="text-xs text-slate-500 mt-3 pt-3 border-t">
                      👉 Lead chega menos defensivo
                    </p>
                  </div>
                </div>
              </div>

              {/* Resultado Esperado */}
              <div>
                <h3 className="text-lg font-semibold text-slate-900 mb-4">📈 Resultado Esperado (Realista)</h3>
                <p className="text-slate-600 mb-4">
                  Com esse modelo, <strong>sem aumentar mídia</strong>:
                </p>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-emerald-100">
                        <th className="text-left p-3 font-semibold text-emerald-800 rounded-tl-lg">Ação</th>
                        <th className="text-right p-3 font-semibold text-emerald-800 rounded-tr-lg">Impacto Estimado</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      <tr>
                        <td className="p-3 text-slate-700">Melhor progressão do lead (pistas)</td>
                        <td className="p-3 text-right text-emerald-600 font-medium">+2 a +3 vendas/mês</td>
                      </tr>
                      <tr>
                        <td className="p-3 text-slate-700">Melhor uso do Meta (qualificação)</td>
                        <td className="p-3 text-right text-emerald-600 font-medium">+2 vendas/mês</td>
                      </tr>
                      <tr>
                        <td className="p-3 text-slate-700">Menos desgaste do vendedor</td>
                        <td className="p-3 text-right text-emerald-600 font-medium">+1 venda/mês</td>
                      </tr>
                      <tr>
                        <td className="p-3 text-slate-700">Branding mais filtrador</td>
                        <td className="p-3 text-right text-emerald-600 font-medium">+1 venda/mês</td>
                      </tr>
                      <tr className="bg-emerald-50">
                        <td className="p-3 font-bold text-slate-900">Total Realista</td>
                        <td className="p-3 text-right font-bold text-emerald-700">+6 a +8 vendas/mês</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div className="mt-4 bg-amber-50 border border-amber-200 rounded-lg p-4">
                  <p className="text-sm text-amber-800">
                    👆 Isso é <strong>crescimento real</strong>, não PowerPoint. Meta inicial: +4 vendas/mês, revisar em 60 dias.
                  </p>
                </div>
              </div>

            </div>
          </div>
        </section>

        {/* Próximos Passos - Otimização Avançada */}
        <section>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
              <Rocket className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">Próximos Passos</h2>
              <p className="text-slate-500">Otimizações avançadas para implementar com a agência</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
            <div className="p-6 space-y-6">
              
              {/* Métricas Faltantes */}
              <div className="pb-6 border-b">
                <div className="flex items-center gap-3 mb-4">
                  <FileSearch className="w-5 h-5 text-purple-600" />
                  <h3 className="text-lg font-semibold text-slate-900">Métricas que Precisamos Acompanhar</h3>
                </div>
                <p className="text-slate-600 mb-4">
                  Para ter uma visão completa do funil, precisamos cobrar da agência as seguintes métricas que estão faltando:
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="p-4 bg-purple-50 rounded-xl border border-purple-100">
                    <Tooltip 
                      content="Percentual de pessoas que clicam no anúncio após vê-lo"
                      formula="(Cliques / Impressões) × 100"
                      source="Meta Ads / Google Ads - relatório de campanha"
                    >
                      <p className="font-medium text-purple-900 mb-1">CTR (Click-Through Rate)</p>
                    </Tooltip>
                    <p className="text-sm text-purple-700">Criativo atrativo? Público certo?</p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-xl border border-purple-100">
                    <Tooltip 
                      content="Quantas vezes em média o mesmo usuário viu o anúncio"
                      formula="Impressões / Alcance"
                      source="Meta Ads / Google Ads - relatório de frequência"
                    >
                      <p className="font-medium text-purple-900 mb-1">Frequência</p>
                    </Tooltip>
                    <p className="text-sm text-purple-700">Acima de 3x indica saturação</p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-xl border border-purple-100">
                    <Tooltip 
                      content="Tempo entre chegada do lead e primeira resposta do vendedor"
                      formula="Hora primeira mensagem - Hora entrada lead"
                      source="CRM - histórico de atividades"
                    >
                      <p className="font-medium text-purple-900 mb-1">Tempo de Resposta (SLA)</p>
                    </Tooltip>
                    <p className="text-sm text-purple-700">Responder em 5min aumenta conversão 9x</p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-xl border border-purple-100">
                    <Tooltip 
                      content="Qual anúncio específico gera mais vendas, não só cliques"
                      formula="Vendas por criativo / Custo por criativo"
                      source="UTMs + CRM cruzado com relatório da agência"
                    >
                      <p className="font-medium text-purple-900 mb-1">Performance por Criativo</p>
                    </Tooltip>
                    <p className="text-sm text-purple-700">Qual anúncio converte mais?</p>
                  </div>
                </div>
              </div>

              {/* Implementações Técnicas */}
              <div className="pb-6 border-b">
                <div className="flex items-center gap-3 mb-4">
                  <Wrench className="w-5 h-5 text-blue-600" />
                  <h3 className="text-lg font-semibold text-slate-900">Implementações Técnicas</h3>
                </div>
                <div className="space-y-4">
                  <div className="flex items-start gap-4 p-4 bg-blue-50 rounded-xl border border-blue-100">
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center shrink-0">
                      <RefreshCw className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-blue-900">API de Conversões Offline</h4>
                      <p className="text-sm text-blue-700 mt-1">
                        Integrar vendas do CRM de volta para Meta e Google. O algoritmo passa a otimizar para quem <strong>compra</strong>, não só quem clica.
                        Isso pode reduzir o CPV em até 30%.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-4 p-4 bg-emerald-50 rounded-xl border border-emerald-100">
                    <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center shrink-0">
                      <Users className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-emerald-900">Lookalike de Compradores</h4>
                      <p className="text-sm text-emerald-700 mt-1">
                        Criar público similar baseado em quem <strong>já comprou</strong>, não em quem só clicou.
                        Meta e Google podem encontrar pessoas parecidas com seus melhores clientes.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-4 p-4 bg-amber-50 rounded-xl border border-amber-100">
                    <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center shrink-0">
                      <Bot className="w-5 h-5 text-amber-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-amber-900">Qualificação Automatizada</h4>
                      <p className="text-sm text-amber-700 mt-1">
                        Chatbot no WhatsApp perguntando: "Qual seu orçamento?", "Tem entrada?", "Precisa financiar?".
                        Só passa para o vendedor quem responde corretamente, filtrando curiosos.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Remarketing */}
              <div className="pb-6 border-b">
                <div className="flex items-center gap-3 mb-4">
                  <Target className="w-5 h-5 text-indigo-600" />
                  <h3 className="text-lg font-semibold text-slate-900">Estrutura de Remarketing</h3>
                </div>
                <p className="text-slate-600 mb-4">
                  Criar sequência de anúncios para pessoas que já interagiram mas não converteram:
                </p>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-slate-50">
                        <th className="text-left p-3 font-medium text-slate-700">Público</th>
                        <th className="text-left p-3 font-medium text-slate-700">Anúncio</th>
                        <th className="text-left p-3 font-medium text-slate-700">Objetivo</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      <tr>
                        <td className="p-3 text-slate-600">Visitou site, não mandou mensagem</td>
                        <td className="p-3 text-slate-900">Vídeo do veículo específico</td>
                        <td className="p-3 text-indigo-600">Reengajar</td>
                      </tr>
                      <tr>
                        <td className="p-3 text-slate-600">Mandou mensagem, não agendou</td>
                        <td className="p-3 text-slate-900">"Agende sua visita hoje"</td>
                        <td className="p-3 text-indigo-600">Converter</td>
                      </tr>
                      <tr>
                        <td className="p-3 text-slate-600">Visitou loja, não comprou</td>
                        <td className="p-3 text-slate-900">Oferta especial personalizada</td>
                        <td className="p-3 text-indigo-600">Fechar</td>
                      </tr>
                      <tr>
                        <td className="p-3 text-slate-600">Comprou há 2+ anos</td>
                        <td className="p-3 text-slate-900">"Hora de trocar seu carro?"</td>
                        <td className="p-3 text-indigo-600">Recompra</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Perguntas para a Agência */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <MessageCircle className="w-5 h-5 text-rose-600" />
                  <h3 className="text-lg font-semibold text-slate-900">Perguntas para Fazer na Reunião</h3>
                </div>
                <div className="space-y-3">
                  {[
                    "Qual o CTR médio das campanhas? Está acima de 1%?",
                    "Qual a frequência dos anúncios? Estão saturando o público?",
                    "Vocês já usam API de Conversões Offline?",
                    "Qual criativo específico gera mais VENDAS, não só cliques?",
                    "O lookalike é baseado em compradores ou só em leads?",
                    "Temos remarketing estruturado por etapa do funil?",
                  ].map((pergunta, i) => (
                    <div key={i} className="flex items-center gap-3 p-3 bg-rose-50 rounded-lg border border-rose-100">
                      <span className="w-6 h-6 bg-rose-200 text-rose-700 rounded-full flex items-center justify-center text-xs font-bold shrink-0">
                        {i + 1}
                      </span>
                      <p className="text-sm text-rose-800">{pergunta}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Observação Final */}
          <div className="mt-6 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-6 border border-indigo-100">
            <div className="flex items-start gap-4">
              <Lightbulb className="w-6 h-6 text-indigo-600 shrink-0 mt-1" />
              <div>
                <h4 className="font-semibold text-indigo-900">Observação Final</h4>
                <p className="text-indigo-800 mt-2">
                  As otimizações técnicas acima podem representar uma <strong>redução de 20-40% no CPV</strong> quando bem implementadas.
                  A integração de conversões offline é especialmente crítica: sem ela, Meta e Google otimizam para cliques, não para vendas reais.
                </p>
                <p className="text-indigo-800 mt-3">
                  <strong>Recomendação:</strong> Solicitar à agência um cronograma de implementação dessas melhorias nos próximos 30-60 dias,
                  com checkpoints semanais para acompanhamento.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="text-center text-sm text-slate-400 pt-8 border-t">
          <p>Netcar × Voren • Relatório de Alinhamento • Janeiro 2026</p>
        </footer>

      </div>
    </div>
  );
}
