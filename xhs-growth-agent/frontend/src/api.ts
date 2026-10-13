export interface Source { title: string; url: string; verified?: boolean }
export interface Media { id: string; url: string; path: string; sha256: string; source?: string; license?: string; template?: string }
export interface Article {
  id: string; title: string; title_candidates: string[]; body: string; tags: string[];
  status: string; category: string; style: string; ai_assisted: boolean; sources: Source[];
  media: Media[]; quality: { score: number; reasons: string[]; risks: string[]; method?: string };
  version: number; created_at: string; comment_prompt?: string; mode?: string;
}
export interface Topic { id: string; title: string; category: string; score: number; reasons: string[]; sources: Source[]; status: string }
export interface Job { id: string; article_id: string; title: string; status: string; mode: string; error?: string; created_at: string; response?: unknown }
export interface AgentRun { id?: string; name?: string; agent?: string; task?: string; status: string; last_run?: string; created_at?: string; started_at?: string; detail?: unknown; result?: unknown; mode?: string }
export interface Authorization { id: string; article_id: string; version: number; content_hash: string; visibility: string; account_id: string; account_name: string; consumed: boolean }
export interface Metrics { likes: number | null; saves: number | null; comments: number | null; views: number | null; shares?: number | null; followers?: number | null }
export interface McpStatus { connected: boolean; logged_in: boolean; detail: string; tools?: string[] }
export interface Dashboard {
  counts: { articles: number; pending_review: number; approved: number; published: number; verify_required: number; topics: number };
  agents: AgentRun[]; mcp: McpStatus; model: { mode: string; configured: boolean; provider?: string; name?: string; reasoning_effort?: string; detail?: string };
  paused: boolean; daily_limit: number; recent_runs: AgentRun[]; metrics: Metrics;
  costs: { calls: number; cost_usd: number | null };
}
export interface Settings {
  daily_limit: number; quality_threshold: number; account_positioning: string; model_mode: string;
  model_configured: boolean; model_provider?: string; model_reasoning_effort?: string; model_detail?: string; mcp_url: string; paused: boolean; scheduler_enabled: boolean;
  production_target: number; keywords: string[]; rss_urls: string[]; user_id?: string; model_name?: string;
  approval_to_queue?: boolean; approved_account_id?: string; approved_account_name?: string;
}
export interface Report {
  date: string; production: unknown; approvals: unknown; published: unknown; blocked: unknown;
  insights: unknown; uncertainty: unknown; metrics: Metrics; experiments: unknown;
}

export async function api<T>(path: string, method = 'GET', body?: unknown): Promise<T> {
  const controller = new AbortController();
  const taskRequest = /^\/(creation|hotspots)(?:\/|$)/.test(path);
  const timeoutMs = taskRequest ? (method === 'GET' ? 5000 : 30000) : method === 'GET' ? path.startsWith('/mcp/status?refresh=true') ? 180000 : 60000 : path === '/publishing/pause' ? 30000 : /\/publish(?:ing\/|$)/.test(path) || /\/jobs\/.*\/verify$/.test(path) ? 900000 : /^\/(research|plan|generate|scheduler\/)|\/revise$/.test(path) ? 1800000 : 180000;
  const timeout = window.setTimeout(() => controller.abort(), timeoutMs);
  let response: Response;
  try {
    response = await fetch(`/api${path}`, {
      method,
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json' },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      if (taskRequest) throw new Error(`等待 ${timeoutMs / 1000} 秒未获得任务响应。后台任务可能仍在运行，请刷新任务进度确认。`);
      throw new Error(`请求等待超过 ${timeoutMs / 1000} 秒；请刷新内容与执行记录确认结果。系统没有自动重试，发布结果未知时请先人工核实。`);
    }
    if (taskRequest && method !== 'GET') throw new Error('未收到任务响应。请刷新任务进度确认后台状态。');
    throw new Error(method === 'GET' ? '无法连接本地后端，请确认服务已在 18760 端口启动。' : '未获得可确认的执行响应。请检查本地服务并刷新执行记录；真实发布结果未知时，勿重复提交。');
  } finally {
    window.clearTimeout(timeout);
  }
  const raw = await response.text();
  let data: unknown;
  try { data = raw ? JSON.parse(raw) : {}; } catch {
    throw new Error(`后端返回非 JSON 响应（HTTP ${response.status}），请检查本地服务。`);
  }
  if (!response.ok) {
    const detail = (data as { detail?: unknown })?.detail;
    throw new Error(typeof detail === 'string' ? detail : detail ? JSON.stringify(detail) : `请求失败（HTTP ${response.status}）`);
  }
  return data as T;
}

export function list<T>(data: unknown): T[] {
  if (Array.isArray(data)) return data as T[];
  if (data && typeof data === 'object') {
    const value = data as { items?: T[]; data?: T[] };
    return value.items ?? value.data ?? [];
  }
  return [];
}
