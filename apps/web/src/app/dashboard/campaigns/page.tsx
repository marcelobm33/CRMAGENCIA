"use client";

import { Header } from "@/components/layout/header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatCurrency, formatNumber, formatPercent } from "@/lib/utils";
import { ArrowUpDown, ExternalLink } from "lucide-react";

// Dados mock
const mockCampaigns = [
  {
    id: "1",
    name: "Busca - Seminovos Premium",
    platform: "google",
    status: "active",
    spend: 1250.00,
    impressions: 28500,
    clicks: 1425,
    leads: 45,
    cpl: 27.78,
    deals: 28,
    vendas: 12,
    receita: 145000,
  },
  {
    id: "2",
    name: "Leads - Ofertas Especiais",
    platform: "meta",
    status: "active",
    spend: 980.00,
    impressions: 42000,
    clicks: 890,
    leads: 38,
    cpl: 25.79,
    deals: 25,
    vendas: 10,
    receita: 118000,
  },
  {
    id: "3",
    name: "Busca - Carros Usados SP",
    platform: "google",
    status: "active",
    spend: 1520.00,
    impressions: 32000,
    clicks: 1280,
    leads: 32,
    cpl: 47.50,
    deals: 18,
    vendas: 5,
    receita: 62000,
  },
  {
    id: "4",
    name: "Remarketing - Visitantes",
    platform: "meta",
    status: "active",
    spend: 650.00,
    impressions: 58000,
    clicks: 1740,
    leads: 28,
    cpl: 23.21,
    deals: 15,
    vendas: 4,
    receita: 48000,
  },
  {
    id: "5",
    name: "Display - Remarketing",
    platform: "google",
    status: "paused",
    spend: 420.00,
    impressions: 15000,
    clicks: 450,
    leads: 8,
    cpl: 52.50,
    deals: 4,
    vendas: 1,
    receita: 12000,
  },
  {
    id: "6",
    name: "Busca - Financiamento",
    platform: "google",
    status: "active",
    spend: 1331.50,
    impressions: 9920,
    clicks: 685,
    leads: 13,
    cpl: 102.42,
    deals: 0,
    vendas: 0,
    receita: 0,
  },
];

export default function CampaignsPage() {
  return (
    <>
      <Header title="Campanhas" description="Performance por campanha - Últimos 30 dias" />

      <div className="p-6 space-y-6">
        {/* Resumo */}
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-muted-foreground">Total de Campanhas</p>
              <p className="text-2xl font-bold">{mockCampaigns.length}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-muted-foreground">Campanhas Ativas</p>
              <p className="text-2xl font-bold">
                {mockCampaigns.filter((c) => c.status === "active").length}
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-muted-foreground">Gasto Total</p>
              <p className="text-2xl font-bold">
                {formatCurrency(mockCampaigns.reduce((sum, c) => sum + c.spend, 0))}
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-muted-foreground">Total de Leads</p>
              <p className="text-2xl font-bold">
                {formatNumber(mockCampaigns.reduce((sum, c) => sum + c.leads, 0))}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Tabela de campanhas */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-medium">Todas as Campanhas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">
                      <span className="flex items-center gap-1 cursor-pointer hover:text-foreground">
                        Campanha
                        <ArrowUpDown className="h-4 w-4" />
                      </span>
                    </th>
                    <th className="text-center py-3 px-4 font-medium text-muted-foreground">Plataforma</th>
                    <th className="text-center py-3 px-4 font-medium text-muted-foreground">Status</th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">Gasto</th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">Leads</th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">CPL</th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">Vendas</th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">Receita</th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">ROAS</th>
                  </tr>
                </thead>
                <tbody>
                  {mockCampaigns.map((campaign) => (
                    <tr key={campaign.id} className="border-b border-border/50 hover:bg-secondary/30">
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <span className="font-medium">{campaign.name}</span>
                          <ExternalLink className="h-3 w-3 text-muted-foreground" />
                        </div>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <Badge variant={campaign.platform === "google" ? "default" : "secondary"}>
                          {campaign.platform === "google" ? "Google" : "Meta"}
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <Badge variant={campaign.status === "active" ? "success" : "outline"}>
                          {campaign.status === "active" ? "Ativa" : "Pausada"}
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-right">{formatCurrency(campaign.spend)}</td>
                      <td className="py-3 px-4 text-right">{formatNumber(campaign.leads)}</td>
                      <td className="py-3 px-4 text-right">
                        <span
                          className={
                            campaign.cpl > 60
                              ? "text-destructive"
                              : campaign.cpl < 35
                              ? "text-success"
                              : ""
                          }
                        >
                          {formatCurrency(campaign.cpl)}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right">{formatNumber(campaign.vendas)}</td>
                      <td className="py-3 px-4 text-right">{formatCurrency(campaign.receita)}</td>
                      <td className="py-3 px-4 text-right font-medium">
                        {campaign.spend > 0 ? `${(campaign.receita / campaign.spend).toFixed(1)}x` : "-"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Insights */}
        <div className="grid gap-4 md:grid-cols-2">
          <Card className="border-success/50">
            <CardHeader className="pb-2">
              <CardTitle className="text-base font-medium text-success">Melhor Performance</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="font-medium">Remarketing - Visitantes</p>
              <p className="text-sm text-muted-foreground">
                CPL de R$ 23,21 - 40% abaixo da média
              </p>
            </CardContent>
          </Card>
          <Card className="border-destructive/50">
            <CardHeader className="pb-2">
              <CardTitle className="text-base font-medium text-destructive">Atenção Necessária</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="font-medium">Busca - Financiamento</p>
              <p className="text-sm text-muted-foreground">
                CPL de R$ 102,42 - 120% acima da média, 0 vendas
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
}

