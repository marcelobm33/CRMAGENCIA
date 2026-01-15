"""
Seed simples de campanhas - sem dependências complexas
"""
import pymysql
from datetime import datetime, timedelta

# Conectar ao banco local
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='crm_ia_campanhas',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    cursor = conn.cursor()
    
    # Criar tabela se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS campaigns (
        id INT AUTO_INCREMENT PRIMARY KEY,
        external_id VARCHAR(100) UNIQUE,
        name VARCHAR(255) NOT NULL,
        platform ENUM('meta', 'google') NOT NULL,
        status ENUM('active', 'paused', 'completed') DEFAULT 'active',
        impressions INT DEFAULT 0,
        clicks INT DEFAULT 0,
        spend FLOAT DEFAULT 0.0,
        cpc FLOAT DEFAULT 0.0,
        ctr FLOAT DEFAULT 0.0,
        leads_generated INT DEFAULT 0,
        sales_closed INT DEFAULT 0,
        revenue FLOAT DEFAULT 0.0,
        cpl FLOAT DEFAULT 0.0,
        conversion_rate FLOAT DEFAULT 0.0,
        roi FLOAT DEFAULT 0.0,
        roas FLOAT DEFAULT 0.0,
        start_date DATETIME,
        end_date DATETIME,
        last_sync DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        extra_data TEXT,
        INDEX idx_platform (platform),
        INDEX idx_status (status),
        INDEX idx_external_id (external_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    
    # Limpar dados existentes
    cursor.execute("DELETE FROM campaigns")
    
    # Dados de exemplo
    campaigns = [
        # META
        ('meta_001', 'Busca - Seminovos Premium', 'meta', 'active', 50000, 380, 1250.00, 45, 12, 145000.00, 30),
        ('meta_002', 'Leads - Ofertas Especiais', 'meta', 'active', 75000, 520, 980.00, 38, 10, 118000.00, 25),
        ('meta_003', 'Busca - Carros Usados SP', 'meta', 'active', 42000, 285, 1532.00, 32, 5, 62000.00, 20),
        ('meta_004', 'Remarketing - Visitantes', 'meta', 'active', 28000, 420, 655.00, 28, 4, 48000.00, 15),
        ('meta_005', 'Display - Remarketing', 'meta', 'paused', 95000, 180, 420.00, 8, 1, 12000.00, 10),
        ('meta_006', 'Busca - Financiamento', 'meta', 'active', 38000, 245, 1331.50, 13, 0, 0.00, 5),
        # GOOGLE
        ('google_001', 'Busca - Seminovos Premium', 'google', 'active', 65000, 520, 1250.00, 45, 12, 145000.00, 30),
        ('google_002', 'Leads - Ofertas Especiais', 'google', 'active', 48000, 380, 980.00, 38, 10, 118000.00, 25),
        ('google_003', 'Busca - Carros Usados SP', 'google', 'active', 55000, 425, 1532.00, 32, 5, 62000.00, 20),
        ('google_004', 'Remarketing - Visitantes', 'google', 'active', 32000, 285, 655.00, 28, 4, 48000.00, 15),
        ('google_005', 'Display - Remarketing', 'google', 'active', 78000, 195, 420.00, 8, 1, 12000.00, 10),
    ]
    
    for camp in campaigns:
        external_id, name, platform, status, impressions, clicks, spend, leads, sales, revenue, days_ago = camp
        
        # Calcular métricas
        cpc = spend / clicks if clicks > 0 else 0
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpl = spend / leads if leads > 0 else 0
        conversion_rate = (sales / leads * 100) if leads > 0 else 0
        roi = ((revenue - spend) / spend * 100) if spend > 0 else 0
        roas = (revenue / spend) if spend > 0 else 0
        
        start_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
        INSERT INTO campaigns (
            external_id, name, platform, status,
            impressions, clicks, spend, cpc, ctr,
            leads_generated, sales_closed, revenue,
            cpl, conversion_rate, roi, roas,
            start_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            external_id, name, platform, status,
            impressions, clicks, spend, round(cpc, 2), round(ctr, 2),
            leads, sales, revenue,
            round(cpl, 2), round(conversion_rate, 2), round(roi, 2), round(roas, 2),
            start_date
        ))
    
    conn.commit()
    print(f"✅ {len(campaigns)} campanhas criadas com sucesso!")
    print(f"   • Meta: {len([c for c in campaigns if c[2] == 'meta'])} campanhas")
    print(f"   • Google: {len([c for c in campaigns if c[2] == 'google'])} campanhas")
    
finally:
    conn.close()

print("\n✨ Pronto! Acesse http://localhost:8000/api/campaigns para ver as campanhas.")

