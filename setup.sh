#!/bin/bash

# ===========================================
# CRM IA CAMPANHAS - Script de Setup
# ===========================================
# Este script configura o ambiente de desenvolvimento
# Uso: ./setup.sh

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║           CRM IA CAMPANHAS - Setup Inicial                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Função para verificar comandos
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}✗ $1 não encontrado. Por favor, instale antes de continuar.${NC}"
        exit 1
    else
        echo -e "${GREEN}✓ $1 encontrado${NC}"
    fi
}

# 1. Verificar dependências
echo -e "\n${YELLOW}[1/6] Verificando dependências...${NC}"
check_command docker
check_command docker-compose || check_command "docker compose"

# Verificar se Docker está rodando
if ! docker info &> /dev/null; then
    echo -e "${RED}✗ Docker não está rodando. Por favor, inicie o Docker Desktop.${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Docker está rodando${NC}"
fi

# 2. Configurar arquivo .env
echo -e "\n${YELLOW}[2/6] Configurando variáveis de ambiente...${NC}"
if [ ! -f .env ]; then
    if [ -f env.example ]; then
        cp env.example .env
        echo -e "${GREEN}✓ Arquivo .env criado a partir de env.example${NC}"
        echo -e "${YELLOW}  IMPORTANTE: Edite o arquivo .env com suas configurações${NC}"
    else
        echo -e "${RED}✗ Arquivo env.example não encontrado${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Arquivo .env já existe${NC}"
fi

# 3. Criar diretórios necessários
echo -e "\n${YELLOW}[3/6] Criando estrutura de diretórios...${NC}"
mkdir -p apps/api apps/web apps/worker packages/shared infra/migrations/versions infra/seeds infra/scripts docs
echo -e "${GREEN}✓ Diretórios criados${NC}"

# 4. Build das imagens Docker
echo -e "\n${YELLOW}[4/6] Construindo imagens Docker (pode demorar na primeira vez)...${NC}"
docker compose build --no-cache
echo -e "${GREEN}✓ Imagens construídas${NC}"

# 5. Subir banco de dados e rodar migrations
echo -e "\n${YELLOW}[5/6] Iniciando banco de dados e rodando migrations...${NC}"
docker compose up -d db redis
echo "Aguardando banco de dados ficar pronto..."
sleep 10

# Rodar migrations
docker compose run --rm api alembic upgrade head
echo -e "${GREEN}✓ Migrations executadas${NC}"

# 6. Popular dados de exemplo
echo -e "\n${YELLOW}[6/6] Populando dados de exemplo (seeds)...${NC}"
docker compose run --rm api python -m infra.seeds.run_seeds
echo -e "${GREEN}✓ Dados de exemplo criados${NC}"

# Parar serviços
docker compose down

echo -e "\n${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Setup Concluído!                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "Próximos passos:"
echo "  1. Revise o arquivo .env com suas configurações"
echo "  2. Execute ./run_local.sh para iniciar o sistema"
echo ""
echo -e "${BLUE}Documentação: docs/README.md${NC}"

