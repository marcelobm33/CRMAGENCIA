# Guia de Importação do CRM

Este guia explica como importar dados do seu CRM para o sistema.

## Formatos Suportados

- **CSV** (recomendado)
- **JSON**

## Modelo de CSV

### Download do Template

Baixe o template em branco: [template_crm.csv](../infra/seeds/template_crm.csv)

### Estrutura das Colunas

| Coluna | Tipo | Obrigatória | Descrição | Exemplo |
|--------|------|-------------|-----------|---------|
| vendedor | texto | **Sim** | Nome do vendedor | Carlos Silva |
| valor | número | Não | Valor do veículo | 85000 |
| lucro_bruto | número | Não | Lucro bruto estimado | 8500 |
| status | texto | Não | aberto, ganho, perdido | ganho |
| motivo_perda | texto | Não | Motivo se perdido | Preço alto |
| data_criacao | data | Não | Data do primeiro contato | 2024-01-15 |
| data_fechamento | data | Não | Data do fechamento | 2024-01-25 |
| telefone | texto | Não | Telefone do cliente | 11999887766 |
| email | texto | Não | Email do cliente | cliente@email.com |
| nome_cliente | texto | Não | Nome do cliente | João Santos |
| origem | texto | Não | Como chegou | Site |
| canal | texto | Não | Canal de marketing | Google |
| utm_source | texto | Não | Parâmetro UTM | google |
| utm_medium | texto | Não | Parâmetro UTM | cpc |
| utm_campaign | texto | Não | Parâmetro UTM | busca_seminovos |
| utm_content | texto | Não | Parâmetro UTM | anuncio_v2 |
| utm_term | texto | Não | Parâmetro UTM | carro usado sp |
| gclid | texto | Não | Google Click ID | abc123... |
| fbclid | texto | Não | Facebook Click ID | xyz789... |
| veiculo_interesse | texto | Não | Veículo desejado | Honda Civic 2022 |
| observacoes | texto | Não | Notas adicionais | Cliente retorna amanhã |

### Formatos de Data

O sistema aceita:
- `YYYY-MM-DD` (recomendado): 2024-01-15
- `DD/MM/YYYY`: 15/01/2024
- `YYYY-MM-DD HH:MM:SS`: 2024-01-15 14:30:00

### Formatos de Valor

O sistema aceita:
- Número simples: `85000`
- Com decimais: `85000.50`
- Com vírgula BR: `85.000,50`
- Com R$: `R$ 85.000,00`

### Status Permitidos

- `aberto` - Negociação em andamento
- `ganho` - Venda concluída
- `perdido` - Não converteu

## Exemplo de CSV

```csv
vendedor,valor,lucro_bruto,status,motivo_perda,data_criacao,telefone,email,nome_cliente,canal,utm_source,utm_campaign,veiculo_interesse
Carlos Silva,85000,8500,ganho,,2024-01-10,11999887766,joao@email.com,João Santos,Google,google,busca_seminovos,Honda Civic 2022
Maria Santos,0,0,perdido,Preço alto,2024-01-12,11988776655,ana@email.com,Ana Costa,Meta,facebook,leads_ofertas,VW Golf 2021
Pedro Souza,0,0,aberto,,2024-01-15,11977665544,carlos@email.com,Carlos Lima,Google,google,busca_financiamento,Toyota Corolla 2023
```

## Importando via Dashboard

1. Acesse **Configurações** > **Importar Dados**
2. Clique em **Selecionar arquivo**
3. Escolha seu arquivo CSV
4. Revise o preview dos dados
5. Clique em **Importar**

## Importando via API

### Com cURL

```bash
curl -X POST "http://localhost:8000/api/crm/import" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -F "file=@dados.csv"
```

### Resposta de Sucesso

```json
{
  "total_linhas": 100,
  "importados": 98,
  "erros": 2,
  "detalhes_erros": [
    {
      "linha": 45,
      "erro": "Campo 'vendedor' é obrigatório",
      "dados": {...}
    }
  ]
}
```

## Importação via JSON

### Estrutura

```json
[
  {
    "vendedor": "Carlos Silva",
    "valor": 85000,
    "status": "ganho",
    "data_criacao": "2024-01-10T10:30:00",
    "telefone": "11999887766",
    "nome_cliente": "João Santos",
    "canal": "Google",
    "utm_source": "google",
    "utm_campaign": "busca_seminovos",
    "veiculo_interesse": "Honda Civic 2022"
  }
]
```

### Via API

```bash
curl -X POST "http://localhost:8000/api/crm/deals" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"vendedor": "Carlos", "valor": 50000}]'
```

## Dicas para Importação

### UTMs para Atribuição

Para que o sistema relacione negócios com campanhas automaticamente, preencha:

1. **utm_source**: Origem (google, facebook, instagram)
2. **utm_campaign**: Nome da campanha

O sistema faz match automático entre `utm_campaign` do CRM e o nome da campanha nos Ads.

### Click IDs

Se você captura `gclid` (Google) ou `fbclid` (Facebook) nos formulários, inclua esses campos. Eles permitem atribuição mais precisa.

### Canal

Use valores padronizados:
- `Google` - Para Google Ads
- `Meta` - Para Facebook/Instagram Ads
- `Orgânico` - Busca orgânica
- `Direto` - Acesso direto
- `Indicação` - Indicação de clientes

### Motivos de Perda

Padronize os motivos para análises melhores:
- Preço alto
- Cliente não retornou
- Comprou em outro lugar
- Sem condições financeiras
- Desistiu da compra
- Veículo vendido
- Demora no atendimento

## Erros Comuns

### "Campo 'vendedor' é obrigatório"

Todo registro precisa ter um vendedor. Verifique se a coluna existe e está preenchida.

### "Status inválido"

Use apenas: `aberto`, `ganho` ou `perdido` (minúsculo).

### "Data inválida"

Verifique o formato da data. Use YYYY-MM-DD.

### "Encoding incorreto"

Salve o CSV em UTF-8. No Excel: Salvar como > CSV UTF-8.

## Exportando do Seu CRM

### RD Station CRM

1. Vá em Negócios > Exportar
2. Selecione os campos relevantes
3. Exporte como CSV
4. Renomeie as colunas conforme template

### Pipedrive

1. Vá em Deals > Export
2. Escolha os campos
3. Baixe CSV
4. Ajuste as colunas

### HubSpot

1. Vá em Deals > Actions > Export
2. Selecione propriedades
3. Exporte
4. Mapeie as colunas

### Planilha Manual

Se você usa planilha (Excel/Google Sheets):
1. Baixe o template
2. Preencha os dados
3. Salve como CSV (UTF-8)
4. Importe

## Importação Periódica

Para manter dados atualizados, você pode:

1. **Exportar do CRM** mensalmente/semanalmente
2. **Importar via API** com automação (Zapier, Make, etc.)
3. **Usar webhook** para sync em tempo real (requer desenvolvimento)

## Suporte

Se encontrar problemas na importação:

1. Verifique se o CSV está no formato correto
2. Confirme encoding UTF-8
3. Teste com poucas linhas primeiro
4. Verifique os logs de erro retornados

