'use client';

import { useState, useEffect } from 'react';
import { 
  AlertTriangle,
  TrendingDown,
  TrendingUp,
  Users,
  DollarSign,
  Target,
  ThumbsDown,
  ThumbsUp,
  Zap,
  RefreshCw,
  Award,
  XCircle,
  CheckCircle2,
  MessageCircle,
  Clock
} from 'lucide-react';

interface QualidadeData {
  periodo: string;
  investimento_total: number;
  resumo_midia: {
    total_leads: number;
    ganhos: number;
    perdidos: number;
    em_andamento: number;
    taxa_conversao: number;
    custo_por_lead: number;
    custo_por_venda: number;
  };
  comparativo_indicacao: {
    total_leads: number;
    ganhos: number;
    perdidos: number;
    taxa_conversao: number;
    custo: number;
    multiplicador: number;
  };
  origens: Array<{
    fonte: string;
    total_leads: number;
    ganhos: number;
    perdidos: number;
    taxa_conversao: number;
    valor_vendido: number;
    qualidade: string;
  }>;
  motivos_perda: Array<{
    motivo: string;
    quantidade: number;
    percentual: number;
  }>;
  leads_frios_percentual: number;
  vendedores: Array<{
    vendedor: string;
    total_leads: number;
    ganhos: number;
    perdidos: number;
    taxa_conversao: number;
  }>;
  alertas: string[];
  recomendacoes: Array<{
    acao: string;
    motivo: string;
    prioridade: string;
  }>;
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

export default function QualidadeLeadsPage() {
  const [data, setData] = useState<QualidadeData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/roi/qualidade-leads');
      if (response.ok) {
        const result = await response.json();
        setData(result);
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
        <p className="text-gray-500">Dados não disponíveis</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">
          Análise de Qualidade de Leads
        </h1>
        <p className="text-gray-500 mt-2">
          Período: {data.periodo} | Investimento: {formatCurrency(data.investimento_total)}
        </p>
      </div>

      {/* Alerta Principal */}
      <div className="bg-gradient-to-r from-red-500 to-red-600 rounded-2xl p-8 text-white">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-white/20 rounded-xl">
            <AlertTriangle className="w-8 h-8" />
          </div>
          <div>
            <h2 className="text-2xl font-bold">Problema Identificado</h2>
            <p className="mt-2 text-white/90 text-lg">
              De cada <span className="font-bold text-3xl">100</span> leads de mídia paga, 
              apenas <span className="font-bold text-3xl">{Math.round(data.resumo_midia.taxa_conversao)}</span> viram vendas.
            </p>
            <p className="mt-1 text-white/80">
              A equipe trabalhou <strong>{formatNumber(data.resumo_midia.perdidos)}</strong> leads sem resultado.
            </p>
          </div>
        </div>
      </div>

      {/* KPIs Impactantes */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border p-6 text-center">
          <div className="w-12 h-12 mx-auto bg-red-100 rounded-full flex items-center justify-center mb-3">
            <TrendingDown className="w-6 h-6 text-red-600" />
          </div>
          <p className="text-4xl font-bold text-red-600">{data.resumo_midia.taxa_conversao}%</p>
          <p className="text-sm text-gray-500 mt-1">Taxa Conversão<br/>Mídia Paga</p>
        </div>
        
        <div className="bg-white rounded-xl border p-6 text-center">
          <div className="w-12 h-12 mx-auto bg-emerald-100 rounded-full flex items-center justify-center mb-3">
            <TrendingUp className="w-6 h-6 text-emerald-600" />
          </div>
          <p className="text-4xl font-bold text-emerald-600">{data.comparativo_indicacao.taxa_conversao}%</p>
          <p className="text-sm text-gray-500 mt-1">Taxa Conversão<br/>Indicação</p>
        </div>
        
        <div className="bg-white rounded-xl border p-6 text-center">
          <div className="w-12 h-12 mx-auto bg-amber-100 rounded-full flex items-center justify-center mb-3">
            <XCircle className="w-6 h-6 text-amber-600" />
          </div>
          <p className="text-4xl font-bold text-amber-600">{data.resumo_midia.perdidos}</p>
          <p className="text-sm text-gray-500 mt-1">Leads Perdidos<br/>(Esforço Desperdiçado)</p>
        </div>
        
        <div className="bg-white rounded-xl border p-6 text-center">
          <div className="w-12 h-12 mx-auto bg-purple-100 rounded-full flex items-center justify-center mb-3">
            <DollarSign className="w-6 h-6 text-purple-600" />
          </div>
          <p className="text-4xl font-bold text-purple-600">{formatCurrency(data.resumo_midia.custo_por_venda)}</p>
          <p className="text-sm text-gray-500 mt-1">Custo por Venda<br/>Real</p>
        </div>
      </div>

      {/* Comparativo Visual Mídia vs Indicação */}
      <div className="bg-white rounded-2xl border overflow-hidden">
        <div className="bg-gray-900 px-6 py-4">
          <h3 className="text-xl font-bold text-white">Comparativo: Mídia Paga vs Indicação</h3>
        </div>
        
        <div className="p-6">
          <div className="grid lg:grid-cols-2 gap-8">
            {/* Mídia Paga */}
            <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-xl p-6 border-2 border-red-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center">
                  <ThumbsDown className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h4 className="font-bold text-gray-900">Mídia Paga (Agência)</h4>
                  <p className="text-sm text-red-600">Baixa qualidade</p>
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Leads recebidos</span>
                  <span className="text-2xl font-bold">{data.resumo_midia.total_leads}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Vendas fechadas</span>
                  <span className="text-2xl font-bold text-emerald-600">{data.resumo_midia.ganhos}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Taxa de conversão</span>
                  <span className="text-2xl font-bold text-red-600">{data.resumo_midia.taxa_conversao}%</span>
                </div>
                <div className="flex justify-between items-center pt-4 border-t">
                  <span className="text-gray-600">Investimento</span>
                  <span className="text-xl font-bold">{formatCurrency(data.investimento_total)}</span>
                </div>
              </div>
            </div>
            
            {/* Indicação */}
            <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl p-6 border-2 border-emerald-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-emerald-500 rounded-lg flex items-center justify-center">
                  <ThumbsUp className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h4 className="font-bold text-gray-900">Indicação</h4>
                  <p className="text-sm text-emerald-600">Alta qualidade</p>
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Leads recebidos</span>
                  <span className="text-2xl font-bold">{data.comparativo_indicacao.total_leads}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Vendas fechadas</span>
                  <span className="text-2xl font-bold text-emerald-600">{data.comparativo_indicacao.ganhos}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Taxa de conversão</span>
                  <span className="text-2xl font-bold text-emerald-600">{data.comparativo_indicacao.taxa_conversao}%</span>
                </div>
                <div className="flex justify-between items-center pt-4 border-t">
                  <span className="text-gray-600">Investimento</span>
                  <span className="text-xl font-bold text-emerald-600">R$ 0</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Destaque do multiplicador */}
          <div className="mt-6 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl p-6 text-center text-white">
            <Zap className="w-12 h-12 mx-auto mb-2" />
            <p className="text-3xl font-bold">
              Indicação converte {data.comparativo_indicacao.multiplicador}x MAIS
            </p>
            <p className="text-emerald-100 mt-1">e com custo ZERO de mídia!</p>
          </div>
        </div>
      </div>

      {/* O que fazer agora (plano de ação) */}
      <div className="bg-white rounded-2xl border overflow-hidden">
        <div className="bg-gradient-to-r from-gray-900 to-gray-800 px-6 py-4">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <Target className="w-6 h-6" />
            Plano para melhorar ROI (o que fazer agora)
          </h3>
          <p className="text-sm text-white/70 mt-1">
            Foco: reduzir leads frios ({data.leads_frios_percentual}%) e aliviar a equipe (perdidos: {formatNumber(data.resumo_midia.perdidos)}).
          </p>
        </div>

        <div className="p-6 space-y-6">
          <div className="grid lg:grid-cols-2 gap-4">
            <div className="rounded-xl border bg-emerald-50 border-emerald-100 p-5">
              <h4 className="font-bold text-emerald-900 flex items-center gap-2">
                <Zap className="w-5 h-5" />
                Próximos 7 dias (maior impacto)
              </h4>
              <ul className="mt-3 space-y-2 text-sm text-gray-700">
                <li><strong>SDR / pré-vendas</strong> (ou rodízio): qualificar em <strong>2–5 min</strong> e só então passar ao vendedor.</li>
                <li><strong>Regra de qualificação</strong>: modelo + faixa de preço + entrada/financiamento + prazo + cidade.</li>
                <li><strong>Playbook anti “não responde”</strong>: 6 tentativas em 48h (WhatsApp + ligação + áudio curto).</li>
                <li><strong>Mensagem inicial padrão</strong>: 1 pergunta fechada + 2 opções (“prefere X ou Y?”).</li>
              </ul>
            </div>

            <div className="rounded-xl border bg-amber-50 border-amber-100 p-5">
              <h4 className="font-bold text-amber-900 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                Cobrança imediata da agência (7 dias)
              </h4>
              <ul className="mt-3 space-y-2 text-sm text-gray-700">
                <li><strong>Separar por intenção</strong>: Meta (mensagem/WhatsApp + remarketing) e Google (Search alta intenção).</li>
                <li><strong>Filtrar curioso</strong> no anúncio: “a partir de”, entrada mínima, análise de crédito.</li>
                <li><strong>Relatório de qualidade</strong>: % leads válidos, % respondidos, % qualificados, % agendamentos, % vendas.</li>
                <li><strong>UTMs/campos CRM</strong>: garantir origem/canal corretos pra não “sumir venda”.</li>
              </ul>
            </div>
          </div>

          <div className="grid lg:grid-cols-3 gap-4">
            <div className="rounded-xl border bg-white p-5">
              <h4 className="font-bold text-gray-900 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-emerald-600" />
                Plano 30 dias (escala)
              </h4>
              <ul className="mt-3 space-y-2 text-sm text-gray-700">
                <li><strong>SDR fixo</strong> + SLA de resposta &lt; 5 min.</li>
                <li><strong>Remarketing</strong> (Meta/Google) focado em quem interagiu/consultou.</li>
                <li><strong>Landing/WhatsApp</strong> com perguntas de qualificação (entrada, faixa, modelo).</li>
                <li><strong>Treinar time</strong> com o melhor conversor de lead frio do período.</li>
              </ul>
            </div>

            <div className="rounded-xl border bg-white p-5">
              <h4 className="font-bold text-gray-900 flex items-center gap-2">
                <ThumbsUp className="w-5 h-5 text-emerald-600" />
                Alternativas de venda (custo baixo)
              </h4>
              <ul className="mt-3 space-y-2 text-sm text-gray-700">
                <li><strong>Programa de indicação</strong>: bônus por venda (cliente + ex-cliente + parceiros).</li>
                <li><strong>Parcerias locais</strong>: oficinas, despachantes, seguradoras, frotistas pequenos.</li>
                <li><strong>Reativação</strong>: trabalhar perdidos/andamento com oferta e condição.</li>
              </ul>
            </div>

            <div className="rounded-xl border bg-white p-5">
              <h4 className="font-bold text-gray-900 flex items-center gap-2">
                <Users className="w-5 h-5 text-indigo-600" />
                Metas semanais (pra decidir manter/cortar)
              </h4>
              <ul className="mt-3 space-y-2 text-sm text-gray-700">
                <li><strong>% Qualificados</strong> (SDR) / total leads</li>
                <li><strong>% Agendamentos</strong> / qualificados</li>
                <li><strong>Custo por venda real</strong> (CRM) por canal</li>
                <li><strong>Taxa “não responde”</strong> e tempo médio de 1ª resposta</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Por que estamos perdendo? */}
      <div className="bg-white rounded-2xl border overflow-hidden">
        <div className="bg-amber-500 px-6 py-4">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <XCircle className="w-6 h-6" />
            Por que estamos perdendo leads?
          </h3>
        </div>
        
        <div className="p-6">
          <div className="mb-4">
            <div className="inline-flex items-center gap-2 bg-red-100 text-red-700 px-4 py-2 rounded-full text-sm font-medium">
              <AlertTriangle className="w-4 h-4" />
              {data.leads_frios_percentual}% dos leads são FRIOS (sem interesse ou não respondem)
            </div>
          </div>
          
          <div className="space-y-3">
            {data.motivos_perda.map((motivo, i) => (
              <div key={i} className="flex items-center gap-4">
                <div className="w-40 text-sm text-gray-600 truncate">{motivo.motivo}</div>
                <div className="flex-1">
                  <div className="bg-gray-100 rounded-full h-8 overflow-hidden">
                    <div 
                      className={`h-full rounded-full flex items-center px-3 transition-all ${
                        i === 0 || i === 1 ? 'bg-red-500' : 'bg-amber-400'
                      }`}
                      style={{ width: `${Math.max(motivo.percentual, 10)}%` }}
                    >
                      <span className="text-white text-sm font-medium whitespace-nowrap">
                        {motivo.quantidade} ({motivo.percentual}%)
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-6 grid grid-cols-2 gap-4">
            <div className="bg-red-50 rounded-xl p-4 border border-red-100">
              <div className="flex items-center gap-2 text-red-700 font-medium mb-2">
                <MessageCircle className="w-5 h-5" />
                "Sem Interesse"
              </div>
              <p className="text-sm text-gray-600">
                Lead não estava buscando carro. Problema de segmentação da agência.
              </p>
            </div>
            <div className="bg-red-50 rounded-xl p-4 border border-red-100">
              <div className="flex items-center gap-2 text-red-700 font-medium mb-2">
                <Clock className="w-5 h-5" />
                "Não Responde"
              </div>
              <p className="text-sm text-gray-600">
                Lead esfriou. Tempo de resposta pode estar longo demais.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Comparativo por Origem */}
      <div className="bg-white rounded-2xl border overflow-hidden">
        <div className="bg-gray-800 px-6 py-4">
          <h3 className="text-xl font-bold text-white">Qualidade por Origem</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-600">Origem</th>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-600">Leads</th>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-600">Vendas</th>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-600">Perdidos</th>
                <th className="px-6 py-4 text-right text-sm font-semibold text-gray-600">Taxa</th>
                <th className="px-6 py-4 text-center text-sm font-semibold text-gray-600">Qualidade</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {data.origens.map((origem, i) => (
                <tr key={i} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-900">{origem.fonte}</td>
                  <td className="px-6 py-4 text-right text-gray-600">{origem.total_leads}</td>
                  <td className="px-6 py-4 text-right font-semibold text-emerald-600">{origem.ganhos}</td>
                  <td className="px-6 py-4 text-right text-red-600">{origem.perdidos}</td>
                  <td className="px-6 py-4 text-right font-bold">{origem.taxa_conversao}%</td>
                  <td className="px-6 py-4 text-center">
                    <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${
                      origem.qualidade === 'alta' ? 'bg-emerald-100 text-emerald-700' :
                      origem.qualidade === 'media' ? 'bg-amber-100 text-amber-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {origem.qualidade === 'alta' ? '🟢 Alta' :
                       origem.qualidade === 'media' ? '🟡 Média' :
                       '🔴 Baixa'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Performance dos Vendedores */}
      <div className="bg-white rounded-2xl border overflow-hidden">
        <div className="bg-indigo-600 px-6 py-4">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <Users className="w-6 h-6" />
            Quem consegue converter lead frio?
          </h3>
        </div>
        
        <div className="p-6">
          <div className="grid lg:grid-cols-2 gap-4">
            {data.vendedores.map((vendedor, i) => (
              <div 
                key={i} 
                className={`rounded-xl p-4 border-2 ${
                  i === 0 ? 'bg-emerald-50 border-emerald-200' : 'bg-gray-50 border-gray-200'
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    {i === 0 && <Award className="w-5 h-5 text-emerald-600" />}
                    <span className="font-bold text-gray-900">{vendedor.vendedor}</span>
                  </div>
                  <span className={`text-2xl font-bold ${
                    vendedor.taxa_conversao >= 5 ? 'text-emerald-600' : 'text-gray-400'
                  }`}>
                    {vendedor.taxa_conversao}%
                  </span>
                </div>
                
                <div className="flex gap-4 text-sm">
                  <div>
                    <span className="text-gray-500">Leads:</span>
                    <span className="ml-1 font-medium">{vendedor.total_leads}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">Vendas:</span>
                    <span className="ml-1 font-medium text-emerald-600">{vendedor.ganhos}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">Perdidos:</span>
                    <span className="ml-1 font-medium text-red-600">{vendedor.perdidos}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recomendações */}
      <div className="bg-gradient-to-br from-indigo-600 to-purple-700 rounded-2xl p-8 text-white">
        <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <CheckCircle2 className="w-8 h-8" />
          Recomendações
        </h3>
        
        <div className="grid lg:grid-cols-2 gap-4">
          {data.recomendacoes.map((rec, i) => (
            <div key={i} className="bg-white/10 backdrop-blur rounded-xl p-5">
              <div className="flex items-start gap-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                  rec.prioridade === 'alta' ? 'bg-red-500' : 'bg-amber-500'
                }`}>
                  {i + 1}
                </div>
                <div>
                  <p className="font-semibold text-lg">{rec.acao}</p>
                  <p className="text-white/80 text-sm mt-1">{rec.motivo}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Conclusão Final */}
      <div className="bg-gray-900 rounded-2xl p-8 text-white">
        <h3 className="text-2xl font-bold mb-4">Conclusão</h3>
        <p className="text-xl text-gray-300 max-w-4xl">
          A equipe comercial está ocupada demais tentando converter leads <strong className="text-red-400">frios</strong> da agência.
          <br/><br/>
          Com <strong className="text-emerald-400">{data.resumo_midia.perdidos}</strong> leads perdidos e apenas <strong className="text-emerald-400">{data.resumo_midia.ganhos}</strong> vendas,
          o <strong className="text-amber-400">custo real por venda é {formatCurrency(data.resumo_midia.custo_por_venda)}</strong>.
          <br/><br/>
          Enquanto isso, <strong className="text-emerald-400">indicação converte {data.comparativo_indicacao.multiplicador}x mais</strong> com custo zero.
        </p>

        {/* Proposição objetiva para a verba da agência */}
        <div className="mt-8 grid lg:grid-cols-2 gap-6">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <h4 className="text-lg font-bold text-white">O que fazer com a verba da agência (proposta)</h4>
            <p className="text-sm text-gray-300 mt-2">
              Decisão prática: <strong className="text-white">manter com condição</strong> por 14–30 dias, ou <strong className="text-white">reduzir</strong> e realocar para canais de maior qualidade.
            </p>
            <ul className="mt-4 space-y-3 text-sm text-gray-300">
              <li>
                <strong className="text-white">1) Stop-loss imediato</strong>: não passar lead “cru” para vendedor. Tudo passa por SDR (2–5 min).
              </li>
              <li>
                <strong className="text-white">2) Re-negociação</strong>: manter a agência só se ela aceitar <strong className="text-white">meta por qualidade</strong>, não por volume.
              </li>
              <li>
                <strong className="text-white">3) Realocação de budget</strong>: reduzir Meta de “volume” e priorizar:
                <div className="mt-1 text-gray-400">
                  - <strong className="text-gray-200">Google Search</strong> (alta intenção) + <strong className="text-gray-200">remarketing</strong><br/>
                  - <strong className="text-gray-200">Meta remarketing</strong> e campanhas com filtro (preço/entrada)<br/>
                  - <strong className="text-gray-200">Programa de indicação</strong> (custo baixo, conversão alta)
                </div>
              </li>
            </ul>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <h4 className="text-lg font-bold text-white">Condições para continuar (o que cobrar)</h4>
            <div className="mt-4 grid grid-cols-2 gap-4">
              <div className="rounded-xl bg-black/20 p-4">
                <p className="text-xs text-gray-400 uppercase tracking-widest">KPI 1</p>
                <p className="text-sm font-semibold text-white mt-1">% Qualificados (SDR)</p>
                <p className="text-xs text-gray-400 mt-1">Se não subir, o lead segue frio e não vale o esforço do vendedor.</p>
              </div>
              <div className="rounded-xl bg-black/20 p-4">
                <p className="text-xs text-gray-400 uppercase tracking-widest">KPI 2</p>
                <p className="text-sm font-semibold text-white mt-1">% Agendamentos</p>
                <p className="text-xs text-gray-400 mt-1">Agendamento é o “sinal” de intenção real de compra.</p>
              </div>
              <div className="rounded-xl bg-black/20 p-4">
                <p className="text-xs text-gray-400 uppercase tracking-widest">KPI 3</p>
                <p className="text-sm font-semibold text-white mt-1">Custo por venda (CRM)</p>
                <p className="text-xs text-gray-400 mt-1">
                  Hoje: <strong className="text-amber-300">{formatCurrency(data.resumo_midia.custo_por_venda)}</strong>. Meta é reduzir com qualificação + intenção.
                </p>
              </div>
              <div className="rounded-xl bg-black/20 p-4">
                <p className="text-xs text-gray-400 uppercase tracking-widest">KPI 4</p>
                <p className="text-sm font-semibold text-white mt-1">“Não responde” + SLA</p>
                <p className="text-xs text-gray-400 mt-1">Exigir resposta &lt; 5 min e régua de contato.</p>
              </div>
            </div>

            <div className="mt-5 rounded-xl border border-amber-400/20 bg-amber-500/10 p-4">
              <p className="text-sm text-amber-100">
                <strong className="text-white">Regra de decisão:</strong> se em 14–30 dias os KPIs não melhorarem (mais qualificados, mais agendamentos e menor custo por venda),
                <strong className="text-white"> reduzir a verba e migrar para Search/remarketing + indicação</strong> ou trocar a agência.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
