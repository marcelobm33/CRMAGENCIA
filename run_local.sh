#!/bin/bash

# ===========================================
# CRM IA CAMPANHAS - Script de Execução Local
# ===========================================
# Este script inicia todos os serviços
# Uso: ./run_local.sh

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║           CRM IA CAMPANHAS - Iniciando Sistema            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar se .env existe
if [ ! -f .env ]; then
    echo -e "${RED}✗ Arquivo .env não encontrado. Execute ./setup.sh primeiro.${NC}"
    exit 1
fi

# Verificar se Docker está rodando
if ! docker info &> /dev/null; then
    echo -e "${RED}✗ Docker não está rodando. Por favor, inicie o Docker Desktop.${NC}"
    exit 1
fi

# Iniciar serviços
echo -e "${YELLOW}Iniciando todos os serviços...${NC}"
docker compose up -d

# Aguardar serviços ficarem prontos
echo -e "${YELLOW}Aguardando serviços ficarem prontos...${NC}"

# Função para verificar health de um serviço
wait_for_service() {
    local service=$1
    local url=$2
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $service está pronto${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    echo -e "${RED}✗ $service não respondeu após $max_attempts tentativas${NC}"
    return 1
}

echo -n "API"
wait_for_service "API" "http://localhost:8000/health"

echo -n "Dashboard"
wait_for_service "Dashboard" "http://localhost:3000"

# Exibir status
echo -e "\n${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                Sistema Iniciado com Sucesso!              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo -e "${CYAN}URLs disponíveis:${NC}"
echo ""
echo -e "  📊 Dashboard:     ${GREEN}http://localhost:3000${NC}"
echo -e "  🔌 API:           ${GREEN}http://localhost:8000${NC}"
echo -e "  📚 API Docs:      ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  📖 ReDoc:         ${GREEN}http://localhost:8000/redoc${NC}"
echo ""
echo -e "${CYAN}Credenciais padrão:${NC}"
echo "  Email: admin@revenda.com"
echo "  Senha: admin123"
echo ""
echo -e "${YELLOW}Comandos úteis:${NC}"
echo "  docker compose logs -f          # Ver logs em tempo real"
echo "  docker compose logs -f api      # Ver logs só da API"
echo "  docker compose down             # Parar todos os serviços"
echo "  docker compose restart api      # Reiniciar API"
echo ""
echo -e "${BLUE}Para parar: docker compose down${NC}"

