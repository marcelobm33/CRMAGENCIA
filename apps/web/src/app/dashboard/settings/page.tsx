"use client";

import { Header } from "@/components/layout/header";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Settings,
  Link,
  RefreshCw,
  Upload,
  Download,
  Zap,
  Database,
  XCircle,
} from "lucide-react";

// Dados mock
const integrations = [
  {
    name: "Google Ads",
    platform: "google",
    configured: false,
    connected: false,
    mode: "mock",
    lastSync: null,
  },
  {
    name: "Meta Ads",
    platform: "meta",
    configured: false,
    connected: false,
    mode: "mock",
    lastSync: null,
  },
  {
    name: "IA Analista",
    platform: "ai",
    configured: true,
    connected: true,
    mode: "mock",
    lastSync: "2024-01-20T14:30:00",
  },
];

export default function SettingsPage() {
  return (
    <>
      <Header title="Configurações" description="Gerencie integrações e sistema" />

      <div className="p-6 space-y-6">
        {/* Integrações */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Link className="h-5 w-5" />
              Integrações
            </CardTitle>
            <CardDescription>
              Conecte suas contas de anúncios para sincronizar dados automaticamente
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {integrations.map((integration) => (
              <div
                key={integration.platform}
                className="flex items-center justify-between p-4 rounded-lg border border-border"
              >
                <div className="flex items-center gap-4">
                  <div
                    className={`h-10 w-10 rounded-lg flex items-center justify-center ${
                      integration.connected
                        ? "bg-success/20"
                        : "bg-secondary"
                    }`}
                  >
                    {integration.connected ? (
                      <Link className="h-5 w-5 text-success" />
                    ) : (
                      <XCircle className="h-5 w-5 text-muted-foreground" />
                    )}
                  </div>
                  <div>
                    <p className="font-medium">{integration.name}</p>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Badge variant={integration.mode === "live" ? "success" : "secondary"}>
                        {integration.mode === "live" ? "Conectado" : "Modo Mock"}
                      </Badge>
                      {integration.lastSync && (
                        <span>Última sync: {new Date(integration.lastSync).toLocaleString("pt-BR")}</span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {integration.connected ? (
                    <>
                      <Button variant="ghost" size="sm">
                        <RefreshCw className="h-4 w-4 mr-2" />
                        Sincronizar
                      </Button>
                      <Button variant="outline" size="sm">
                        Desconectar
                      </Button>
                    </>
                  ) : (
                    <Button size="sm">
                      Conectar
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Importar/Exportar */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="h-5 w-5" />
              Dados
            </CardTitle>
            <CardDescription>
              Importe ou exporte dados do CRM
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between p-4 rounded-lg border border-border">
              <div className="flex items-center gap-4">
                <div className="h-10 w-10 rounded-lg bg-primary/20 flex items-center justify-center">
                  <Upload className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="font-medium">Importar Negócios</p>
                  <p className="text-sm text-muted-foreground">
                    Importe dados do CRM via arquivo CSV
                  </p>
                </div>
              </div>
              <Button>
                <Upload className="h-4 w-4 mr-2" />
                Importar CSV
              </Button>
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg border border-border">
              <div className="flex items-center gap-4">
                <div className="h-10 w-10 rounded-lg bg-secondary flex items-center justify-center">
                  <Download className="h-5 w-5 text-muted-foreground" />
                </div>
                <div>
                  <p className="font-medium">Exportar Dados</p>
                  <p className="text-sm text-muted-foreground">
                    Exporte todos os dados para backup
                  </p>
                </div>
              </div>
              <Button variant="outline">
                <Download className="h-4 w-4 mr-2" />
                Exportar
              </Button>
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg border border-border">
              <div className="flex items-center gap-4">
                <div className="h-10 w-10 rounded-lg bg-secondary flex items-center justify-center">
                  <Download className="h-5 w-5 text-muted-foreground" />
                </div>
                <div>
                  <p className="font-medium">Template CSV</p>
                  <p className="text-sm text-muted-foreground">
                    Baixe o modelo para importação
                  </p>
                </div>
              </div>
              <Button variant="ghost">
                <Download className="h-4 w-4 mr-2" />
                Baixar Template
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* IA */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5" />
              IA Analista
            </CardTitle>
            <CardDescription>
              Configure o comportamento da análise automática
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between p-4 rounded-lg border border-border">
              <div>
                <p className="font-medium">Modo de Operação</p>
                <p className="text-sm text-muted-foreground">
                  Mock (regras) ou OpenAI (LLM avançado)
                </p>
              </div>
              <Badge variant="secondary">Mock</Badge>
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg border border-border">
              <div>
                <p className="font-medium">Frequência de Análise</p>
                <p className="text-sm text-muted-foreground">
                  A cada 6 horas automaticamente
                </p>
              </div>
              <Badge variant="outline">6h</Badge>
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg border border-border">
              <div>
                <p className="font-medium">Executar Análise Agora</p>
                <p className="text-sm text-muted-foreground">
                  Gerar novos insights imediatamente
                </p>
              </div>
              <Button>
                <Zap className="h-4 w-4 mr-2" />
                Analisar
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Sistema */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              Sistema
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="p-4 rounded-lg bg-secondary/30">
                <p className="text-sm text-muted-foreground">Versão</p>
                <p className="font-medium">1.0.0</p>
              </div>
              <div className="p-4 rounded-lg bg-secondary/30">
                <p className="text-sm text-muted-foreground">Ambiente</p>
                <p className="font-medium">Desenvolvimento</p>
              </div>
              <div className="p-4 rounded-lg bg-secondary/30">
                <p className="text-sm text-muted-foreground">Banco de Dados</p>
                <p className="font-medium">PostgreSQL 15</p>
              </div>
              <div className="p-4 rounded-lg bg-secondary/30">
                <p className="text-sm text-muted-foreground">Workers</p>
                <p className="font-medium">Celery + Redis</p>
              </div>
            </div>

            <div className="pt-4 border-t border-border">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Documentação</p>
                  <p className="text-sm text-muted-foreground">
                    Acesse guias e referências
                  </p>
                </div>
                <Button variant="outline" asChild>
                  <a href="/docs" target="_blank">
                    Ver Docs
                  </a>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}

