const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface FetchOptions extends RequestInit {
  token?: string;
}

export async function api<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const { token, ...fetchOptions } = options;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

// Dashboard APIs
export async function getOverview(dias: number = 30) {
  return api(`/api/analytics/overview?dias=${dias}`);
}

export async function getChannels(dias: number = 30) {
  return api(`/api/analytics/channels?dias=${dias}`);
}

export async function getVendedores(dias: number = 30) {
  return api(`/api/analytics/vendedores?dias=${dias}`);
}

export async function getFunnel(dias: number = 30) {
  return api(`/api/analytics/funnel?dias=${dias}`);
}

export async function getKPIs(dias: number = 30) {
  return api(`/api/analytics/kpis?dias=${dias}`);
}

// Campaigns APIs
export async function getCampaigns() {
  return api("/api/campaigns/");
}

export async function getCampaignSpend(campaignId: string) {
  return api(`/api/campaigns/${campaignId}/spend`);
}

export async function getPlatformsSummary(dias: number = 30) {
  return api(`/api/campaigns/platforms/summary?dias=${dias}`);
}

// CRM APIs
export async function getDeals(params: Record<string, any> = {}) {
  const query = new URLSearchParams(params).toString();
  return api(`/api/crm/deals?${query}`);
}

export async function getCRMStats() {
  return api("/api/crm/stats");
}

// AI APIs
export async function getRecommendations(status?: string) {
  const query = status ? `?status=${status}` : "";
  return api(`/api/ai/recommendations${query}`);
}

export async function updateRecommendation(id: string, data: any) {
  return api(`/api/ai/recommendations/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export async function runAnalysis(dias: number = 7) {
  return api("/api/ai/analyze", {
    method: "POST",
    body: JSON.stringify({ periodo_dias: dias }),
  });
}

export async function getAISummary() {
  return api("/api/ai/summary");
}

// Integrations APIs
export async function getIntegrationsStatus() {
  return api("/api/integrations/status");
}

// ============================================
// CRM SYNC - DADOS EM TEMPO REAL
// ============================================

// Status da conexão com CRM externo
export async function getCRMSyncStatus() {
  return api("/api/crm-sync/status");
}

// Resumo do mês em tempo real
export async function getCRMResumo() {
  return api("/api/crm-sync/realtime/resumo");
}

// Performance por vendedor em tempo real
export async function getCRMVendedores(dias: number = 30) {
  return api(`/api/crm-sync/realtime/vendedores?dias=${dias}`);
}

// Performance por origem em tempo real
export async function getCRMOrigens(dias: number = 30) {
  return api(`/api/crm-sync/realtime/origens?dias=${dias}`);
}

// Funil atual em tempo real
export async function getCRMFunil() {
  return api("/api/crm-sync/realtime/funil");
}

// Comparativo META vs GOOGLE
export async function getCRMMetaVsGoogle(dias: number = 30) {
  return api(`/api/crm-sync/realtime/meta-vs-google?dias=${dias}`);
}

// Motivos de perda
export async function getCRMMotivosPerda(dias: number = 30) {
  return api(`/api/crm-sync/realtime/motivos-perda?dias=${dias}`);
}

// Leads parados
export async function getCRMLeadsParados(dias: number = 7) {
  return api(`/api/crm-sync/realtime/leads-parados?dias=${dias}`);
}

// Preview sem sincronizar
export async function getCRMPreview(dias: number = 7) {
  return api(`/api/crm-sync/preview?dias=${dias}`);
}

// Disparar sincronização manual
export async function triggerCRMSync(dias: number = 7, fullSync: boolean = false) {
  return api(`/api/crm-sync/sync?dias=${dias}&full_sync=${fullSync}`, {
    method: "POST",
  });
}

