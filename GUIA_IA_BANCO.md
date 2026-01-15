# 🤖 GUIA PARA IA - BANCO DE DADOS NETCARRC01

Este documento orienta como uma IA/serviço de análise deve interpretar e consultar este banco de dados.

---

## 🎯 CONTEXTO DO NEGÓCIO

Este é o banco de dados de uma **revenda de veículos seminovos** com os seguintes módulos:

1. **CRM de Vendas** - Gestão de leads e negociações
2. **Fluxo de Veículos** - Controle de avaliação, preparação e entrega
3. **Pós-Venda** - Automações de relacionamento via WhatsApp

---

## 📊 FONTES DE VERDADE (Tabelas Principais)

### ⭐ crm_negocio (PRINCIPAL)
**O que é:** Cada registro representa um **lead/negociação** com um potencial cliente.

**Campos essenciais para análise:**
| Campo | Uso |
|-------|-----|
| `id_crm_negocio` | Identificador único |
| `origem` | De onde veio o lead (FACEBOOK, GOOGLE, SITE, etc) |
| `id_user` | Vendedor responsável (FK → users) |
| `id_state` | Estado no funil (1-5 = ativo, 6 = ganho, 7 = perdido) |
| `valor` | Valor do negócio |
| `date_create` | Data de entrada do lead |
| `motivo_perda` | Se perdido, qual o motivo |

**Estados do Funil:**
```
1 = Novo
2 = Em Atendimento
3 = Proposta Enviada
4 = Em Negociação
5 = Fechamento
6 = GANHO ✅
7 = PERDIDO ❌
8 = Arquivado
```

### 👥 users
**O que é:** Cadastro de usuários do sistema (vendedores, gerentes, admins).

**Perfis:**
- 1 = Administrador
- 2 = Gerente
- 3 = Vendedor
- 4 = Outro

### 🚗 veiculos
**O que é:** Cadastro de veículos em estoque ou já vendidos.

**Campos importantes:**
- `seqveiculo` - ID único
- `modelo`, `placa`, `anofab`, `anomod`
- `vlrcompra`, `precovenda` - Valores
- `flgvendido` - Se foi vendido ('S'/'N')

---

## 🔗 COMO AS TABELAS SE RELACIONAM

```
crm_negocio.id_user → users.id_users
crm_negocio_comentario.id_crm_negocio → crm_negocio.id_crm_negocio

fvalue_*.id_car → veiculos.seqveiculo
fvalue_*.id_users → users.id_users
fvalue_*.id_fvalue_stage → fvalue_stage.id_fvalue_stage

posv_*.id_veiculo → veiculos.seqveiculo
```

---

## 🚫 REGRAS ABSOLUTAS DE SEGURANÇA

### ❌ NUNCA EXECUTAR (Proibido)
```sql
CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, TRUNCATE, CREATE VIEW
```

### ✅ PERMITIDO (Apenas)
```sql
SELECT, SHOW, DESCRIBE, EXPLAIN
```

### 🔐 DADOS SENSÍVEIS (Nunca expor)
- `users.password` - Senhas
- `crm_negocio.celular` - Telefones de clientes
- `crm_negocio.email` - E-mails de clientes
- `*.chatpro_token` - Tokens de API
- `*.chatpro_endpoint` - URLs internas

---

## 💡 COMO A IA DEVE "PENSAR" O BANCO

### Para análise de VENDAS:
1. Use `crm_negocio` como base principal
2. JOIN com `users` para nome do vendedor
3. Filtre por `date_create` para período
4. Use `id_state = 6` para vendas fechadas
5. Use `id_state = 7` para perdas

### Para análise de CONVERSÃO:
```sql
taxa_conversao = (ganhos / (ganhos + perdidos)) * 100
```
Onde:
- `ganhos` = COUNT de `id_state = 6`
- `perdidos` = COUNT de `id_state = 7`

### Para análise de ORIGENS (Meta/Google):
Agrupe assim:
- **META** = FACEBOOK + INSTAGRAM
- **GOOGLE** = Google (atenção ao case-sensitive)
- **PORTAIS** = WEBMOTORS, ICARROS, MEUCARRONOVO, etc
- **PRESENCIAL** = SHOWROOM, FEIRÃO, NA PISTA
- **DIRETO** = WHATSAPP, TELEFONE

### Para análise de VEÍCULOS:
1. Use `veiculos` como base
2. JOIN com `fvalue_car_stage` para status atual
3. JOIN com `fvalue_intervention` para custos

---

## 📈 PERGUNTAS COMUNS E COMO RESPONDER

### "Quantas vendas tivemos este mês?"
```sql
SELECT COUNT(*) 
FROM crm_negocio 
WHERE id_state = 6 
  AND DATE_FORMAT(date_create, '%Y-%m') = DATE_FORMAT(NOW(), '%Y-%m');
```

### "Qual vendedor vendeu mais?"
```sql
SELECT u.name, COUNT(*) as vendas
FROM crm_negocio n
JOIN users u ON n.id_user = u.id_users
WHERE n.id_state = 6
GROUP BY n.id_user, u.name
ORDER BY vendas DESC
LIMIT 5;
```

### "Qual origem converte mais?"
```sql
SELECT origem,
       COUNT(*) as total,
       SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) as ganhos,
       ROUND(SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as taxa
FROM crm_negocio
WHERE id_state IN (6, 7)
GROUP BY origem
ORDER BY taxa DESC;
```

### "Por que estamos perdendo vendas?"
```sql
SELECT motivo_perda, COUNT(*) as qtd
FROM crm_negocio
WHERE id_state = 7
  AND motivo_perda IS NOT NULL AND motivo_perda != ''
GROUP BY motivo_perda
ORDER BY qtd DESC
LIMIT 10;
```

---

## ⚡ BOAS PRÁTICAS PARA CONSULTAS

### 1. Sempre use filtros de data
```sql
-- BOM ✅
WHERE date_create >= '2025-01-01'

-- RUIM ❌ (traz todo o histórico)
WHERE 1=1
```

### 2. Use LIMIT para exploração
```sql
-- BOM ✅
SELECT * FROM crm_negocio LIMIT 100

-- RUIM ❌
SELECT * FROM crm_negocio
```

### 3. Evite SELECT *
```sql
-- BOM ✅
SELECT id_crm_negocio, titulo, origem, valor FROM crm_negocio

-- RUIM ❌
SELECT * FROM crm_negocio
```

### 4. Use CTEs para queries complexas
```sql
-- BOM ✅
WITH vendas_mes AS (
    SELECT id_user, COUNT(*) as vendas
    FROM crm_negocio WHERE id_state = 6
    GROUP BY id_user
)
SELECT u.name, v.vendas
FROM vendas_mes v
JOIN users u ON v.id_user = u.id_users;
```

### 5. Prefira JOINs a subqueries
```sql
-- BOM ✅
SELECT n.*, u.name as vendedor
FROM crm_negocio n
JOIN users u ON n.id_user = u.id_users

-- MENOS EFICIENTE
SELECT *, (SELECT name FROM users WHERE id_users = crm_negocio.id_user) as vendedor
FROM crm_negocio
```

---

## 📋 ÍNDICES EXISTENTES (para otimização)

O banco possui índices em:
- Chaves primárias (todas as tabelas)
- `crm_negocio.titulo` (MUL)
- `crm_negocio.date_create` (MUL)
- Foreign Keys declaradas

**Índices recomendados (não aplicados):**
- `crm_negocio(date_create, id_state)`
- `crm_negocio(origem)`
- `crm_negocio(id_user)`

---

## 🗂️ GLOSSÁRIO DE TERMOS

| Termo no Banco | Significado |
|----------------|-------------|
| `negocio` | Lead/oportunidade de venda |
| `id_state` | Etapa do funil de vendas |
| `origem` | Canal de aquisição do lead |
| `fvalue` | Sistema de fluxo de veículos (Fabrica Values) |
| `posv` | Pós-venda |
| `chatpro` | Integração com WhatsApp |
| `intervention` | Serviço/reparo no veículo |
| `exchange` | Avaliação de veículo de troca |

---

## 📊 MÉTRICAS PADRÃO

### Taxa de Conversão
```
(Negócios Ganhos / Total Finalizados) × 100
```

### Ticket Médio
```
Soma(valor dos ganhos) / Quantidade de ganhos
```

### Ciclo de Venda
```
AVG(date_update - date_create) WHERE id_state = 6
```

### Leads Parados
```
Leads com id_state entre 1-5 E date_update > 7 dias atrás
```

---

## ⚠️ LIMITAÇÕES CONHECIDAS

1. **Dados de data inválidos:** Alguns registros têm `date_create = '0000-00-00'`
2. **Campos nulos:** `canal` é NULL em 92% dos registros
3. **Sem FK formal no CRM:** `id_user` e `id_state` não têm FK declarada
4. **Duplicados:** Campo `duplicado` existe mas precisa validar uso

---

## 🔄 FLUXO DE DADOS

```
1. Lead entra (origem: site/meta/google/showroom)
         ↓
2. Atribuído a vendedor (id_user)
         ↓
3. Progride no funil (id_state: 1→2→3→4→5)
         ↓
4. Resultado final:
   - id_state = 6 (GANHO) → Venda concluída
   - id_state = 7 (PERDIDO) → motivo_perda preenchido
```

---

*Este documento deve ser usado como referência para qualquer IA ou serviço que consulte este banco de dados.*

