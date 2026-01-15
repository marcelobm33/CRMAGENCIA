# Configuração do Meta Ads (Facebook/Instagram)

Este guia explica como configurar a integração com o Meta Ads para sincronizar dados de campanhas.

## Pré-requisitos

- Conta de anúncios Meta (Facebook Ads)
- Acesso de administrador ao Business Manager
- Conta de desenvolvedor Meta

## Passo a Passo

### 1. Criar App no Meta for Developers

1. Acesse [Meta for Developers](https://developers.facebook.com/)
2. Clique em **Meus Apps** > **Criar App**
3. Selecione **Tipo: Business**
4. Preencha:
   - Nome: "CRM IA Campanhas"
   - Email de contato
   - Business Manager (selecione sua conta)
5. Clique em **Criar app**

### 2. Adicionar Marketing API

1. No dashboard do app, clique em **Adicionar produtos**
2. Encontre **Marketing API** e clique em **Configurar**
3. Siga o wizard de configuração

### 3. Obter App ID e Secret

1. Vá em **Configurações** > **Básico**
2. **Anote** o App ID
3. Clique em **Mostrar** ao lado de Chave Secreta do App
4. **Anote** o App Secret

### 4. Gerar Access Token

#### Opção A: Token de curta duração (para testes)

1. Vá em **Ferramentas** > **Graph API Explorer**
2. Selecione seu app no dropdown
3. Clique em **Gerar Token de Acesso**
4. Adicione as permissões:
   - `ads_read`
   - `ads_management`
   - `business_management`
5. **Anote** o token gerado

**Nota**: Este token expira em algumas horas.

#### Opção B: Token de longa duração (recomendado)

1. Gere um token de curta duração (Opção A)
2. Troque por um de longa duração via API:

```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=SEU_APP_ID&client_secret=SEU_APP_SECRET&fb_exchange_token=TOKEN_CURTO"
```

3. **Anote** o token retornado (dura 60 dias)

#### Opção C: Token permanente (System User)

Para produção, recomendamos usar System User:

1. No Business Manager, vá em **Configurações** > **System Users**
2. Crie um novo System User
3. Atribua acesso à conta de anúncios
4. Gere um token para este usuário

### 5. Obter Ad Account ID

1. Acesse o [Business Manager](https://business.facebook.com/)
2. Vá em **Configurações de negócios** > **Contas** > **Contas de anúncios**
3. Clique na conta desejada
4. O ID aparece no formato `act_XXXXXXXX`
5. **Anote** o ID completo (incluindo `act_`)

### 6. Configurar o Sistema

Edite o arquivo `.env`:

```env
META_APP_ID=seu_app_id
META_APP_SECRET=seu_app_secret
META_ACCESS_TOKEN=seu_access_token
META_AD_ACCOUNT_ID=act_1234567890
```

### 7. Reiniciar o Sistema

```bash
docker compose down
docker compose up -d
```

### 8. Verificar Integração

Acesse http://localhost:8000/api/integrations/status

Você deve ver:
```json
{
  "integrations": [
    {
      "platform": "meta",
      "configured": true,
      "connected": false,
      "mode": "live"
    }
  ]
}
```

## Troubleshooting

### Erro "Invalid OAuth access token"

- O token expirou, gere um novo
- Verifique se o token tem as permissões necessárias

### Erro "User does not have permission"

- Confirme que o token tem acesso à conta de anúncios
- Verifique as permissões no Business Manager

### Erro "Ad account ID is invalid"

- Confirme que o ID começa com `act_`
- Verifique se você tem acesso a esta conta

### Token expirando frequentemente

- Use System User para tokens permanentes
- Configure alerta para renovar antes de expirar

## Limites da API

- **Rate Limit**: Depende do nível do app
- **Insights**: Dados disponíveis por até 37 meses

O sistema respeita os rate limits automaticamente.

## Dados Sincronizados

O sistema sincroniza:

- Campanhas (nome, status, objetivo)
- Conjuntos de anúncios (adsets)
- Métricas diárias:
  - Gasto
  - Impressões
  - Alcance
  - Cliques
  - Leads (se configurado)
  - CPM, CPC, CTR

## Renovação de Token

Tokens de longa duração duram 60 dias. Configure um lembrete para renovar antes de expirar:

```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=SEU_APP_ID&client_secret=SEU_APP_SECRET&fb_exchange_token=TOKEN_ATUAL"
```

## Referências

- [Documentação Marketing API](https://developers.facebook.com/docs/marketing-apis)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Guia de Access Tokens](https://developers.facebook.com/docs/facebook-login/access-tokens)

