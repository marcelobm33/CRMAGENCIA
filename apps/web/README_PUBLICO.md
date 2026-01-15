## Publicar relatório para compartilhar (grátis)

Objetivo: disponibilizar um link público **sem expor CRM/segredos**.  
O relatório público lê apenas `public/public-report.json` (estático).

### 1) Gerar o arquivo público (no seu computador)

Pré-requisitos:
- API `roi_api` rodando em `http://localhost:8000`
- Frontend não é necessário para gerar o JSON

Comandos:

```bash
cd "apps/web"
python3 scripts/generate_public_report.py
```

Isso vai criar:
- `apps/web/public/public-report.json`

### 2) Ver localmente

Com o Next rodando, abra:
- `/publico/roi`

Exemplo:
- `http://localhost:3001/publico/roi`

### 3) Publicar grátis (opções)

#### Opção A — Vercel (mais simples)
- Crie conta grátis na Vercel
- Importe o repositório / pasta `apps/web`
- Build command: `npm run build`
- Output: padrão (Next.js)
- Depois de publicado, o link será algo como:
  - `https://SEU-PROJETO.vercel.app/publico/roi`

#### Opção B — Cloudflare Pages (grátis)
- Crie conta no Cloudflare
- Pages → Create a project
- Framework preset: Next.js
- Build command: `npm run build`
- Output directory: `.next`

### 4) Checklist de privacidade (recomendado)
- **Não publicar**: nomes de clientes, telefones, IDs do CRM, credenciais.
- O gerador atual **não exporta vendas detalhadas**, só agregados.
- Se quiser, você pode trocar o nome do branding:

```bash
PUBLIC_REPORT_BRAND="Relatório" python3 scripts/generate_public_report.py
```

