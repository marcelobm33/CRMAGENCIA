"""
Configuração do Celery
"""
from celery import Celery
from celery.schedules import crontab
from config import get_settings

settings = get_settings()

# Criar app Celery
app = Celery(
    'crm_worker',
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        'tasks.sync_google',
        'tasks.sync_meta',
        'tasks.kpi_calculator',
        'tasks.ai_analyst',
        'tasks.sync_crm'
    ]
)

# Configurações
app.conf.update(
    # Serialização
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Timezone
    timezone='America/Sao_Paulo',
    enable_utc=True,
    
    # Retry
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Resultados
    result_expires=3600,  # 1 hora
    
    # Concorrência
    worker_prefetch_multiplier=1,
    worker_concurrency=4,
)

# Agendamento de tasks (Celery Beat)
app.conf.beat_schedule = {
    # ========================================
    # CRM EXTERNO (netcarrc01) - Tempo Real
    # ========================================
    
    # Verificar conexão a cada 2 minutos
    'check-crm-connection': {
        'task': 'check_crm_connection',
        'schedule': crontab(minute='*/2'),
        'args': ()
    },
    
    # Sincronizar CRM a cada 5 minutos (incremental)
    'sync-crm-incremental': {
        'task': 'sync_crm_external',
        'schedule': crontab(minute='*/5'),
        'args': (1,)  # Último dia
    },
    
    # KPIs em tempo real a cada 3 minutos
    'realtime-kpis': {
        'task': 'get_realtime_kpis',
        'schedule': crontab(minute='*/3'),
        'args': ()
    },
    
    # ========================================
    # CAMPANHAS EXTERNAS
    # ========================================
    
    # Sincronizar campanhas a cada hora
    'sync-google-hourly': {
        'task': 'tasks.sync_google.sync_google_ads',
        'schedule': crontab(minute=0),  # A cada hora
        'args': ()
    },
    'sync-meta-hourly': {
        'task': 'tasks.sync_meta.sync_meta_ads',
        'schedule': crontab(minute=5),  # 5 min após a hora
        'args': ()
    },
    
    # ========================================
    # ANALYTICS E IA
    # ========================================
    
    # Calcular KPIs a cada 6 horas
    'calculate-kpis': {
        'task': 'tasks.kpi_calculator.calculate_daily_kpis',
        'schedule': crontab(minute=30, hour='*/6'),  # A cada 6h
        'args': ()
    },
    
    # Rodar IA Analyst a cada 6 horas
    'run-ai-analyst': {
        'task': 'tasks.ai_analyst.run_analysis',
        'schedule': crontab(minute=0, hour='6,12,18'),  # 3x ao dia
        'args': ()
    },
    
    # Reprocessar últimos 7 dias (1x por dia às 3h)
    'reprocess-week': {
        'task': 'tasks.sync_google.reprocess_last_7_days',
        'schedule': crontab(minute=0, hour=3),
        'args': ()
    }
}

# Export para uso em tasks
celery_app = app

if __name__ == '__main__':
    app.start()

