# Configuração do Google Ads API

Este guia explica como configurar a integração com o Google Ads para sincronizar dados de campanhas automaticamente.

## Pré-requisitos

- Conta Google Ads ativa
- Acesso de administrador à conta
- Conta Google Cloud Platform (gratuita)

## Passo a Passo

### 1. Criar Projeto no Google Cloud

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Clique em "Selecionar projeto" > "Novo projeto"
3. Nome: "CRM IA Campanhas" (ou outro de sua preferência)
4. Clique em "Criar"
5. Aguarde a criação e selecione o projeto

### 2. Ativar a API do Google Ads

1. No menu lateral, vá em **APIs e Serviços** > **Biblioteca**
2. Busque por "Google Ads API"
3. Clique em **Google Ads API**
4. Clique em **Ativar**

### 3. Criar Credenciais OAuth 2.0

1. Vá em **APIs e Serviços** > **Credenciais**
2. Clique em **Criar credenciais** > **ID do cliente OAuth**
3. Se pedido, configure a tela de consentimento OAuth:
   - Tipo de usuário: **Interno** (se for G Suite) ou **Externo**
   - Preencha nome do app, email de suporte
   - Em escopos, adicione: `https://www.googleapis.com/auth/adwords`
4. Volte para credenciais e crie o OAuth Client ID:
   - Tipo de aplicativo: **Aplicativo da Web**
   - Nome: "CRM IA Campanhas"
   - URIs de redirecionamento: `http://localhost:8000/api/integrations/google/callback`
5. **Anote** o Client ID e Client Secret

### 4. Obter Developer Token

1. Acesse o [Google Ads API Center](https://ads.google.com/aw/apicenter)
2. Se você não tem um Developer Token:
   - Clique em "Solicitar token"
   - Para desenvolvimento, o token de teste é suficiente
3. **Anote** o Developer Token

### 5. Obter Customer ID

1. Acesse sua conta no [Google Ads](https://ads.google.com)
2. O Customer ID aparece no canto superior direito (formato: 123-456-7890)
3. **Anote** o ID sem os hífens: `1234567890`

### 6. Gerar Refresh Token

Este passo requer rodar um script localmente:

```bash
# Na pasta do projeto
cd apps/api

# Instale a biblioteca do Google
pip install google-auth-oauthlib

# Rode o script de autenticação
python scripts/google_oauth.py
```

O script vai:
1. Abrir o navegador para você autorizar
2. Imprimir o Refresh Token no terminal

**Anote** o Refresh Token.

### 7. Configurar o Sistema

Edite o arquivo `.env` com os valores obtidos:

```env
GOOGLE_ADS_DEVELOPER_TOKEN=seu_developer_token_aqui
GOOGLE_ADS_CLIENT_ID=seu_client_id.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=seu_client_secret
GOOGLE_ADS_REFRESH_TOKEN=seu_refresh_token
GOOGLE_ADS_CUSTOMER_ID=1234567890
```

### 8. Reiniciar o Sistema

```bash
docker compose down
docker compose up -d
```

### 9. Verificar Integração

Acesse http://localhost:8000/api/integrations/status

Você deve ver:
```json
{
  "integrations": [
    {
      "platform": "google",
      "configured": true,
      "connected": false,
      "mode": "live"
    }
  ]
}
```

Depois, conecte a conta via API ou Dashboard.

## Troubleshooting

### Erro "Developer token not approved"

- Use um token de teste para desenvolvimento
- Para produção, solicite aprovação no API Center

### Erro "Access denied"

- Verifique se você tem acesso à conta Google Ads
- Confirme que o Customer ID está correto
- Regere o Refresh Token

### Erro "Quota exceeded"

- A API tem limites diários
- Aguarde 24h ou solicite aumento de quota

## Limites da API

- **Básico (teste)**: 15.000 operações/dia
- **Padrão**: 100.000 operações/dia

Para a maioria das revendas, o limite básico é suficiente.

## Dados Sincronizados

O sistema sincroniza automaticamente:

- Campanhas (nome, status, objetivo)
- Métricas diárias por campanha:
  - Gasto
  - Impressões
  - Cliques
  - Conversões/Leads
  - CPC, CPM, CTR

A sincronização ocorre a cada hora automaticamente.

## Referências

- [Documentação oficial Google Ads API](https://developers.google.com/google-ads/api/docs/start)
- [Guia de autenticação](https://developers.google.com/google-ads/api/docs/oauth/overview)

