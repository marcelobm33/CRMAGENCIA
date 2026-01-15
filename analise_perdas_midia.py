#!/usr/bin/env python3
"""
Análise: O que aconteceu com os leads de META e GOOGLE?
"""
import pymysql
from pymysql.cursors import DictCursor

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
print("🔍 O QUE ACONTECEU COM OS LEADS DE MÍDIA PAGA?")
print("=" * 70)

# 1. Status dos leads de META e GOOGLE nos últimos 3 meses
print("\n📊 STATUS DOS LEADS DE MÍDIA PAGA (OUT-NOV-DEZ 2025)")
print("-" * 70)

query_status = """
SELECT 
    CASE 
        WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
    END AS canal,
    CASE id_state
        WHEN 1 THEN '1-Novo'
        WHEN 2 THEN '2-Em Atendimento'
        WHEN 3 THEN '3-Proposta'
        WHEN 4 THEN '4-Negociacao'
        WHEN 5 THEN '5-Fechamento'
        WHEN 6 THEN '6-GANHO'
        WHEN 7 THEN '7-PERDIDO'
        WHEN 8 THEN '8-Arquivado'
    END AS status,
    COUNT(*) AS quantidade
FROM crm_negocio
WHERE origem IN ('FACEBOOK', 'INSTAGRAM', 'Google', 'GOOGLE')
  AND date_create >= '2025-10-01'
GROUP BY canal, status
ORDER BY canal, id_state
"""

with conn.cursor() as cursor:
    cursor.execute(query_status)
    status = cursor.fetchall()

current_canal = None
for s in status:
    if s['canal'] != current_canal:
        if current_canal:
            print()
        print(f"\n  📱 {s['canal']}:")
        current_canal = s['canal']
    print(f"      {s['status']:20} → {s['quantidade']:3} leads")

# 2. Motivos de perda dos leads de mídia paga
print("\n" + "=" * 70)
print("❌ MOTIVOS DE PERDA - LEADS DE MÍDIA PAGA (últimos 3 meses)")
print("-" * 70)

query_motivos = """
SELECT 
    CASE 
        WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
    END AS canal,
    COALESCE(motivo_perda, 'NÃO INFORMADO') AS motivo,
    COUNT(*) AS quantidade
FROM crm_negocio
WHERE origem IN ('FACEBOOK', 'INSTAGRAM', 'Google', 'GOOGLE')
  AND id_state = 7
  AND date_create >= '2025-10-01'
GROUP BY canal, motivo
ORDER BY canal, quantidade DESC
"""

with conn.cursor() as cursor:
    cursor.execute(query_motivos)
    motivos = cursor.fetchall()

current_canal = None
for m in motivos:
    if m['canal'] != current_canal:
        if current_canal:
            print()
        print(f"\n  📱 {m['canal']}:")
        current_canal = m['canal']
    print(f"      {m['motivo'][:40]:40} → {m['quantidade']:3}")

# 3. Tempo até perda - quanto tempo levou para marcar como perdido?
print("\n" + "=" * 70)
print("⏱️ TEMPO ATÉ PERDA - Quanto tempo levou para desistir?")
print("-" * 70)

query_tempo_perda = """
SELECT 
    CASE 
        WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
    END AS canal,
    ROUND(AVG(DATEDIFF(date_update, date_create)), 1) AS dias_medio,
    MIN(DATEDIFF(date_update, date_create)) AS dias_min,
    MAX(DATEDIFF(date_update, date_create)) AS dias_max,
    COUNT(*) AS total_perdas
FROM crm_negocio
WHERE origem IN ('FACEBOOK', 'INSTAGRAM', 'Google', 'GOOGLE')
  AND id_state = 7
  AND date_create >= '2025-10-01'
GROUP BY canal
"""

with conn.cursor() as cursor:
    cursor.execute(query_tempo_perda)
    tempo_perda = cursor.fetchall()

for t in tempo_perda:
    print(f"  {t['canal']:8} | {t['total_perdas']:3} perdas | Média: {t['dias_medio']:5} dias | Min: {t['dias_min']:3}d | Max: {t['dias_max']:3}d")

# 4. Comparar taxa de conversão por origem
print("\n" + "=" * 70)
print("📈 TAXA DE CONVERSÃO POR ORIGEM (últimos 3 meses)")
print("-" * 70)

query_conversao = """
SELECT 
    CASE 
        WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
        WHEN origem IN ('SITE') THEN 'SITE'
        WHEN origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO') THEN 'INDICACAO'
        WHEN origem IN ('SHOWROOM', 'NA PISTA', 'FEIRÃO') THEN 'PRESENCIAL'
        ELSE 'OUTROS'
    END AS canal,
    COUNT(*) AS total_leads,
    SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
    SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
    SUM(CASE WHEN id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS ativos
FROM crm_negocio
WHERE date_create >= '2025-10-01'
GROUP BY canal
ORDER BY ganhos DESC
"""

with conn.cursor() as cursor:
    cursor.execute(query_conversao)
    conversao = cursor.fetchall()

print(f"  {'CANAL':12} | {'LEADS':>6} | {'GANHOS':>6} | {'PERDIDOS':>8} | {'ATIVOS':>6} | {'CONVERSÃO':>10}")
print("  " + "-" * 65)

for c in conversao:
    total = c['ganhos'] + c['perdidos']
    taxa = (c['ganhos'] / total * 100) if total > 0 else 0
    print(f"  {c['canal']:12} | {c['total_leads']:>6} | {c['ganhos']:>6} | {c['perdidos']:>8} | {c['ativos']:>6} | {taxa:>9.1f}%")

# 5. Analisar os leads de META que GANHARAM - quem era o vendedor?
print("\n" + "=" * 70)
print("🏆 VENDAS DE MÍDIA PAGA - Quem conseguiu vender?")
print("-" * 70)

query_vendas = """
SELECT 
    CASE 
        WHEN n.origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
        WHEN n.origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
    END AS canal,
    u.name AS vendedor,
    n.titulo AS veiculo,
    n.valor,
    n.date_create AS entrada,
    n.date_update AS fechamento,
    DATEDIFF(n.date_update, n.date_create) AS dias
FROM crm_negocio n
LEFT JOIN users u ON n.id_user = u.id_users
WHERE n.origem IN ('FACEBOOK', 'INSTAGRAM', 'Google', 'GOOGLE')
  AND n.id_state = 6
  AND n.date_create >= '2025-10-01'
ORDER BY n.date_update DESC
"""

with conn.cursor() as cursor:
    cursor.execute(query_vendas)
    vendas = cursor.fetchall()

if vendas:
    for v in vendas:
        print(f"  {v['canal']:6} | {v['vendedor'] or 'N/A':12} | R$ {v['valor'] or 0:>10,.2f} | {v['dias']}d | {(v['veiculo'] or '')[:30]}")
else:
    print("  ⚠️ Nenhuma venda de mídia paga nos últimos 3 meses!")

# 6. Quem são os vendedores que recebem leads de mídia paga?
print("\n" + "=" * 70)
print("👥 DISTRIBUIÇÃO DE LEADS DE MÍDIA PAGA POR VENDEDOR")
print("-" * 70)

query_vendedores = """
SELECT 
    u.name AS vendedor,
    COUNT(*) AS leads_recebidos,
    SUM(CASE WHEN n.id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
    SUM(CASE WHEN n.id_state = 7 THEN 1 ELSE 0 END) AS perdidos
FROM crm_negocio n
LEFT JOIN users u ON n.id_user = u.id_users
WHERE n.origem IN ('FACEBOOK', 'INSTAGRAM', 'Google', 'GOOGLE')
  AND n.date_create >= '2025-10-01'
GROUP BY n.id_user, u.name
ORDER BY leads_recebidos DESC
"""

with conn.cursor() as cursor:
    cursor.execute(query_vendedores)
    vendedores = cursor.fetchall()

print(f"  {'VENDEDOR':15} | {'LEADS':>6} | {'GANHOS':>6} | {'PERDIDOS':>8} | {'CONVERSÃO':>10}")
print("  " + "-" * 55)

for v in vendedores:
    total = v['ganhos'] + v['perdidos']
    taxa = (v['ganhos'] / total * 100) if total > 0 else 0
    print(f"  {(v['vendedor'] or 'N/A'):15} | {v['leads_recebidos']:>6} | {v['ganhos']:>6} | {v['perdidos']:>8} | {taxa:>9.1f}%")

conn.close()

print("\n" + "=" * 70)
print("✅ Análise concluída!")
print("=" * 70)
