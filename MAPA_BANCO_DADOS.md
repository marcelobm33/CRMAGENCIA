# 🗄️ MAPA DO BANCO DE DADOS - NETCARRC01

**Gerado em:** 21/12/2025  
**Banco:** netcarrc01 @ mysql.netcar-rc.com.br  
**Total de Tabelas:** 45  
**Modo de Acesso:** READ-ONLY (apenas SELECT)

---

## 📊 RESUMO EXECUTIVO

Este banco de dados é um **sistema integrado de gestão para revenda de veículos** com 3 módulos principais:

| Módulo | Prefixo | Função |
|--------|---------|--------|
| **CRM** | `crm_` | Gestão de leads e negociações |
| **FValue** | `fvalue_` | Gestão do fluxo de veículos (avaliação → venda) |
| **Pós-Venda** | `posv_` | Automações de relacionamento (WhatsApp) |

---

## 🏗️ CLASSIFICAÇÃO DAS TABELAS

### 📋 TABELAS DE CADASTRO (Entidades Principais)

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `users` | 18 | Usuários do sistema (vendedores, gerentes) |
| `veiculos` | 3.655 | Catálogo de veículos em estoque/vendidos |
| `posv_fornecedor` | 33 | Fornecedores de serviços |
| `posv_mensagem` | 8 | Templates de mensagens |
| `fvalue_stage` | 6 | Etapas do fluxo de veículos |
| `fvalue_type_intervention` | 3 | Tipos de intervenção em veículos |
| `fvalue_checkitem` | 29 | Itens de checklist |
| `fvalue_margem` | 15 | Faixas de margem de lucro |
| `parametros_gpt` | 2 | Configurações do ChatGPT |

### 💼 TABELAS TRANSACIONAIS (Operações do Negócio)

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `crm_negocio` | **19.385** | ⭐ **PRINCIPAL** - Negociações/Leads |
| `crm_negocio_comentario` | 2.592 | Histórico de comentários por negócio |
| `fvalue_intervention` | 19.763 | Intervenções em veículos |
| `fvalue_exchange` | 5.221 | Avaliações de veículos de troca |
| `fvalue_warranty` | 591 | Garantias de veículos |
| `fvalue_tasks` | 273 | Tarefas internas |
| `forn_pagamento` | 4.456 | Pagamentos a fornecedores |

### 📜 TABELAS DE HISTÓRICO/LOG

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `fvalue_car_steps` | 20.258 | Histórico de mudanças de etapa por veículo |
| `fvalue_car_stage` | 4.148 | Status atual por etapa |
| `fvalue_car_checkitem` | 66.919 | Checklist executado por veículo |
| `fvalue_comments` | 1.264 | Comentários em veículos |
| `fvalue_restrictions` | 2.728 | Restrições/pendências |
| `chatpro_log` | 5.284 | Log de mensagens WhatsApp |

### 📱 TABELAS DE AUTOMAÇÃO (Pós-Venda)

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `posv_contrato` | 5.232 | Envio de contratos |
| `posv_campanha` | 1.240 | Campanhas de marketing |
| `posv_campanha_blackfriday` | 4.312 | Campanha Black Friday |
| `posv_alertafabrica` | 1.149 | Alertas de fábrica |
| `posv_agradecimento` | 6 | Mensagens de agradecimento |
| `posv_aniversariante` | 13 | Aniversário do cliente |
| `posv_googlereview` | 2 | Solicitação de avaliação |
| `posv_blacklist` | 1.530 | Clientes bloqueados para envio |

### 📊 TABELAS DE APOIO

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `fvalue_fipe` | 224 | Tabela FIPE de veículos |
| `fvalue_placa_fipe` | 802 | Relação placa → código FIPE |
| `fvalue_soma_fipe` | 1.348 | Soma diária de valores FIPE |
| `anuncio_chatgpt` | 3 | Anúncios gerados por IA |
| `posv_config` | 3 | Configurações do sistema |

---

## 🔑 TABELA PRINCIPAL: crm_negocio

Esta é a **fonte de verdade** para todas as análises de vendas e leads.

### Estrutura Completa

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id_crm_negocio` | int(11) PK | ID único do negócio |
| `id_supabase` | varchar(36) | ID externo (integração Supabase) |
| `titulo` | varchar(100) | Descrição do veículo de interesse |
| `comentario` | text | Observações gerais |
| `origem` | varchar(100) | **De onde veio o lead** |
| `canal` | varchar(100) | Canal de primeiro contato |
| `duplicado` | tinyint(1) | Flag de duplicidade |
| `cliente` | varchar(100) | Nome do cliente |
| `celular` | varchar(100) | Telefone do cliente |
| `email` | varchar(100) | E-mail do cliente |
| `valor` | double | Valor do negócio |
| `id_user` | int(11) | **Vendedor responsável** |
| `id_state` | int(11) | **Estado no funil** |
| `date_create` | datetime | Data de criação |
| `date_update` | datetime | Última atualização |
| `date_return` | datetime | Data de retorno programado |
| `motivo_perda` | varchar(200) | Motivo se perdido |
| `id_group` | int(11) | Grupo (filial?) |
| `dias_ultima_negociacao` | int(11) | Dias desde último contato |

### 🎯 Origens dos Leads (TOP 10)

| Origem | Qtd | % |
|--------|-----|---|
| SITE | 5.832 | 30,4% |
| SHOWROOM | 2.571 | 13,4% |
| WHATSAPP | 1.658 | 8,6% |
| Autocarro | 1.543 | 8,0% |
| OFERTA VENDEDOR | 1.383 | 7,2% |
| WEBMOTORS | 1.001 | 5,2% |
| FACEBOOK | 650 | 3,4% |
| ICARROS | 556 | 2,9% |
| INDICACAO | 548 | 2,9% |
| TELEMARKETING | 480 | 2,5% |

### 📊 Estados do Funil

| id_state | Descrição Provável | Qtd |
|----------|-------------------|-----|
| 1 | Novo/Entrada | 31 |
| 2 | Em Atendimento | 9 |
| 3 | Proposta Enviada | 6 |
| 4 | Em Negociação | 9 |
| 5 | Fechamento | 8 |
| 6 | **GANHO** | 3.316 |
| 7 | **PERDIDO** | 15.796 |
| 8 | Arquivado | 6 |

> ⚠️ **NOTA:** Os estados 1-5 têm poucos registros pois a maioria já foi movida para GANHO (6) ou PERDIDO (7).

### ❌ Motivos de Perda (TOP 10)

| Motivo | Qtd |
|--------|-----|
| Vai Esperar | 3.750 |
| Desistência Sem Motivo | 3.526 |
| Sem Interesse | 2.455 |
| Cliente Não Responde | 1.439 |
| Crédito Negado | 935 |
| Veículo Já Foi Vendido | 875 |
| Veículo da troca não interessa | 662 |
| Concorrência | 660 |
| Avaliação da Troca | 581 |
| Produto não disponível | 323 |

---

## 👥 TABELA: users (Vendedores)

| id_users | Nome | Negócios | Status | Perfil |
|----------|------|----------|--------|--------|
| 8 | Tiago | 6.369 | Ativo | 3 (Vendedor) |
| 15 | Bruno | 5.441 | Ativo | 3 (Vendedor) |
| 7 | Carlos | 3.236 | Ativo | 3 (Vendedor) |
| 3 | Marcelo | 1.884 | Ativo | 1 (Admin?) |
| 18 | Herick | 1.107 | Ativo | 2 (Gerente?) |
| 21 | Gilnei | 917 | Inativo | 3 (Vendedor) |

**Perfis identificados:**
- 1 = Administrador
- 2 = Gerente
- 3 = Vendedor
- 4 = Outro

---

## 🚗 FLUXO DE VEÍCULOS (fvalue_stage)

| Etapa | Nome | Descrição |
|-------|------|-----------|
| 1 | Aguardando Avaliação | Veículo entrou, aguarda checklist |
| 2 | Checklist Avaliação | Em processo de avaliação |
| 3 | Checklist Showroom | Preparação para showroom |
| 4 | Checklist Entrega | Vendido, preparando entrega |
| 5 | Vendido | Processo concluído |
| 6 | Excluído | Removido do sistema |

---

## 🔗 DIAGRAMA DE RELACIONAMENTOS

```
                              ┌─────────────────┐
                              │     users       │
                              │   (id_users)    │
                              └────────┬────────┘
                                       │
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
              ▼                        ▼                        ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │   crm_negocio   │     │ fvalue_exchange │     │ fvalue_comments │
    │ (id_crm_negocio)│     │   (avaliações)  │     │  (comentários)  │
    └────────┬────────┘     └─────────────────┘     └─────────────────┘
             │
             ▼
    ┌─────────────────┐
    │crm_negocio_     │
    │   comentario    │
    └─────────────────┘


    ┌─────────────────┐
    │    veiculos     │
    │  (seqveiculo)   │
    └────────┬────────┘
             │
    ┌────────┼────────┬────────────────┬─────────────────┐
    │        │        │                │                 │
    ▼        ▼        ▼                ▼                 ▼
┌────────┐┌────────┐┌────────┐   ┌──────────┐    ┌────────────┐
│fvalue_ ││fvalue_ ││fvalue_ │   │ fvalue_  │    │   posv_    │
│car_    ││interv- ││car_    │   │ warranty │    │  contrato  │
│stage   ││ention  ││steps   │   │          │    │            │
└────────┘└────────┘└────────┘   └──────────┘    └────────────┘


    ┌─────────────────┐         ┌─────────────────┐
    │   fvalue_stage  │◄────────│ fvalue_checkitem│
    │    (etapas)     │         │(itens checklist)│
    └─────────────────┘         └─────────────────┘
```

---

## ⚠️ RELAÇÕES A VALIDAR

Estas são relações **inferidas** (não há FK declarada):

| Origem | Destino Provável | Query de Validação |
|--------|-----------------|-------------------|
| `crm_negocio.id_user` | `users.id_users` | `SELECT DISTINCT n.id_user, u.name FROM crm_negocio n LEFT JOIN users u ON n.id_user = u.id_users` |
| `crm_negocio.id_state` | (tabela interna?) | Verificar se existe tabela de estados |
| `posv_contrato.id_veiculo` | `veiculos.seqveiculo` | `SELECT c.id_veiculo, v.modelo FROM posv_contrato c LEFT JOIN veiculos v ON c.id_veiculo = v.seqveiculo LIMIT 5` |
| `fvalue_*.id_car` | `veiculos.seqveiculo` | `SELECT DISTINCT id_car FROM fvalue_car_stage WHERE id_car NOT IN (SELECT seqveiculo FROM veiculos)` |
| `chatpro_log.id_user` | `users.id_users` | `SELECT DISTINCT l.id_user, u.name FROM chatpro_log l LEFT JOIN users u ON l.id_user = u.id_users` |

---

## 📈 KPIs DISPONÍVEIS PARA BI

### Vendas & Conversão
- Taxa de conversão por origem
- Taxa de conversão por vendedor
- Tempo médio de fechamento
- Ticket médio por origem/vendedor

### Funil de Vendas
- Leads por etapa do funil
- Motivos de perda mais frequentes
- Leads "parados" por mais de X dias

### Produtividade
- Negócios por vendedor
- Volume de WhatsApp por vendedor
- Checklist completados por dia

### Pós-Venda
- Campanhas enviadas vs respondidas
- Taxa de opt-out (blacklist)
- Garantias acionadas

---

## 🔒 REGRAS DE SEGURANÇA (READ-ONLY)

### ❌ NUNCA EXECUTAR
```sql
-- PROIBIDO
CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, TRUNCATE
```

### ✅ PERMITIDO
```sql
-- LIBERADO
SELECT, SHOW, DESCRIBE, EXPLAIN
```

### 🔐 CAMPOS SENSÍVEIS (Evitar expor)
- `users.password`
- `crm_negocio.celular` (dados pessoais)
- `crm_negocio.email` (dados pessoais)
- `*.chatpro_token` (credenciais de API)
- `*.chatpro_endpoint` (URLs internas)

---

## 📅 PERÍODO DOS DADOS

| Métrica | Valor |
|---------|-------|
| Primeiro registro | ~2020 (data inválida em alguns) |
| Último registro | 20/12/2025 |
| Total de negócios | 19.182 |
| Negócios ganhos | 3.316 (17,3%) |
| Negócios perdidos | 15.796 (82,3%) |

---

*Documento gerado automaticamente - Apenas para consulta*

