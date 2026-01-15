#!/usr/bin/env python3
"""
Análise do Ciclo de Venda - Tempo entre lead e fechamento
"""
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime

# Credenciais
HOST = "mysql.netcar-rc.com.br"
PORT = 3306
DATABASE = "netcarrc01"
USER = "netcarrc01_add1"
PASSWORD = "Banco@netcar"

conn = pymysql.connect(
    host=HOST, port=PORT, database=DATABASE,
    user=USER, password=PASSWORD,
    cursorclass=DictCursor, charset='utf8mb4'
)

print("=" * 70)
print("📊 ANÁLISE DO CICLO DE VENDA")
print("=" * 70)

# 1. Tempo médio entre criação e fechamento (vendas GANHAS)
print("\n🕐 TEMPO MÉDIO PARA FECHAR VENDA (últimos 6 meses)")
print("-" * 70)

query_tempo = """
SELECT 
    CASE 
        WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
        WHEN origem IN ('SITE') THEN 'SITE'
        WHEN origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO') THEN 'INDICACAO'
        WHEN origem IN ('SHOWROOM', 'NA PISTA', 'FEIRÃO') THEN 'PRESENCIAL'
        ELSE 'OUTROS'
    END AS canal,
    COUNT(*) AS vendas,
    ROUND(AVG(DATEDIFF(date_update, date_create)), 1) AS dias_medio,
    MIN(DATEDIFF(date_update, date_create)) AS dias_min,
    MAX(DATEDIFF(date_update, date_create)) AS dias_max
FROM crm_negocio
WHERE id_state = 6
  AND date_create >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY canal
ORDER BY vendas DESC
"""

with conn.cursor() as cursor:
    cursor.execute(query_tempo)
    tempos = cursor.fetchall()

for t in tempos:
    print(f"  {t['canal']:12} | {t['vendas']:3} vendas | Média: {t['dias_medio']:5} dias | Min: {t['dias_min']:3}d | Max: {t['dias_max']:3}d")

# 2. Leads de novembro que viraram vendas em dezembro
print("\n" + "=" * 70)
print("📈 LEADS DE NOVEMBRO → VENDAS EM DEZEMBRO")
print("-" * 70)

query_nov_dez = """
SELECT 
    CASE 
        WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
        WHEN origem IN ('SITE') THEN 'SITE'
        WHEN origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO') THEN 'INDICACAO'
        ELSE 'OUTROS'
    END AS canal,
    COUNT(*) AS vendas,
    SUM(valor) AS valor_vendido,
    ROUND(AVG(DATEDIFF(date_update, date_create)), 1) AS dias_para_fechar
FROM crm_negocio
WHERE id_state = 6
  AND YEAR(date_create) = 2025 AND MONTH(date_create) = 11
  AND YEAR(date_update) = 2025 AND MONTH(date_update) = 12
GROUP BY canal
ORDER BY vendas DESC
"""

with conn.cursor() as cursor:
    cursor.execute(query_nov_dez)
    nov_dez = cursor.fetchall()

total_vendas_nov = 0
total_valor_nov = 0
for v in nov_dez:
    valor = float(v['valor_vendido'] or 0)
    total_vendas_nov += v['vendas']
    total_valor_nov += valor
    print(f"  {v['canal']:12} | {v['vendas']:3} vendas | R$ {valor:>12,.2f} | Levou {v['dias_para_fechar']} dias")

print(f"\n  TOTAL: {total_vendas_nov} vendas de leads de NOV fechados em DEZ = R$ {total_valor_nov:,.2f}")

# 3. Leads de outubro que viraram vendas em dezembro
print("\n" + "=" * 70)
print("📈 LEADS DE OUTUBRO → VENDAS EM DEZEMBRO")
print("-" * 70)

query_out_dez = """
SELECT 
    CASE 
        WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
        WHEN origem IN ('SITE') THEN 'SITE'
        WHEN origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO') THEN 'INDICACAO'
        ELSE 'OUTROS'
    END AS canal,
    COUNT(*) AS vendas,
    SUM(valor) AS valor_vendido,
    ROUND(AVG(DATEDIFF(date_update, date_create)), 1) AS dias_para_fechar
FROM crm_negocio
WHERE id_state = 6
  AND YEAR(date_create) = 2025 AND MONTH(date_create) = 10
  AND YEAR(date_update) = 2025 AND MONTH(date_update) = 12
GROUP BY canal
ORDER BY vendas DESC
"""

with conn.cursor() as cursor:
    cursor.execute(query_out_dez)
    out_dez = cursor.fetchall()

total_vendas_out = 0
total_valor_out = 0
for v in out_dez:
    valor = float(v['valor_vendido'] or 0)
    total_vendas_out += v['vendas']
    total_valor_out += valor
    print(f"  {v['canal']:12} | {v['vendas']:3} vendas | R$ {valor:>12,.2f} | Levou {v['dias_para_fechar']} dias")

print(f"\n  TOTAL: {total_vendas_out} vendas de leads de OUT fechados em DEZ = R$ {total_valor_out:,.2f}")

# 4. Análise de vendas de dezembro por mês de entrada do lead
print("\n" + "=" * 70)
print("📊 VENDAS DE DEZEMBRO: De qual mês veio o lead?")
print("-" * 70)

query_origem_vendas = """
SELECT 
    DATE_FORMAT(date_create, '%Y-%m') AS mes_entrada,
    COUNT(*) AS vendas,
    SUM(valor) AS valor,
    ROUND(AVG(DATEDIFF(date_update, date_create)), 1) AS dias_medio
FROM crm_negocio
WHERE id_state = 6
  AND YEAR(date_update) = 2025 AND MONTH(date_update) = 12
GROUP BY mes_entrada
ORDER BY mes_entrada DESC
"""

with conn.cursor() as cursor:
    cursor.execute(query_origem_vendas)
    origem_vendas = cursor.fetchall()

for v in origem_vendas:
    valor = float(v['valor'] or 0)
    print(f"  Lead de {v['mes_entrada']} → {v['vendas']:3} vendas em DEZ | R$ {valor:>12,.2f} | Ciclo: {v['dias_medio']} dias")

# 5. ROI CORRIGIDO - Considerando ciclo de venda
print("\n" + "=" * 70)
print("💰 ROI CORRIGIDO (Considerando ciclo de 30-60 dias)")
print("-" * 70)

# Investimento de OUT + NOV para vendas de DEZ
inv_out = 15500  # Outubro
inv_nov = 15628  # Novembro

# Vendas de DEZ que vieram de leads de OUT + NOV (META + GOOGLE)
query_roi_corrigido = """
SELECT 
    CASE 
        WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
    END AS canal,
    COUNT(*) AS vendas,
    SUM(valor) AS valor_vendido
FROM crm_negocio
WHERE id_state = 6
  AND origem IN ('FACEBOOK', 'INSTAGRAM', 'Google', 'GOOGLE')
  AND date_create >= '2025-10-01' AND date_create < '2025-12-01'
  AND date_update >= '2025-12-01' AND date_update < '2026-01-01'
GROUP BY canal
"""

with conn.cursor() as cursor:
    cursor.execute(query_roi_corrigido)
    roi_corrigido = cursor.fetchall()

print(f"\n  Investimento OUT + NOV (META + GOOGLE): R$ {inv_out + inv_nov:,.2f}")
print(f"\n  Vendas em DEZEMBRO de leads de OUT/NOV:")

total_vendas_midia = 0
total_valor_midia = 0
for r in roi_corrigido:
    if r['canal']:
        valor = float(r['valor_vendido'] or 0)
        total_vendas_midia += r['vendas']
        total_valor_midia += valor
        print(f"    {r['canal']}: {r['vendas']} vendas = R$ {valor:,.2f}")

print(f"\n  TOTAL mídia paga (OUT/NOV → DEZ): {total_vendas_midia} vendas = R$ {total_valor_midia:,.2f}")

if total_vendas_midia > 0:
    custo_por_venda = (inv_out + inv_nov) / total_vendas_midia
    roi = (total_valor_midia / (inv_out + inv_nov)) * 100
    print(f"\n  📊 Custo por venda (corrigido): R$ {custo_por_venda:,.2f}")
    print(f"  📊 ROI corrigido: {roi:.0f}%")
else:
    print(f"\n  ⚠️ Nenhuma venda de mídia paga (OUT/NOV) fechou em DEZ")

# 6. Projeção: Leads de DEZ que podem fechar em JAN
print("\n" + "=" * 70)
print("🔮 PROJEÇÃO: Leads de DEZEMBRO em andamento")
print("-" * 70)

query_projecao = """
SELECT 
    CASE 
        WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
        WHEN origem IN ('SITE') THEN 'SITE'
        WHEN origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO') THEN 'INDICACAO'
        ELSE 'OUTROS'
    END AS canal,
    COUNT(*) AS leads_ativos,
    SUM(valor) AS valor_potencial,
    id_state
FROM crm_negocio
WHERE id_state BETWEEN 1 AND 5
  AND YEAR(date_create) = 2025 AND MONTH(date_create) = 12
GROUP BY canal, id_state
ORDER BY canal, id_state
"""

with conn.cursor() as cursor:
    cursor.execute(query_projecao)
    projecao = cursor.fetchall()

canais = {}
for p in projecao:
    canal = p['canal']
    if canal not in canais:
        canais[canal] = {'leads': 0, 'valor': 0}
    canais[canal]['leads'] += p['leads_ativos']
    canais[canal]['valor'] += float(p['valor_potencial'] or 0)

for canal, dados in sorted(canais.items(), key=lambda x: x[1]['leads'], reverse=True):
    print(f"  {canal:12} | {dados['leads']:3} leads ativos | Potencial: R$ {dados['valor']:>12,.2f}")

conn.close()

print("\n" + "=" * 70)
print("✅ Análise concluída!")
print("=" * 70)
