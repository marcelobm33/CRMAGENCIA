import json
import os
from datetime import datetime, timezone
from urllib.request import urlopen, Request


API_BASE = os.getenv("PUBLIC_REPORT_API_BASE", "http://localhost:8000")
OUT_FILE = os.getenv(
    "PUBLIC_REPORT_OUT",
    os.path.join(os.path.dirname(__file__), "..", "public", "public-report.json"),
)
# Nome neutro (ou vazio para omitir)
BRAND = os.getenv("PUBLIC_REPORT_BRAND", "")


def fetch_json(path: str):
    url = f"{API_BASE}{path}"
    req = Request(url, headers={"Accept": "application/json"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    consolidado = fetch_json("/api/roi/consolidado")
    qualidade = fetch_json("/api/roi/qualidade-leads")

    # Sanitização: não exportar lista de vendas, nomes de clientes, etc.
    top_motivos = []
    for m in (qualidade.get("motivos_perda") or [])[:2]:
        top_motivos.append({"motivo": m.get("motivo"), "percentual": m.get("percentual")})

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "periodo": consolidado.get("periodo"),
        "roi": {
            "investimento_total": consolidado.get("investimento_total", 0),
            "leads_agencia": consolidado.get("leads_agencia", 0),
            "leads_crm": consolidado.get("leads_crm", 0),
            "vendas_crm": consolidado.get("vendas_crm", 0),
            "valor_vendido": consolidado.get("valor_vendido", 0),
            "custo_por_lead_real": consolidado.get("custo_por_lead_real", 0),
            "custo_por_venda": consolidado.get("custo_por_venda", 0),
            "roi_percentual": consolidado.get("roi_percentual", 0),
            "meta": {
                "investimento": (consolidado.get("meta") or {}).get("investimento", 0),
                "leads_crm": (consolidado.get("meta") or {}).get("leads_crm", 0),
                "vendas": (consolidado.get("meta") or {}).get("vendas", 0),
                "valor_vendido": (consolidado.get("meta") or {}).get("valor_vendido", 0),
                "roi": (consolidado.get("meta") or {}).get("roi", 0),
            },
            "google": {
                "investimento": (consolidado.get("google") or {}).get("investimento", 0),
                "leads_crm": (consolidado.get("google") or {}).get("leads_crm", 0),
                "vendas": (consolidado.get("google") or {}).get("vendas", 0),
                "valor_vendido": (consolidado.get("google") or {}).get("valor_vendido", 0),
                "roi": (consolidado.get("google") or {}).get("roi", 0),
            },
        },
        "qualidade": {
            "resumo_midia": {
                "total_leads": (qualidade.get("resumo_midia") or {}).get("total_leads", 0),
                "ganhos": (qualidade.get("resumo_midia") or {}).get("ganhos", 0),
                "perdidos": (qualidade.get("resumo_midia") or {}).get("perdidos", 0),
                "taxa_conversao": (qualidade.get("resumo_midia") or {}).get("taxa_conversao", 0),
                "custo_por_venda": (qualidade.get("resumo_midia") or {}).get("custo_por_venda", 0),
            },
            "leads_frios_percentual": qualidade.get("leads_frios_percentual", 0),
            "top_motivos_perda": top_motivos,
        },
        "proposta": {
            "decisao": "Manter por 14–30 dias com condição (qualidade), ou reduzir e realocar.",
            "cobrancas_7_dias": [
                "Separar campanhas por intenção (Search alta intenção + remarketing).",
                "Filtrar curioso no anúncio (preço/entrada/análise de crédito).",
                "Relatório de qualidade: % válidos, % respondidos, % qualificados, % agendamentos, % vendas.",
                "UTMs e padrão no CRM (origem e canal).",
            ],
            "realocacao": [
                "Google Search (alta intenção) + remarketing",
                "Meta remarketing + criativos com filtro",
                "Programa de indicação + parcerias",
            ],
            "kpis_para_decidir": [
                "% Qualificados (SDR) / total leads",
                "% Agendamentos / qualificados",
                "Custo por venda (CRM) por canal",
                "\"Não responde\" + SLA de 1ª resposta",
            ],
        },
    }
    if BRAND:
        report["brand"] = BRAND

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"✅ public-report.json gerado em: {os.path.abspath(OUT_FILE)}")


if __name__ == "__main__":
    main()

