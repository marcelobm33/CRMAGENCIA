# Guia de Troubleshooting

Este guia ajuda a resolver problemas comuns do sistema CRM IA Campanhas.

## Problemas de Instalação

### Docker não encontrado

**Sintoma**: `./setup.sh` falha com "docker não encontrado"

**Solução**:
1. Instale o Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Inicie o Docker Desktop
3. Aguarde o ícone ficar verde
4. Execute `./setup.sh` novamente

### Permissão negada nos scripts

**Sintoma**: `./setup.sh: Permission denied`

**Solução**:
```bash
chmod +x setup.sh run_local.sh
```

### Porta já em uso

**Sintoma**: `Error: bind: address already in use`

**Solução**:
1. Identifique o processo usando a porta:
```bash
# Para porta 8000
lsof -i :8000

# Para porta 3000
lsof -i :3000
```

2. Pare o processo ou use portas diferentes no `docker-compose.yml`

### Erro de permissão do macOS

**Sintoma**: macOS pede permissão para acessar pastas

**Solução**:
- Clique em "Permitir" quando solicitado
- Isso só acontece uma vez por pasta

## Problemas de Banco de Dados

### Banco não conecta

**Sintoma**: `Connection refused` ou `could not connect to server`

**Soluções**:
1. Verifique se o container está rodando:
```bash
docker compose ps
```

2. Aguarde o banco inicializar (pode levar 30s):
```bash
docker compose logs db
```

3. Reinicie o banco:
```bash
docker compose restart db
```

### Migrations falhando

**Sintoma**: `alembic.util.exc.CommandError`

**Soluções**:
1. Verifique o status atual:
```bash
docker compose run --rm api alembic current
```

2. Force a atualização:
```bash
docker compose run --rm api alembic upgrade head
```

3. Se persistir, recrie o banco:
```bash
docker compose down -v
docker compose up -d
```

### Dados corrompidos

**Sintoma**: Erros SQL estranhos ou dados inconsistentes

**Solução**:
```bash
# Backup primeiro (se possível)
docker compose exec db pg_dump -U admin crm_campanhas > backup.sql

# Recrie o banco
docker compose down -v
docker compose up -d

# Restaure (opcional)
cat backup.sql | docker compose exec -T db psql -U admin crm_campanhas
```

## Problemas da API

### API retorna 500

**Sintoma**: Erro interno do servidor

**Diagnóstico**:
```bash
docker compose logs -f api
```

**Soluções comuns**:
1. Banco não está conectado - veja seção anterior
2. Migrations não rodaram:
```bash
docker compose run --rm api alembic upgrade head
```
3. Erro no código - verifique os logs

### API muito lenta

**Sintoma**: Requisições demoram mais de 5s

**Soluções**:
1. Verifique uso de recursos:
```bash
docker stats
```

2. Aumente recursos do Docker Desktop (Settings > Resources)

3. Reinicie os containers:
```bash
docker compose restart
```

### Autenticação falha

**Sintoma**: 401 Unauthorized em todas as rotas

**Soluções**:
1. Verifique se o usuário admin existe:
```bash
docker compose run --rm api python -c "
from infra.seeds.run_seeds import create_admin_user
import asyncio
asyncio.run(create_admin_user())
"
```

2. Redefina a senha via banco:
```bash
docker compose exec db psql -U admin crm_campanhas -c "
UPDATE users SET hashed_password = '\$2b\$12\$...' WHERE email = 'admin@revenda.com';
"
```

## Problemas do Frontend

### Dashboard não carrega

**Sintoma**: Página em branco ou erro 500

**Diagnóstico**:
```bash
docker compose logs -f web
```

**Soluções**:
1. Aguarde o build (primeira vez pode demorar 60s)

2. Reinicie o frontend:
```bash
docker compose restart web
```

3. Reconstrua a imagem:
```bash
docker compose build --no-cache web
docker compose up -d web
```

### Erro de CORS

**Sintoma**: `CORS policy: No 'Access-Control-Allow-Origin'`

**Solução**:
Verifique se a URL do frontend está na lista de origens permitidas em `apps/api/main.py`

### Gráficos não aparecem

**Sintoma**: Cards mostram dados mas gráficos estão vazios

**Soluções**:
1. Verifique se há dados no período selecionado
2. Abra o console do navegador (F12) e veja se há erros JS
3. Tente outro navegador

## Problemas do Worker

### Jobs não executam

**Sintoma**: Sync de campanhas não acontece

**Diagnóstico**:
```bash
docker compose logs -f worker
docker compose logs -f beat
```

**Soluções**:
1. Verifique se Redis está rodando:
```bash
docker compose exec redis redis-cli ping
# Deve retornar: PONG
```

2. Reinicie workers:
```bash
docker compose restart worker beat
```

### IA não gera insights

**Sintoma**: Página de IA vazia

**Soluções**:
1. Execute análise manualmente:
```bash
curl -X POST "http://localhost:8000/api/ai/analyze" \
  -H "Authorization: Bearer TOKEN"
```

2. Verifique modo da IA no `.env`:
```env
AI_MODE=mock  # Deve ser mock ou openai
```

## Problemas de Integração

### Google Ads não sincroniza

**Diagnóstico**:
1. Verifique configuração:
```bash
curl http://localhost:8000/api/integrations/status
```

2. Veja logs do worker:
```bash
docker compose logs -f worker | grep -i google
```

**Soluções**:
- Token expirado: gere novo refresh token
- Customer ID errado: confirme o ID sem hífens
- Developer token não aprovado: use token de teste

### Meta Ads não sincroniza

**Diagnóstico**:
```bash
docker compose logs -f worker | grep -i meta
```

**Soluções**:
- Token expirado: gere novo token
- Conta sem acesso: verifique permissões no Business Manager
- Ad Account ID errado: confirme que começa com `act_`

## Problemas de Performance

### Sistema lento

**Diagnóstico**:
```bash
# Ver uso de recursos
docker stats

# Ver processos do banco
docker compose exec db psql -U admin crm_campanhas -c "
SELECT pid, query, state FROM pg_stat_activity;
"
```

**Soluções**:
1. Aumente recursos no Docker Desktop
2. Limpe dados antigos:
```bash
docker compose exec db psql -U admin crm_campanhas -c "
DELETE FROM ad_spend_daily WHERE date < NOW() - INTERVAL '90 days';
"
```

3. Recrie containers:
```bash
docker compose down
docker compose up -d
```

### Disco cheio

**Sintoma**: `No space left on device`

**Solução**:
```bash
# Limpar recursos Docker não usados
docker system prune -a

# Limpar volumes antigos
docker volume prune
```

## Logs Importantes

### Onde encontrar logs

```bash
# Todos os serviços
docker compose logs

# Serviço específico
docker compose logs api
docker compose logs web
docker compose logs worker
docker compose logs db

# Em tempo real
docker compose logs -f api

# Últimas 100 linhas
docker compose logs --tail=100 api
```

### Exportar logs

```bash
docker compose logs > logs_$(date +%Y%m%d).txt
```

## Contato para Suporte

Se o problema persistir após tentar as soluções acima:

1. Colete os logs:
```bash
docker compose logs > logs.txt
```

2. Anote:
   - Passos para reproduzir o erro
   - Mensagem de erro exata
   - Versão do Docker e sistema operacional

3. Abra uma issue ou entre em contato com suporte.

