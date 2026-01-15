-- ================================================================================
-- CAMADA DE CONSULTAS READ-ONLY - CRM NETCARRC01
-- ================================================================================
-- Todas as queries são APENAS SELECT - nenhuma escrita
-- Parametrizáveis por: data, vendedor, origem
-- ================================================================================


-- ================================================================================
-- 1. LEADS COM ORIGEM, CAMPANHA, VENDEDOR E STATUS
-- ================================================================================

-- 1.1 Listagem completa de leads com informações do vendedor
SELECT 
    n.id_crm_negocio AS id,
    n.titulo AS veiculo,
    n.cliente,
    n.celular,
    n.origem,
    n.canal,
    n.valor,
    u.name AS vendedor,
    n.id_state AS estado,
    CASE n.id_state
        WHEN 1 THEN 'Novo'
        WHEN 2 THEN 'Em Atendimento'
        WHEN 3 THEN 'Proposta Enviada'
        WHEN 4 THEN 'Em Negociação'
        WHEN 5 THEN 'Fechamento'
        WHEN 6 THEN 'GANHO'
        WHEN 7 THEN 'PERDIDO'
        WHEN 8 THEN 'Arquivado'
        ELSE 'Desconhecido'
    END AS estado_nome,
    n.date_create AS data_criacao,
    n.date_update AS ultima_atualizacao,
    n.motivo_perda,
    n.dias_ultima_negociacao
FROM crm_negocio n
LEFT JOIN users u ON n.id_user = u.id_users
ORDER BY n.date_create DESC
LIMIT 100;


-- 1.2 Leads filtrados por período
-- PARAMETROS: @data_inicio, @data_fim
SELECT 
    n.id_crm_negocio AS id,
    n.titulo AS veiculo,
    n.cliente,
    n.origem,
    u.name AS vendedor,
    n.id_state AS estado,
    n.valor,
    n.date_create AS data_criacao
FROM crm_negocio n
LEFT JOIN users u ON n.id_user = u.id_users
WHERE n.date_create BETWEEN '2025-01-01' AND '2025-12-31'  -- Substitua pelas datas desejadas
ORDER BY n.date_create DESC;


-- 1.3 Leads por vendedor específico
-- PARAMETRO: @id_vendedor
SELECT 
    n.id_crm_negocio AS id,
    n.titulo AS veiculo,
    n.cliente,
    n.origem,
    n.id_state AS estado,
    n.valor,
    n.date_create AS data_criacao
FROM crm_negocio n
WHERE n.id_user = 8  -- Substitua pelo ID do vendedor
ORDER BY n.date_create DESC;


-- 1.4 Leads por origem específica
-- PARAMETRO: @origem
SELECT 
    n.id_crm_negocio AS id,
    n.titulo AS veiculo,
    n.cliente,
    u.name AS vendedor,
    n.id_state AS estado,
    n.valor,
    n.date_create AS data_criacao
FROM crm_negocio n
LEFT JOIN users u ON n.id_user = u.id_users
WHERE n.origem = 'FACEBOOK'  -- Substitua pela origem desejada
ORDER BY n.date_create DESC;


-- ================================================================================
-- 2. NEGÓCIOS GANHOS x PERDIDOS POR PERÍODO
-- ================================================================================

-- 2.1 Resumo mensal de ganhos x perdidos
WITH negocios_mensais AS (
    SELECT 
        DATE_FORMAT(date_create, '%Y-%m') AS mes,
        id_state,
        COUNT(*) AS quantidade,
        SUM(valor) AS valor_total
    FROM crm_negocio
    WHERE date_create >= '2024-01-01'
    GROUP BY DATE_FORMAT(date_create, '%Y-%m'), id_state
)
SELECT 
    mes,
    SUM(CASE WHEN id_state = 6 THEN quantidade ELSE 0 END) AS ganhos,
    SUM(CASE WHEN id_state = 7 THEN quantidade ELSE 0 END) AS perdidos,
    SUM(CASE WHEN id_state = 6 THEN valor_total ELSE 0 END) AS valor_ganhos,
    SUM(CASE WHEN id_state = 7 THEN valor_total ELSE 0 END) AS valor_perdidos,
    ROUND(
        SUM(CASE WHEN id_state = 6 THEN quantidade ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN id_state IN (6,7) THEN quantidade ELSE 0 END), 0)
    , 2) AS taxa_conversao
FROM negocios_mensais
GROUP BY mes
ORDER BY mes DESC;


-- 2.2 Ganhos x Perdidos por vendedor
WITH vendedor_stats AS (
    SELECT 
        n.id_user,
        u.name AS vendedor,
        n.id_state,
        COUNT(*) AS quantidade,
        SUM(n.valor) AS valor_total
    FROM crm_negocio n
    LEFT JOIN users u ON n.id_user = u.id_users
    WHERE n.date_create >= '2025-01-01'
    GROUP BY n.id_user, u.name, n.id_state
)
SELECT 
    vendedor,
    SUM(CASE WHEN id_state = 6 THEN quantidade ELSE 0 END) AS ganhos,
    SUM(CASE WHEN id_state = 7 THEN quantidade ELSE 0 END) AS perdidos,
    SUM(CASE WHEN id_state = 6 THEN valor_total ELSE 0 END) AS valor_ganhos,
    ROUND(
        SUM(CASE WHEN id_state = 6 THEN quantidade ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN id_state IN (6,7) THEN quantidade ELSE 0 END), 0)
    , 2) AS taxa_conversao
FROM vendedor_stats
GROUP BY id_user, vendedor
ORDER BY ganhos DESC;


-- 2.3 Ganhos x Perdidos por origem (Meta / Google / etc)
WITH origem_stats AS (
    SELECT 
        CASE 
            WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
            WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
            WHEN origem IN ('SITE') THEN 'SITE PRÓPRIO'
            WHEN origem IN ('WEBMOTORS', 'ICARROS', 'MEUCARRONOVO', 'MERCADO LIVRE', 'MOBIAUTO', 'AUTOLINE', 'POACARROS', 'SOCARRAO', 'Autocarro') THEN 'PORTAIS'
            WHEN origem IN ('SHOWROOM', 'NA PISTA', 'FEIRÃO') THEN 'PRESENCIAL'
            WHEN origem IN ('WHATSAPP', 'TELEFONE', 'TELEMARKETING') THEN 'DIRETO'
            WHEN origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO') THEN 'INDICAÇÃO'
            ELSE 'OUTROS'
        END AS grupo_origem,
        id_state,
        COUNT(*) AS quantidade,
        SUM(valor) AS valor_total
    FROM crm_negocio
    WHERE date_create >= '2025-01-01'
    GROUP BY grupo_origem, id_state
)
SELECT 
    grupo_origem,
    SUM(CASE WHEN id_state = 6 THEN quantidade ELSE 0 END) AS ganhos,
    SUM(CASE WHEN id_state = 7 THEN quantidade ELSE 0 END) AS perdidos,
    SUM(CASE WHEN id_state = 6 THEN valor_total ELSE 0 END) AS valor_ganhos,
    ROUND(
        SUM(CASE WHEN id_state = 6 THEN quantidade ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN id_state IN (6,7) THEN quantidade ELSE 0 END), 0)
    , 2) AS taxa_conversao
FROM origem_stats
GROUP BY grupo_origem
ORDER BY ganhos DESC;


-- ================================================================================
-- 3. FUNIL POR ETAPA
-- ================================================================================

-- 3.1 Funil atual (leads ativos por estado)
SELECT 
    id_state,
    CASE id_state
        WHEN 1 THEN '1. Novo'
        WHEN 2 THEN '2. Em Atendimento'
        WHEN 3 THEN '3. Proposta Enviada'
        WHEN 4 THEN '4. Em Negociação'
        WHEN 5 THEN '5. Fechamento'
        WHEN 6 THEN '6. GANHO'
        WHEN 7 THEN '7. PERDIDO'
        WHEN 8 THEN '8. Arquivado'
        ELSE 'Desconhecido'
    END AS etapa,
    COUNT(*) AS quantidade,
    SUM(valor) AS valor_total,
    ROUND(AVG(valor), 2) AS ticket_medio
FROM crm_negocio
GROUP BY id_state
ORDER BY id_state;


-- 3.2 Funil por período (apenas leads ativos - estados 1 a 5)
SELECT 
    id_state,
    CASE id_state
        WHEN 1 THEN '1. Novo'
        WHEN 2 THEN '2. Em Atendimento'
        WHEN 3 THEN '3. Proposta Enviada'
        WHEN 4 THEN '4. Em Negociação'
        WHEN 5 THEN '5. Fechamento'
    END AS etapa,
    COUNT(*) AS quantidade,
    SUM(valor) AS valor_potencial
FROM crm_negocio
WHERE id_state BETWEEN 1 AND 5
  AND date_create >= '2025-01-01'
GROUP BY id_state
ORDER BY id_state;


-- 3.3 Leads "parados" há mais de X dias
SELECT 
    n.id_crm_negocio AS id,
    n.titulo AS veiculo,
    n.cliente,
    n.origem,
    u.name AS vendedor,
    n.id_state AS estado,
    n.valor,
    n.date_create AS data_criacao,
    n.date_update AS ultima_atualizacao,
    DATEDIFF(NOW(), n.date_update) AS dias_parado
FROM crm_negocio n
LEFT JOIN users u ON n.id_user = u.id_users
WHERE n.id_state BETWEEN 1 AND 5  -- Apenas leads ativos
  AND DATEDIFF(NOW(), n.date_update) > 7  -- Mais de 7 dias parado
ORDER BY dias_parado DESC;


-- ================================================================================
-- 4. PERFORMANCE POR VENDEDOR
-- ================================================================================

-- 4.1 Ranking de vendedores (período atual)
WITH vendedor_performance AS (
    SELECT 
        n.id_user,
        u.name AS vendedor,
        COUNT(*) AS total_leads,
        SUM(CASE WHEN n.id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
        SUM(CASE WHEN n.id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
        SUM(CASE WHEN n.id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS em_andamento,
        SUM(CASE WHEN n.id_state = 6 THEN n.valor ELSE 0 END) AS valor_vendido,
        AVG(CASE WHEN n.id_state = 6 THEN n.valor ELSE NULL END) AS ticket_medio
    FROM crm_negocio n
    LEFT JOIN users u ON n.id_user = u.id_users
    WHERE n.date_create >= '2025-01-01'
    GROUP BY n.id_user, u.name
)
SELECT 
    vendedor,
    total_leads,
    ganhos,
    perdidos,
    em_andamento,
    ROUND(ganhos * 100.0 / NULLIF(ganhos + perdidos, 0), 2) AS taxa_conversao,
    ROUND(valor_vendido, 2) AS valor_vendido,
    ROUND(ticket_medio, 2) AS ticket_medio
FROM vendedor_performance
ORDER BY valor_vendido DESC;


-- 4.2 Performance por vendedor e origem
SELECT 
    u.name AS vendedor,
    n.origem,
    COUNT(*) AS total_leads,
    SUM(CASE WHEN n.id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
    ROUND(
        SUM(CASE WHEN n.id_state = 6 THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(COUNT(*), 0)
    , 2) AS taxa_conversao
FROM crm_negocio n
LEFT JOIN users u ON n.id_user = u.id_users
WHERE n.date_create >= '2025-01-01'
GROUP BY u.name, n.origem
HAVING COUNT(*) >= 10  -- Mínimo de 10 leads
ORDER BY u.name, ganhos DESC;


-- 4.3 Evolução mensal por vendedor
SELECT 
    DATE_FORMAT(n.date_create, '%Y-%m') AS mes,
    u.name AS vendedor,
    COUNT(*) AS total_leads,
    SUM(CASE WHEN n.id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
    SUM(CASE WHEN n.id_state = 6 THEN n.valor ELSE 0 END) AS valor_vendido
FROM crm_negocio n
LEFT JOIN users u ON n.id_user = u.id_users
WHERE n.date_create >= '2024-01-01'
GROUP BY DATE_FORMAT(n.date_create, '%Y-%m'), u.name
ORDER BY mes DESC, valor_vendido DESC;


-- ================================================================================
-- 5. COMPARATIVO POR ORIGEM/CAMPANHA (META / GOOGLE)
-- ================================================================================

-- 5.1 META (Facebook + Instagram) vs GOOGLE
WITH origem_comparativo AS (
    SELECT 
        CASE 
            WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
            WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
            ELSE NULL
        END AS plataforma,
        id_state,
        valor,
        date_create
    FROM crm_negocio
    WHERE origem IN ('FACEBOOK', 'INSTAGRAM', 'Google', 'GOOGLE')
)
SELECT 
    plataforma,
    COUNT(*) AS total_leads,
    SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
    SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
    ROUND(
        SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(COUNT(*), 0)
    , 2) AS taxa_conversao,
    SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido,
    ROUND(AVG(CASE WHEN id_state = 6 THEN valor ELSE NULL END), 2) AS ticket_medio
FROM origem_comparativo
WHERE plataforma IS NOT NULL
GROUP BY plataforma;


-- 5.2 Comparativo mensal META vs GOOGLE
WITH origem_mensal AS (
    SELECT 
        DATE_FORMAT(date_create, '%Y-%m') AS mes,
        CASE 
            WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
            WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
        END AS plataforma,
        id_state,
        valor
    FROM crm_negocio
    WHERE origem IN ('FACEBOOK', 'INSTAGRAM', 'Google', 'GOOGLE')
      AND date_create >= '2024-01-01'
)
SELECT 
    mes,
    plataforma,
    COUNT(*) AS leads,
    SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
    ROUND(
        SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(COUNT(*), 0)
    , 2) AS taxa_conversao
FROM origem_mensal
WHERE plataforma IS NOT NULL
GROUP BY mes, plataforma
ORDER BY mes DESC, plataforma;


-- 5.3 Todas as origens comparadas
SELECT 
    origem,
    COUNT(*) AS total_leads,
    SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
    SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
    ROUND(
        SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN id_state IN (6,7) THEN 1 ELSE 0 END), 0)
    , 2) AS taxa_conversao,
    SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido,
    ROUND(AVG(CASE WHEN id_state = 6 THEN valor ELSE NULL END), 2) AS ticket_medio
FROM crm_negocio
WHERE date_create >= '2025-01-01'
GROUP BY origem
HAVING COUNT(*) >= 10
ORDER BY taxa_conversao DESC;


-- ================================================================================
-- 6. MOTIVOS DE PERDA (ANÁLISE)
-- ================================================================================

-- 6.1 Top motivos de perda
SELECT 
    motivo_perda,
    COUNT(*) AS quantidade,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM crm_negocio WHERE id_state = 7), 2) AS percentual
FROM crm_negocio
WHERE id_state = 7
  AND motivo_perda IS NOT NULL
  AND motivo_perda != ''
GROUP BY motivo_perda
ORDER BY quantidade DESC
LIMIT 20;


-- 6.2 Motivos de perda por vendedor
SELECT 
    u.name AS vendedor,
    n.motivo_perda,
    COUNT(*) AS quantidade
FROM crm_negocio n
LEFT JOIN users u ON n.id_user = u.id_users
WHERE n.id_state = 7
  AND n.motivo_perda IS NOT NULL
  AND n.motivo_perda != ''
  AND n.date_create >= '2025-01-01'
GROUP BY u.name, n.motivo_perda
ORDER BY u.name, quantidade DESC;


-- 6.3 Motivos de perda por origem
SELECT 
    origem,
    motivo_perda,
    COUNT(*) AS quantidade
FROM crm_negocio
WHERE id_state = 7
  AND motivo_perda IS NOT NULL
  AND motivo_perda != ''
  AND date_create >= '2025-01-01'
GROUP BY origem, motivo_perda
ORDER BY origem, quantidade DESC;


-- ================================================================================
-- 7. ANÁLISE DE VEÍCULOS
-- ================================================================================

-- 7.1 Veículos em estoque por etapa
SELECT 
    s.name AS etapa,
    COUNT(*) AS quantidade
FROM fvalue_car_stage cs
JOIN fvalue_stage s ON cs.id_fvalue_stage = s.id_fvalue_stage
WHERE cs.status = 'S'
GROUP BY s.name
ORDER BY s.id_fvalue_stage;


-- 7.2 Intervenções por tipo
SELECT 
    t.name AS tipo_intervencao,
    COUNT(*) AS quantidade,
    SUM(i.price) AS custo_total,
    AVG(i.price) AS custo_medio
FROM fvalue_intervention i
JOIN fvalue_type_intervention t ON i.id_fvalue_type_intervention = t.id_fvalue_type_intervention
GROUP BY t.name
ORDER BY quantidade DESC;


-- 7.3 Top 10 veículos com mais intervenções
SELECT 
    v.modelo,
    v.placa,
    v.anofab,
    COUNT(i.id_fvalue_intervention) AS total_intervencoes,
    SUM(i.price) AS custo_total
FROM veiculos v
JOIN fvalue_intervention i ON i.id_car = v.seqveiculo
GROUP BY v.seqveiculo, v.modelo, v.placa, v.anofab
ORDER BY total_intervencoes DESC
LIMIT 10;


-- ================================================================================
-- 8. DASHBOARD EXECUTIVO (RESUMO)
-- ================================================================================

-- 8.1 KPIs do mês atual
SELECT 
    'MES_ATUAL' AS periodo,
    COUNT(*) AS total_leads,
    SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
    SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
    SUM(CASE WHEN id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS em_andamento,
    ROUND(
        SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN id_state IN (6,7) THEN 1 ELSE 0 END), 0)
    , 2) AS taxa_conversao,
    SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido,
    ROUND(AVG(CASE WHEN id_state = 6 THEN valor ELSE NULL END), 2) AS ticket_medio
FROM crm_negocio
WHERE DATE_FORMAT(date_create, '%Y-%m') = DATE_FORMAT(NOW(), '%Y-%m');


-- ================================================================================
-- SUGESTÕES DE ÍNDICES (NÃO EXECUTAR - APENAS REFERÊNCIA)
-- ================================================================================
/*
-- Estes índices melhorariam a performance das consultas acima:

CREATE INDEX idx_crm_negocio_date_create ON crm_negocio(date_create);
CREATE INDEX idx_crm_negocio_id_user ON crm_negocio(id_user);
CREATE INDEX idx_crm_negocio_id_state ON crm_negocio(id_state);
CREATE INDEX idx_crm_negocio_origem ON crm_negocio(origem);
CREATE INDEX idx_crm_negocio_composite ON crm_negocio(date_create, id_state, id_user);
*/

