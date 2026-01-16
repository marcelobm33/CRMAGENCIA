'use client';

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
} from 'lucide-react';

function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0,
  }).format(value);
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
                  <p className="text-xs text-slate-500 uppercase font-medium">Investimento Total</p>
                  <p className="text-2xl font-bold text-slate-900 mt-1">R$ 46.598</p>
                </div>
                <div className="bg-slate-50 rounded-xl p-4">
                  <p className="text-xs text-slate-500 uppercase font-medium">Leads no CRM</p>
                  <p className="text-2xl font-bold text-slate-900 mt-1">502</p>
                </div>
                <div className="bg-slate-50 rounded-xl p-4">
                  <p className="text-xs text-slate-500 uppercase font-medium">Vendas Atribuídas</p>
                  <p className="text-2xl font-bold text-slate-900 mt-1">37</p>
                </div>
                <div className="bg-slate-50 rounded-xl p-4">
                  <p className="text-xs text-slate-500 uppercase font-medium">Faturamento</p>
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
                    <p className="text-sm text-slate-500">ROI</p>
                    <p className="text-3xl font-bold text-emerald-600">9.521%</p>
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-slate-500">Conversão</p>
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
                    <span className="text-slate-600">Investimento</span>
                    <span className="font-medium text-slate-900">R$ 20.693</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-600">Vendas geradas</span>
                    <span className="font-medium text-slate-900">20 unidades</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-600">Custo por venda</span>
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
                    <p className="text-sm text-slate-500">Leads</p>
                    <p className="text-3xl font-bold text-blue-600">207</p>
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-slate-500">Conversão</p>
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
                    <span className="text-slate-600">Vendas geradas</span>
                    <span className="font-medium text-slate-900">19 unidades</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-600">% do total de vendas</span>
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
                    <p className="text-sm text-red-600 font-medium">Conversão</p>
                    <p className="text-3xl font-bold text-red-700">2,5%</p>
                    <p className="text-xs text-red-500 mt-1">vs 7,3% do Google</p>
                  </div>
                  <div className="text-center p-4 bg-red-50 rounded-xl">
                    <p className="text-sm text-red-600 font-medium">Custo por Venda</p>
                    <p className="text-3xl font-bold text-red-700">R$ 3.373</p>
                    <p className="text-xs text-red-500 mt-1">3x mais caro que Google</p>
                  </div>
                  <div className="text-center p-4 bg-red-50 rounded-xl">
                    <p className="text-sm text-red-600 font-medium">Vendas</p>
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
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-xl font-bold text-blue-700">57%</span>
                      </div>
                      <div>
                        <p className="font-semibold text-blue-900">Leads Frios</p>
                        <p className="text-sm text-blue-600">dos leads são perdidos por "Sem Interesse" ou "Não Responde"</p>
                      </div>
                    </div>
                  </div>
                  <div className="p-5 bg-slate-50 rounded-xl border border-slate-200">
                    <p className="font-semibold text-slate-900 mb-2">Principais motivos de perda:</p>
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
                      <p className="text-sm text-slate-500 mb-1">CPV atual (com atribuição)</p>
                      <p className="text-2xl font-bold text-slate-900">R$ 1.106</p>
                    </div>
                    <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-100">
                      <p className="text-sm text-emerald-600 mb-1">Meta sugerida</p>
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

        {/* Footer */}
        <footer className="text-center text-sm text-slate-400 pt-8 border-t">
          <p>Netcar × Voren • Relatório de Alinhamento • Janeiro 2026</p>
        </footer>

      </div>
    </div>
  );
}
