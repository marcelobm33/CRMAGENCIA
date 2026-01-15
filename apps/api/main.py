"""
CRM IA Campanhas - API Principal
FastAPI Application
"""
import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import get_settings
from database import init_db, close_db

# Importar routers
from routers import crm, campaigns, analytics, ai_analyst, integrations, auth
from routers import crm_sync, roi_analysis

# Configurar logging estruturado
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    logger.info("Iniciando CRM IA Campanhas API...")
    # Startup
    await init_db()
    logger.info("Banco de dados inicializado")
    
    yield
    
    # Shutdown
    await close_db()
    logger.info("API encerrada")


# Criar aplicação FastAPI
app = FastAPI(
    title="CRM IA Campanhas",
    description="""
    Sistema de CRM com integração de campanhas Google Ads e Meta Ads.
    
    ## Funcionalidades
    
    * **CRM**: Gestão de negócios/deals da revenda
    * **Campanhas**: Sincronização com Google Ads e Meta Ads
    * **Analytics**: Dashboard de métricas e KPIs
    * **IA Analista**: Insights e recomendações automáticas
    
    ## Autenticação
    
    Use o endpoint `/auth/login` para obter um token JWT.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Handler de exceções global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Erro não tratado", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )


# Health check
@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verifica se a API está funcionando"""
    return {
        "status": "healthy",
        "service": "crm-ia-campanhas-api",
        "version": "1.0.0",
        "environment": settings.environment
    }


@app.get("/", tags=["Sistema"])
async def root():
    """Página inicial da API"""
    return {
        "message": "CRM IA Campanhas API",
        "docs": "/docs",
        "health": "/health"
    }


# Registrar routers
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(crm.router, prefix="/api/crm", tags=["CRM"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["Campanhas"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(ai_analyst.router, prefix="/api/ai", tags=["IA Analista"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["Integrações"])
app.include_router(crm_sync.router, prefix="/api/crm-sync", tags=["CRM Sync"])
app.include_router(roi_analysis.router, prefix="/api/roi", tags=["ROI Analysis"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development"
    )

