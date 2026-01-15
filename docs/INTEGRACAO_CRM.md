# 🔗 Integração com CRM Externo (netcarrc01)

Este documento explica como a integração com seu CRM existente funciona.

---

## 📊 Visão Geral

O sistema se conecta **em tempo real** ao seu banco de dados MySQL existente:

| Item | Valor |
|------|-------|
| **Servidor** | mysql.netcar-rc.com.br |
| **Banco** | netcarrc01 |
| **Modo** | READ-ONLY (apenas SELECT) |
| **Atualização** | A cada 5 minutos |

---

## 🔐 Configuração

### 1. Credenciais no `.env`

```bash
# CRM Externo (MySQL)
EXTERNAL_CRM_HOST=mysql.netcar-rc.com.br
EXTERNAL_CRM_PORT=3306
EXTERNAL_CRM_DATABASE=netcarrc01
EXTERNAL_CRM_USER=seu_usuario_aqui
EXTERNAL_CRM_PASSWORD=sua_senha_aqui
```

### 2. Usuário do Banco

O usuário precisa ter permissão de **SELECT** nas seguintes tabelas:

- `crm_negocio` (principal - negociações)
- `users` (vendedores)
- `veiculos` (opcional)

```sql
-- Exemplo de grant mínimo necessário
GRANT SELECT ON netcarrc01.crm_negocio TO 'usuario_bi'@'%';
GRANT SELECT ON netcarrc01.users TO 'usuario_bi'@'%';
```

---

## 📈 Dados Capturados

### Da tabela `crm_negocio`:

| Campo | Uso |
|-------|-----|
| `id_crm_negocio` | ID único |
| `titulo` | Veículo de interesse |
| `cliente` | Nome do cliente |
| `origem` | De onde veio o lead |
| `id_user` | Vendedor responsável |
| `id_state` | Estado do funil (1-8) |
| `valor` | Valor do negócio |
| `date_create` | Data de criação |
| `motivo_perda` | Motivo se perdido |

### Estados do Funil:

| Estado | Nome | Considerado |
|--------|------|-------------|
| 1 | Novo | Ativo |
| 2 | Em Atendimento | Ativo |
| 3 | Proposta Enviada | Ativo |
| 4 | Em Negociação | Ativo |
| 5 | Fechamento | Ativo |
| 6 | **GANHO** | Convertido ✅ |
| 7 | **PERDIDO** | Não convertido ❌ |
| 8 | Arquivado | Ignorado |

---

## 🔄 Como a Sincronização Funciona

### Modo Tempo Real (via API)

Os endpoints `/api/crm-sync/realtime/*` consultam diretamente o MySQL:

```
GET /api/crm-sync/realtime/resumo
GET /api/crm-sync/realtime/vendedores
GET /api/crm-sync/realtime/origens
GET /api/crm-sync/realtime/funil
GET /api/crm-sync/realtime/meta-vs-google
GET /api/crm-sync/realtime/motivos-perda
GET /api/crm-sync/realtime/leads-parados
```

### Modo Cache (via Celery)

Para performance, algumas métricas são cacheadas:

- **A cada 3 min**: KPIs são calculados e cacheados
- **A cada 5 min**: Novos leads são sincronizados

---

## 📊 Agrupamento de Origens

O sistema agrupa automaticamente as origens para análise:

| Grupo | Origens Incluídas |
|-------|-------------------|
| **META** | FACEBOOK, INSTAGRAM |
| **GOOGLE** | Google, GOOGLE |
| **SITE** | SITE |
| **PORTAIS** | WEBMOTORS, ICARROS, MEUCARRONOVO, MERCADO LIVRE, MOBIAUTO, AUTOLINE, POACARROS, SOCARRAO, Autocarro |
| **PRESENCIAL** | SHOWROOM, NA PISTA, FEIRÃO |
| **DIRETO** | WHATSAPP, TELEFONE, TELEMARKETING |
| **INDICAÇÃO** | INDICACAO, INDICAÇÃO CAMPANHA, REDE RELACIONAMENTO |
| **OUTROS** | Demais |

---

## 🛡️ Segurança

### O que é PERMITIDO:
- ✅ SELECT
- ✅ SHOW
- ✅ DESCRIBE

### O que é PROIBIDO:
- ❌ INSERT
- ❌ UPDATE
- ❌ DELETE
- ❌ DROP
- ❌ CREATE

O código valida toda query antes de executar!

---

## 🔍 Endpoints Disponíveis

### Status da Conexão
```bash
GET /api/crm-sync/status
```

Resposta:
```json
{
  "crm_externo": {
    "host": "mysql.netcar-rc.com.br",
    "database": "netcarrc01",
    "conexao": true
  },
  "sincronizacao": {
    "total_sincronizado": 1500,
    "total_crm_externo": 19385,
    "ultima_sincronizacao": "2025-12-21T10:00:00"
  }
}
```

### Preview (sem sincronizar)
```bash
GET /api/crm-sync/preview?dias=7
```

### Disparar Sincronização Manual
```bash
POST /api/crm-sync/sync?dias=30&full_sync=false
```

### Dados em Tempo Real
```bash
# Resumo do mês
GET /api/crm-sync/realtime/resumo

# Por vendedor
GET /api/crm-sync/realtime/vendedores?dias=30

# Por origem
GET /api/crm-sync/realtime/origens?dias=30

# Funil atual
GET /api/crm-sync/realtime/funil

# Comparativo META vs GOOGLE
GET /api/crm-sync/realtime/meta-vs-google?dias=30

# Motivos de perda
GET /api/crm-sync/realtime/motivos-perda?dias=30

# Leads parados
GET /api/crm-sync/realtime/leads-parados?dias=7
```

---

## 🧪 Testando a Conexão

### Via Terminal:
```bash
# Dentro do container da API
docker exec -it crm_api python -c "
from services.external_crm import get_external_crm
crm = get_external_crm()
print('Conexão OK!' if crm.test_connection() else 'FALHOU')
"
```

### Via API:
```bash
curl http://localhost:8000/api/crm-sync/status
```

---

## ❓ Troubleshooting

### Erro: "Não foi possível conectar"

1. Verifique as credenciais no `.env`
2. Confirme que seu IP está liberado no firewall do MySQL
3. Teste a conexão via terminal:
   ```bash
   mysql -h mysql.netcar-rc.com.br -u usuario -p netcarrc01
   ```

### Erro: "Timeout"

O timeout padrão é 10 segundos. Se sua conexão é lenta:
- Considere usar VPN
- Ou aumente o timeout no código

### Dados não aparecem

1. Verifique se há dados no período selecionado
2. Confirme que o campo `date_create` está preenchido
3. Verifique se o `id_state` está correto

---

## 📅 Histórico de Dados

| Período | Volume |
|---------|--------|
| Total | ~19.385 negócios |
| Ganhos | ~3.316 (17%) |
| Perdidos | ~15.796 (82%) |
| Primeiro registro | ~2020 |
| Último | Hoje |

---

*Documentação gerada automaticamente em 21/12/2025*

