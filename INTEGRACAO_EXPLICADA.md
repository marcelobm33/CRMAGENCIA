# 🔗 Como Funciona a Integração CRM + Campanhas

## Resumo Executivo

A integração conecta **3 fontes de dados** para gerar insights completos:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Meta Ads API  │     │ Google Ads API  │     │  CRM MySQL      │
│                 │     │                 │     │  (netcarrc01)   │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ • Impressões    │     │ • Impressões    │     │ • Leads         │
│ • Cliques       │     │ • Cliques       │     │ • Origem        │
│ • Gasto (R$)    │     │ • Gasto (R$)    │     │ • Vendas        │
│ • CPC           │     │ • CPC           │     │ • Receita       │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   Backend FastAPI      │
                    │  (Campaign Integrator) │
                    └────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  Métricas Calculadas   │
                    ├────────────────────────┤
                    │ • CAC (Custo/Lead)     │
                    │ • ROI (%)              │
                    │ • ROAS                 │
                    │ • Taxa Conversão       │
                    │ • Receita por Campanha │
                    └────────────────────────┘
```

---

## 🎯 Exemplo Prático

### Campanha: "Busca - Seminovos Premium" (Google Ads)

#### 1️⃣ Dados do Google Ads API
```json
{
  "campaign_id": "google_001",
  "name": "Busca - Seminovos Premium",
  "impressions": 65000,
  "clicks": 520,
  "spend": 1250.00,
  "cpc": 2.40
}
```

#### 2️⃣ Dados do CRM (netcarrc01)
```sql
SELECT 
    COUNT(*) as leads,
    SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) as vendas,
    SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) as receita
FROM crm_negocio
WHERE origem = 'GOOGLE'
  AND date_create >= '2025-11-01'
```

**Resultado:**
```json
{
  "leads": 45,
  "vendas": 12,
  "receita": 145000.00
}
```

#### 3️⃣ Métricas Calculadas
```javascript
// CAC (Custo de Aquisição por Cliente)
CAC = gasto / leads
CAC = 1250 / 45 = R$ 27,78

// Taxa de Conversão
Taxa = (vendas / leads) × 100
Taxa = (12 / 45) × 100 = 26,67%

// ROI (Return on Investment)
ROI = ((receita - gasto) / gasto) × 100
ROI = ((145000 - 1250) / 1250) × 100 = 11.500%

// ROAS (Return on Ad Spend)
ROAS = receita / gasto
ROAS = 145000 / 1250 = 116x
```

#### 4️⃣ Dashboard Final
```
┌──────────────────────────────────────────────────────────┐
│ 📊 Campanha: Busca - Seminovos Premium                  │
│ 🟢 Google Ads                                            │
├──────────────────────────────────────────────────────────┤
│ INVESTIMENTO                                             │
│   Gasto: R$ 1.250,00                                    │
│   Impressões: 65.000                                     │
│   Cliques: 520                                           │
│   CPC: R$ 2,40                                          │
│                                                          │
│ RESULTADO (do CRM)                                       │
│   Leads: 45                                              │
│   Vendas: 12                                             │
│   Receita: R$ 145.000,00                                │
│                                                          │
│ PERFORMANCE                                              │
│   CAC: R$ 27,78                                         │
│   Taxa Conversão: 26,67%                                │
│   ROI: 11.500% ⭐                                        │
│   ROAS: 116x                                            │
└──────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Sincronização

### Automático (a cada hora)
```python
# 1. Worker Celery executa
@celery.task
def sync_campaigns():
    # 2. Buscar dados do Meta Ads
    meta_campaigns = meta_api.get_campaigns()
    
    # 3. Buscar dados do Google Ads
    google_campaigns = google_api.get_campaigns()
    
    # 4. Para cada campanha:
    for campaign in meta_campaigns:
        # 4.1 Mapear origem no CRM
        crm_origin = map_platform_to_crm(campaign.platform)
        # "meta" → "FACEBOOK" ou "INSTAGRAM"
        
        # 4.2 Buscar leads do CRM
        crm_data = get_crm_leads(
            origin=crm_origin,
            start_date=campaign.start_date,
            end_date=campaign.end_date
        )
        
        # 4.3 Calcular métricas
        metrics = calculate_metrics(campaign, crm_data)
        
        # 4.4 Salvar no banco local
        save_campaign_metrics(campaign.id, metrics)
```

---

## 📊 Comparativo Meta vs Google

```
┌────────────────┬──────────────┬──────────────┐
│   Métrica      │     Meta     │    Google    │
├────────────────┼──────────────┼──────────────┤
│ Investimento   │  R$ 5.000    │  R$ 3.500    │
│ Impressões     │  290.000     │  232.000     │
│ Cliques        │  2.495       │  2.510       │
│ CTR            │  0,86%       │  1,08% ⭐    │
│                │              │              │
│ Leads (CRM)    │  105         │  59          │
│ CAC            │  R$ 47,62    │  R$ 59,32    │
│                │              │              │
│ Vendas (CRM)   │  33          │  12          │
│ Taxa Conv.     │  31,4% ⭐     │  20,3%       │
│                │              │              │
│ Receita (CRM)  │  R$ 4,5M     │  R$ 1,45M    │
│ ROI            │  89.900%     │  41.329%     │
│ ROAS           │  900x        │  414x        │
└────────────────┴──────────────┴──────────────┘

CONCLUSÃO:
✅ Meta: Melhor taxa de conversão e ROI
✅ Google: Melhor CTR e custo por clique
💡 Recomendação: Aumentar budget no Meta
```

---

## 🎯 Dashboards Disponíveis

### 1. Visão Geral
- Total investido
- Total de leads
- Total de vendas
- ROI geral

### 2. Por Campanha
- Lista de todas as campanhas
- Filtros por plataforma e status
- Ordenação por ROI, CAC, etc

### 3. Comparativo
- Meta vs Google lado a lado
- Gráficos de tendência
- Melhor/pior performance

### 4. Alertas
- Campanhas com ROI negativo
- Campanhas sem conversão
- Oportunidades de otimização

---

## 🔑 Próximos Passos

### Para Ativar a Integração Real:

1. **Meta Ads API**
   - Criar app no Meta for Developers
   - Obter Access Token
   - Configurar permissões (ads_read)

2. **Google Ads API**
   - Criar projeto no Google Cloud
   - Ativar Google Ads API
   - Obter credenciais OAuth 2.0

3. **Configurar no Sistema**
   ```bash
   # .env
   META_ACCESS_TOKEN=seu_token_aqui
   META_AD_ACCOUNT_ID=act_123456789
   
   GOOGLE_ADS_CLIENT_ID=seu_client_id
   GOOGLE_ADS_CLIENT_SECRET=seu_secret
   GOOGLE_ADS_REFRESH_TOKEN=seu_refresh_token
   GOOGLE_ADS_CUSTOMER_ID=123-456-7890
   ```

4. **Testar**
   ```bash
   # Sincronizar manualmente
   curl -X POST http://localhost:8000/api/campaigns/sync
   
   # Ver resultados
   curl http://localhost:8000/api/campaigns
   ```

---

**Documentação criada em:** 22/12/2025  
**Status:** Estrutura pronta, aguardando credenciais das APIs

