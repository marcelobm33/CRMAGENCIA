# CRM IA Campanhas

Sistema de CRM com integração de campanhas Google Ads e Meta Ads, dashboard de performance e IA analista para insights automáticos.

## Visão Geral

Este sistema foi desenvolvido para revendas de carros que querem:
- Acompanhar performance de campanhas de marketing digital
- Relacionar investimento em ads com vendas realizadas
- Receber insights automáticos para melhorar resultados

## Funcionalidades

- **Dashboard de Métricas**: Visão geral, por canal, por campanha e por vendedor
- **Integração com Ads**: Google Ads e Meta Ads (modo mock ou live)
- **Atribuição**: Liga leads/negócios às campanhas que os geraram
- **IA Analista**: Gera recomendações automáticas baseadas nos dados
- **Importação de CRM**: Aceita CSV e JSON

## Requisitos

- Docker e Docker Compose
- macOS, Linux ou Windows com WSL2

## Início Rápido

### 1. Clone ou baixe o projeto

```bash
cd /caminho/para/CRM\ IA\ CAMPANHAS
```

### 2. Configure as variáveis de ambiente

```bash
cp env.example .env
```

Edite o arquivo `.env` se necessário (os padrões funcionam para desenvolvimento).

### 3. Execute o setup

```bash
chmod +x setup.sh run_local.sh
./setup.sh
```

### 4. Inicie o sistema

```bash
./run_local.sh
```

### 5. Acesse o dashboard

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

**Credenciais padrão:**
- Email: admin@revenda.com
- Senha: admin123

## Estrutura do Projeto

```
CRM IA CAMPANHAS/
├── docker-compose.yml    # Orquestração de containers
├── setup.sh              # Script de configuração inicial
├── run_local.sh          # Script para iniciar o sistema
├── env.example           # Exemplo de variáveis de ambiente
│
├── apps/
│   ├── api/              # Backend FastAPI
│   ├── web/              # Frontend Next.js
│   └── worker/           # Jobs Celery
│
├── infra/
│   ├── migrations/       # Migrations do banco (Alembic)
│   └── seeds/            # Dados de exemplo
│
└── docs/                 # Documentação adicional
```

## Importando Dados do CRM

### Via CSV

O sistema aceita arquivos CSV com as seguintes colunas:

| Coluna | Obrigatória | Descrição |
|--------|-------------|-----------|
| vendedor | Sim | Nome do vendedor |
| valor | Não | Valor do negócio |
| lucro_bruto | Não | Lucro bruto |
| status | Não | aberto, ganho ou perdido |
| motivo_perda | Não | Motivo da perda (se perdido) |
| data_criacao | Não | Data de criação (YYYY-MM-DD ou DD/MM/YYYY) |
| telefone | Não | Telefone do cliente |
| email | Não | Email do cliente |
| nome_cliente | Não | Nome do cliente |
| origem | Não | Origem do lead |
| canal | Não | Canal (Google, Meta, etc.) |
| utm_source | Não | Parâmetro UTM source |
| utm_campaign | Não | Parâmetro UTM campaign |
| veiculo_interesse | Não | Veículo de interesse |

Exemplo de CSV:

```csv
vendedor,valor,status,canal,utm_source,utm_campaign,nome_cliente,telefone
Carlos Silva,85000,ganho,Google,google,busca_seminovos,João Santos,11999887766
Maria Santos,0,perdido,Meta,facebook,leads_especiais,Ana Costa,11988776655
```

### Via API

```bash
curl -X POST "http://localhost:8000/api/crm/import" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -F "file=@dados.csv"
```

## Configurando Integrações

### Google Ads (Opcional)

Para conectar sua conta Google Ads, veja [docs/SETUP_GOOGLE.md](docs/SETUP_GOOGLE.md).

### Meta Ads (Opcional)

Para conectar sua conta Meta Ads, veja [docs/SETUP_META.md](docs/SETUP_META.md).

**Nota**: O sistema funciona em modo mock sem configurar as integrações. Dados de campanha serão simulados.

## Comandos Úteis

```bash
# Ver logs de todos os serviços
docker compose logs -f

# Ver logs só da API
docker compose logs -f api

# Reiniciar um serviço
docker compose restart api

# Parar tudo
docker compose down

# Parar e remover dados
docker compose down -v

# Rodar migrations manualmente
docker compose run --rm api alembic upgrade head

# Executar seeds novamente
docker compose run --rm api python -m infra.seeds.run_seeds
```

## Troubleshooting

### Docker não inicia

1. Verifique se o Docker Desktop está rodando
2. Verifique se não há outro serviço nas portas 3000, 5432, 6379 ou 8000
3. Execute `docker compose down` e tente novamente

### Erro de conexão com banco

1. Aguarde o banco inicializar completamente (pode levar 30s na primeira vez)
2. Verifique se as credenciais no `.env` estão corretas
3. Tente `docker compose restart db api`

### Frontend não carrega

1. Aguarde o build do Next.js (pode levar 60s na primeira vez)
2. Verifique os logs: `docker compose logs -f web`
3. Tente `docker compose restart web`

### API retorna 500

1. Verifique os logs: `docker compose logs -f api`
2. Verifique se as migrations rodaram: `docker compose run --rm api alembic current`
3. Rode as migrations: `docker compose run --rm api alembic upgrade head`

## Desenvolvendo

### Rodando localmente (sem Docker)

**Backend:**
```bash
cd apps/api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd apps/web
npm install
npm run dev
```

### Criando novas migrations

```bash
docker compose run --rm api alembic revision --autogenerate -m "descricao"
```

## Arquitetura

```
┌─────────────────┐     ┌─────────────────┐
│   Next.js Web   │────▶│  FastAPI (API)  │
│   (Dashboard)   │     │   Port 8000     │
│   Port 3000     │     └────────┬────────┘
└─────────────────┘              │
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  PostgreSQL   │      │     Redis       │      │  Celery Worker  │
│   Port 5432   │      │   Port 6379     │      │  (Background)   │
└───────────────┘      └─────────────────┘      └─────────────────┘
                                                         │
                                    ┌────────────────────┼────────────────────┐
                                    │                    │                    │
                                    ▼                    ▼                    ▼
                            ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
                            │  Google Ads  │   │   Meta Ads   │   │ IA Analyst   │
                            │     API      │   │     API      │   │   (OpenAI)   │
                            └──────────────┘   └──────────────┘   └──────────────┘
```

## Licença

Projeto privado - todos os direitos reservados.

## Suporte

Para dúvidas ou problemas, consulte a documentação em `/docs` ou abra uma issue.

