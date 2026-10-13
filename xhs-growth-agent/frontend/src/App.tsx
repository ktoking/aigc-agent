import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react';
import {
  ArrowDown, ArrowDownLeft, ArrowRight, ArrowUp, ArrowUpRight, BarChart3, Check,
  CheckCheck, ChevronRight, CircleAlert, Clock3, Copy, ExternalLink, Eye, FileText,
  Flame, Globe, ImagePlus, Layers3, LayoutDashboard, LoaderCircle, LockKeyhole,
  Menu, NotebookPen, Pause, Play, Plus, Radio, RefreshCw, Search, Send, Settings2,
  ShieldCheck, Sparkles, SquarePen, Target, Trash2, WandSparkles, X, type LucideIcon,
} from 'lucide-react';
import { CreationDialog, CreationProgress, HotspotsPage, useCreationFlow, type CreationSeed } from './CreationFlow';
import { api, list, type AgentRun, type Article, type Dashboard, type Job, type McpStatus, type Report, type Settings, type Source } from './api';

type Page = 'dashboard' | 'topics' | 'studio' | 'review' | 'publish' | 'analytics' | 'settings';
type Notice = { text: string; kind: 'success' | 'error' | 'warning' };
const nav: { id: Page; name: string; en: string; icon: LucideIcon }[] = [
  { id: 'dashboard', name: '工作台', en: 'Dashboard', icon: LayoutDashboard },
  { id: 'topics', name: '选题雷达', en: 'Topic Radar', icon: Radio },
  { id: 'studio', name: '内容工坊', en: 'Content Studio', icon: NotebookPen },
  { id: 'review', name: '审核中心', en: 'Review Center', icon: ShieldCheck },
  { id: 'publish', name: '发布中心', en: 'Publish Center', icon: Send },
  { id: 'analytics', name: '数据复盘', en: 'Analytics', icon: BarChart3 },
  { id: 'settings', name: '系统设置', en: 'Settings', icon: Settings2 },
];
const states: Record<string, { text: string; tone: string }> = {
  DISCOVERED: { text: '已发现', tone: 'neutral' }, PLANNED: { text: '已策划', tone: 'blue' },
  GENERATING: { text: '创作中', tone: 'blue' }, GENERATED: { text: '已生成', tone: 'blue' },
  QUALITY_REJECTED: { text: '质检退回', tone: 'red' }, PENDING_REVIEW: { text: '待审核', tone: 'amber' },
  APPROVED: { text: '审核通过', tone: 'green' }, SCHEDULED: { text: '已排期', tone: 'blue' },
  QUEUED: { text: '等待发布', tone: 'blue' }, CANCELLED: { text: '已取消', tone: 'neutral' },
  PUBLISHING: { text: '发布中', tone: 'amber' }, PUBLISHED: { text: '已发布', tone: 'green' },
  NO_SUBMISSION: { text: '已核实未提交', tone: 'amber' }, FAILED: { text: '执行失败', tone: 'red' }, VERIFY_REQUIRED: { text: '需人工核实', tone: 'red' },
  REJECTED: { text: '已拒绝', tone: 'red' }, MOCK_SUCCESS: { text: 'Mock 测试通过', tone: 'blue' },
  MOCK_PUBLISHED: { text: 'Mock 测试通过', tone: 'blue' }, SUCCEEDED: { text: '完成', tone: 'green' },
  SUCCESS: { text: '完成', tone: 'green' }, COMPLETED: { text: '完成', tone: 'green' },
  BLOCKED: { text: '外部阻塞', tone: 'amber' }, RUNNING: { text: '运行中', tone: 'blue' },
  IDLE: { text: '待命', tone: 'neutral' }, READY: { text: '就绪', tone: 'green' },
};
const agentLabels: Record<string, string> = {
  morning_research: '选题研究', editorial_planning: '主编策划', content_generation: '内容创作',
  quality_review: '质量审核', publish_approved: '已批准发布队列', metrics_collection: '指标采集', daily_review: '每日复盘',
  TopicResearchAgent: '选题研究', ChiefEditorAgent: '主编策划', ContentWriterAgent: '内容创作',
  VisualDesignerAgent: '视觉设计', QualityReviewerAgent: '质量审核', PublishingAgent: '发布管理', AnalyticsAgent: '数据复盘',
  'Topic Research': '近期热点', 'Chief Editor': '主编策划', 'Content Writer': '内容准备', 'Content Creation': '内容准备', 'Hotspot Refresh': '近期热点',
  'Visual Designer': '视觉设计', 'Quality Reviewer': '质量审核', Publishing: '发布管理', 'Analytics & Growth': '数据复盘',
};
const dateText = new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Shanghai', month: 'long', day: 'numeric', weekday: 'long' }).format(new Date());
const time = (value?: string) => value && !Number.isNaN(new Date(value).getTime()) ? new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Shanghai', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(value)) : '尚未执行';
const readable = (value: unknown): string => typeof value === 'string' ? value : Array.isArray(value) ? value.map(readable).join('\n') : value == null ? '暂无记录' : JSON.stringify(value, null, 2);
const sourceUrl = (value: string) => /^https?:\/\//i.test(value) ? value : undefined;

function Badge({ status, children, tone = 'neutral' }: { status?: string; children?: ReactNode; tone?: string }) {
  const state = status ? states[status.toUpperCase()] : undefined;
  return <span className={`badge ${state?.tone ?? tone}`}><span className="badge-dot" />{state?.text ?? children ?? status}</span>;
}
function Empty({ icon: Icon = Layers3, title, text, children }: { icon?: LucideIcon; title: string; text: string; children?: ReactNode }) {
  return <div className="empty"><div className="empty-icon"><Icon size={25} strokeWidth={1.5} /></div><h3>{title}</h3><p>{text}</p>{children}</div>;
}
function Panel({ title, kicker, aside, children, className = '' }: { title?: string; kicker?: string; aside?: ReactNode; children: ReactNode; className?: string }) {
  return <section className={`panel ${className}`}>{title && <div className="panel-heading"><div>{kicker && <span className="eyebrow">{kicker}</span>}<h2>{title}</h2></div>{aside}</div>}{children}</section>;
}
function Sources({ sources }: { sources?: Source[] }) {
  return <div className="sources">{!sources?.length ? <p className="muted">尚未记录来源。事实性内容需补充可靠依据。</p> : sources.map((source, i) => <a className="source-link" key={`${source.url}-${i}`} href={sourceUrl(source.url)} target="_blank" rel="noreferrer"><Globe size={15} /><span>{source.title || source.url}<small>{source.verified ? '来源已读取' : '待核验来源'}</small></span><ExternalLink size={14} /></a>)}</div>;
}
function Quality({ article }: { article: Article }) {
  return <div className="quality"><div className="quality-score"><span>{article.quality?.score ?? '—'}</span><small>/ 100</small><p>规则预检评分</p><small className="quality-method">{article.quality?.method ?? '非事实核验或流量预测'}</small></div><div className="quality-details">{article.quality?.reasons?.map((reason, i) => <p key={i}><Check size={14} />{reason}</p>)}{article.quality?.risks?.map((risk, i) => <p className="risk" key={`r${i}`}><CircleAlert size={14} />{risk}</p>)}{!article.quality?.reasons?.length && <p className="muted">暂无评分依据</p>}</div></div>;
}
function NotePreview({ article, compact = false }: { article: Article; compact?: boolean }) {
  return <div className={`note-preview ${compact ? 'compact' : ''}`}><div className="preview-top"><span className="avatar-small">X</span><div><strong>笔记预览</strong><small>本地预览 · {article.status === "PUBLISHED" ? "已核实发布" : states[article.status]?.text ?? "尚未发布"}</small></div><span className="follow-preview">预览</span></div>{article.media?.[0] ? <img className="preview-cover" src={article.media[0].url} alt={`${article.title}封面`} /> : <div className="preview-cover missing-image"><ImagePlus size={32} /><span>等待生成封面</span></div>}<div className="preview-content"><h3>{article.title}</h3><p>{article.body}</p><div className="preview-tags">{article.tags?.map(tag => <span key={tag}>#{tag.replace(/^#/, '')}</span>)}</div>{article.comment_prompt && <p className="comment-prompt">{article.comment_prompt}</p>}</div></div>;
}

export default function App() {
  const [page, setPage] = useState<Page>('dashboard');
  const [mobileNav, setMobileNav] = useState(false);
  const [dashboard, setDashboard] = useState<Dashboard>();
  const [articles, setArticles] = useState<Article[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [settings, setSettings] = useState<Settings>();
  const [report, setReport] = useState<Report>();
  const [mcp, setMcp] = useState<McpStatus>();
  const [runs, setRuns] = useState<AgentRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState('');
  const [pauseBusy, setPauseBusy] = useState(false);
  const [queueError, setQueueError] = useState('');
  const [errors, setErrors] = useState<string[]>([]);
  const [notice, setNotice] = useState<Notice>();
  const [selectedId, setSelectedId] = useState('');
  const [selectedReviews, setSelectedReviews] = useState<string[]>([]);
  const [filter, setFilter] = useState('');
  const [creationSeed, setCreationSeed] = useState<CreationSeed>();
  const [reviewScope, setReviewScope] = useState<'all' | 'current'>('all');
  const [edit, setEdit] = useState({ title: '', body: '', tags: '', media: [] as string[] });
  const [revision, setRevision] = useState('');
  const [coverTemplate, setCoverTemplate] = useState('minimal');
  const [qr, setQr] = useState<{ image_url?: string; detail: string }>();
  const [settingsForm, setSettingsForm] = useState({ positioning: '', keywords: '', rss: '', dailyLimit: 3, target: 50, threshold: 80, scheduler: false, modelMode: 'live', mcpUrl: '' });


  const refresh = useCallback(async (localOnly = false) => {
    const endpoints = ['/dashboard', '/articles', '/hotspots', '/jobs', '/settings', '/report', '/mcp/status', '/runs'];
    const foundErrors: string[] = [];
    await Promise.allSettled(endpoints.map(async (path, index) => {
      if (index === 2 || (localOnly && [0, 5, 6, 7].includes(index))) return;
      try {
        const value = await api<unknown>(path);
      switch (index) {
        case 0: setDashboard(value as Dashboard); break;
        case 1: {
          const currentArticles = list<Article>(value);
          setArticles(currentArticles);
          if (localOnly) setDashboard(current => current ? { ...current, counts: { ...current.counts, articles: currentArticles.length, approved: currentArticles.filter(article => article.status === 'APPROVED').length, published: currentArticles.filter(article => article.status === 'PUBLISHED').length, pending_review: currentArticles.filter(article => ['PENDING_REVIEW', 'QUALITY_REJECTED'].includes(article.status)).length, verify_required: currentArticles.filter(article => article.status === 'VERIFY_REQUIRED').length } } : current);
          break;
        }
        case 2: break;
        case 3: setJobs(list<Job>(value)); break;
        case 4: setSettings(value as Settings); break;
        case 5: setReport(value as Report); break;
        case 6: setMcp(value as McpStatus); break;
        case 7: setRuns(list<AgentRun>(value)); break;
      }
        // Render as each local response arrives; platform diagnostics never block navigation.
        if ([0, 1, 4].includes(index)) setLoading(false);
      } catch (error) {
        foundErrors.push(`${path}：${error instanceof Error ? error.message : '读取失败'}`);
      }
    }));
    setErrors(foundErrors);
    setLoading(false);
  }, []);
  useEffect(() => { void refresh(); }, [refresh]);
  useEffect(() => {
    if (page !== 'publish') return;
    let active = true;
    let fetching = false;
    const refreshQueue = async () => {
      if (fetching) return;
      fetching = true;
      try {
        const results = await Promise.allSettled([api<unknown>('/jobs'), api<unknown>('/articles'), api<Settings>('/settings')]);
        if (!active) return;
        const [jobResult, articleResult, settingResult] = results;
        if (jobResult.status === 'fulfilled') { setJobs(list<Job>(jobResult.value)); setQueueError(''); }
        else setQueueError(jobResult.reason instanceof Error ? jobResult.reason.message : '读取失败');
        if (articleResult.status === 'fulfilled') {
          const currentArticles = list<Article>(articleResult.value);
          setArticles(currentArticles);
          setDashboard(current => current ? { ...current, counts: { ...current.counts, articles: currentArticles.length, approved: currentArticles.filter(article => article.status === 'APPROVED').length, published: currentArticles.filter(article => article.status === 'PUBLISHED').length, pending_review: currentArticles.filter(article => ['PENDING_REVIEW', 'QUALITY_REJECTED'].includes(article.status)).length, verify_required: currentArticles.filter(article => article.status === 'VERIFY_REQUIRED').length } } : current);
        }
        if (settingResult.status === 'fulfilled') setSettings(settingResult.value);
      } finally { fetching = false; }
    };
    const timer = window.setInterval(() => void refreshQueue(), 10000);
    return () => { active = false; window.clearInterval(timer); };
  }, [page]);
  useEffect(() => { if (!selectedId && articles.length) setSelectedId(articles[0].id); }, [articles, selectedId]);
  const selected = articles.find(article => article.id === selectedId);
  useEffect(() => {
    if (selected) setEdit({ title: selected.title, body: selected.body, tags: selected.tags?.join('、') ?? '', media: selected.media?.map(media => media.id) ?? [] });
  }, [selected?.id, selected?.version]);
  useEffect(() => {
    if (settings) setSettingsForm({ positioning: settings.account_positioning, keywords: settings.keywords?.join('、') ?? '', rss: settings.rss_urls?.join('\n') ?? '', dailyLimit: settings.daily_limit, target: settings.production_target, threshold: settings.quality_threshold, scheduler: settings.scheduler_enabled, modelMode: settings.model_mode, mcpUrl: settings.mcp_url });
  }, [settings]);
  useEffect(() => { if (notice && notice.kind !== 'error') { const timer = setTimeout(() => setNotice(undefined), 8000); return () => clearTimeout(timer); } }, [notice]);
  const act = async <T,>(label: string, fn: () => Promise<T>, success: string | ((result: T) => string)): Promise<T | undefined> => {
    if (busy) return;
    setBusy(label); setNotice(undefined);
    try {
      const result = await fn();
      const rawBlocked = (result as { blocked?: unknown; error?: string; status?: string })?.blocked;
      const blocked = Array.isArray(rawBlocked) ? rawBlocked.length > 0 ? rawBlocked : undefined : rawBlocked;
      const failed = (result as { status?: string })?.status;
      setNotice({ kind: blocked || failed === 'VERIFY_REQUIRED' || failed === 'FAILED' ? 'warning' : 'success', text: blocked ? `操作记录已保存；外部阻塞：${readable(blocked)}` : failed === 'VERIFY_REQUIRED' ? '发布结果尚未确认，已暂停后续提交。请到平台人工核实，勿重复发布。' : failed === 'FAILED' ? `执行失败：${(result as { error?: string }).error ?? '请查看发布记录'}` : typeof success === 'function' ? success(result) : success });
      await refresh(true);
      return result;
    } catch (error) {
      setNotice({ kind: 'error', text: error instanceof Error ? error.message : String(error) });
      return undefined;
    } finally { setBusy(''); }
  };
  const go = (next: Page) => { setPage(next); setMobileNav(false); setFilter(''); window.scrollTo({ top: 0 }); };
  const creation = useCreationFlow(async task => {
    const currentArticles = list<Article>(await api('/articles'));
    setArticles(currentArticles);
    setSelectedReviews(current => current.filter(id => currentArticles.some(article => article.id === id && article.status === 'PENDING_REVIEW')));
    setDashboard(current => current ? { ...current, counts: { ...current.counts, articles: currentArticles.length, pending_review: currentArticles.filter(article => ['PENDING_REVIEW', 'QUALITY_REJECTED'].includes(article.status)).length } } : current);
  });
  const openCreation = (seed: CreationSeed = {}) => { setCreationSeed(seed); setNotice(undefined); };
  const showCurrentCreation = () => { setReviewScope('current'); setSelectedReviews([]); go('review'); };
  const creationProgress = () => <CreationProgress task={creation.task} error={creation.error} onRetry={() => { void creation.retryRead(); }} onShow={showCurrentCreation} />;

  const paused = settings?.paused ?? dashboard?.paused ?? true;
  const approvalToQueue = settings?.approval_to_queue === true;
  const setPublishingPause = async (next: boolean) => {
    if (pauseBusy) return;
    setPauseBusy(true);
    try {
      await api('/publishing/pause', 'POST', { paused: next });
      setDashboard(current => current ? { ...current, paused: next } : current);
      setSettings(current => current ? { ...current, paused: next } : current);
      setNotice({ kind: 'success', text: next ? '已阻止后续发布请求。已经提交到平台的请求可能无法撤回，请查看执行记录。' : '发布队列已恢复。按已启用的审批入队策略执行，平台结果将在发布中心记录。' });
    } catch (error) {
      setNotice({ kind: 'error', text: error instanceof Error ? error.message : String(error) });
    } finally { setPauseBusy(false); }
  };
  const pending = articles.filter(article => ['PENDING_REVIEW', 'QUALITY_REJECTED'].includes(article.status));
  const approved = articles.filter(article => article.status === 'APPROVED');
  const currentNav = nav.find(item => item.id === page)!;
  const split = (value: string) => value.split(/[、，,\n]/).map(item => item.trim().replace(/^#/, '')).filter(Boolean);
  const save = () => selected && act('保存内容', () => api<Article>(`/articles/${selected.id}`, 'PATCH', { title: edit.title, body: edit.body, tags: split(edit.tags), media_order: edit.media }), '已保存新版本；原审批与发布授权已失效。');
  const review = (article: Article, decision: 'approve' | 'reject') => act(decision === 'approve' ? (approvalToQueue ? '批准并入队' : '审核通过') : '过滤内容', () => api<Article>(`/articles/${article.id}/review`, 'POST', { decision, reviewer: '本地人工审核' }), decision === 'approve' ? approvalToQueue ? '已批准并加入发布队列，后台将处理当前版本。' : '内容已审核通过；自动入队策略尚未开启，可到发布中心启用。' : '已过滤，移出待审核列表；仍可在内容工坊修改。');
  const runTask = (task: string) => act(agentLabels[task] ?? task, () => api(`/scheduler/${task}/run`, 'POST'), '任务已执行，结果已写入运行记录。');
  const enqueueApproved = () => act('加入发布队列', () => api<{ count: number }>('/publishing/enqueue-approved', 'POST', {}), result => result.count > 0 ? `${result.count} 篇已批准内容加入发布队列，后台将串行处理；请查看执行记录。` : '没有新增队列任务；内容可能已入队或不满足当前发布条件，请查看执行记录。');
  const updateQueuePolicy = (enabled: boolean) => act(enabled ? '核实账号并开启审批入队' : '关闭审批入队策略', () => api<Settings>('/settings', 'PATCH', { approval_to_queue: enabled }), enabled ? '策略已启用。审核批准即允许此版本发布到绑定账号，后台按队列与配额执行。' : '审批自动入队已关闭；已暂停发布并取消未提交的自动任务。已经提交到平台的请求可能无法撤回。');
  const orderedMedia = useMemo(() => edit.media.map(id => selected?.media?.find(item => item.id === id)).filter((media): media is NonNullable<typeof media> => !!media), [edit.media, selected]);
  const previewArticle = selected ? { ...selected, title: edit.title, body: edit.body, tags: split(edit.tags), media: orderedMedia } : undefined;
  const moveMedia = (index: number, direction: number) => {
    const next = [...edit.media];
    if (index + direction < 0 || index + direction >= next.length) return;
    [next[index], next[index + direction]] = [next[index + direction], next[index]];
    setEdit({ ...edit, media: next });
  };

  function dashboardPage() {
    const counts = dashboard?.counts;
    return <>
      <section className="welcome"><div className="welcome-copy"><span className="eyebrow">YOUR CREATIVE OPERATING SYSTEM</span><h1>好内容，从一个<br />值得说的想法开始<span>。</span></h1><p>先说你想写什么，系统准备文案与配图。<br />你来筛选和修改，批准后自动排队发布。</p><div className="button-row"><button className="button primary" onClick={() => openCreation()}><Plus size={17} />准备内容</button><button className="button subtle" onClick={() => go('studio')}>进入内容工坊<ArrowUpRight size={17} /></button></div></div><div className="welcome-art" aria-hidden="true"><div className="art-orbit" /><div className="art-note rear"><span>01 / RESEARCH</span><Radio size={34} /><div className="art-line" /><div className="art-line short" /></div><div className="art-note front"><span className="art-number">Aa<span>✳</span></span><div><small>MAKE SOMETHING</small><strong>worth reading.</strong></div><span className="art-footer">XHS GROWTH STUDIO <ArrowUpRight size={15} /></span></div><div className="art-sticker"><Sparkles size={16} /> HUMAN IN THE LOOP</div></div></section>
      {creationProgress()}
      <div className="metrics-grid">{[{ label: '本地笔记总数', value: counts?.articles, icon: FileText, detail: '内容生产库', color: 'orange' }, { label: '等待人工审核', value: counts?.pending_review, icon: ShieldCheck, detail: '质量通过后由你确认', color: 'amber' }, { label: '真实已发布', value: counts?.published, icon: Send, detail: '不包含 Mock 测试', color: 'green' }, { label: '已审核通过', value: counts?.approved, icon: CheckCheck, detail: '进入发布队列', color: 'blue' }].map(item => <div className="metric-card" key={item.label}><div className="metric-top"><span>{item.label}</span><item.icon size={18} className={item.color} /></div><strong>{item.value ?? '—'}<span>篇</span></strong><small>{item.detail}</small></div>)}</div>
      <div className="dashboard-grid"><Panel title="从灵感到发布" kicker="CONTENT PIPELINE" aside={<button className="text-button" onClick={() => go('review')}>查看内容<ArrowRight size={14} /></button>}><div className="pipeline">{[{ label: '内容方向', icon: Radio, value: '自定' }, { label: '完成创作', icon: SquarePen, value: counts?.articles }, { label: '审核通过', icon: ShieldCheck, value: counts?.approved }, { label: '真实发布', icon: Send, value: counts?.published }].map((step, i) => <div className="pipeline-step" key={step.label}><div className={`pipeline-icon step-${i}`}><step.icon size={21} /></div><span>{step.label}</span><strong>{step.value ?? '—'}</strong>{i < 3 && <ChevronRight className="pipeline-arrow" size={17} />}</div>)}</div><div className="inline-note"><LockKeyhole size={15} /><span>{approvalToQueue ? '审批入队策略已启用：批准当前版本后，后台自动排队发布。' : '自动入队策略尚未启用，内容审批与真实发布分别记录。'}</span></div></Panel><Panel title="运行环境" kicker="CONNECTIONS"><div className="connection-row"><div className={`connection-icon ${mcp?.logged_in ? 'green' : ''}`}><Globe size={20} /></div><div><strong>小红书 MCP</strong><small>{mcp?.logged_in ? '账号已登录' : mcp?.connected ? '服务已连接 · 等待扫码登录' : '等待连接本地服务'}</small></div><span className={`status-light ${mcp?.logged_in ? 'online' : ''}`} /></div><div className="connection-row"><div className="connection-icon"><Sparkles size={20} /></div><div><strong>内容创作模型</strong><small>{dashboard?.model?.configured ? 'gpt-6.1-sol · high · CLI 已安装' : 'Codex CLI 尚未找到'}</small></div><Badge tone={dashboard?.model?.configured ? 'green' : 'amber'}>{dashboard?.model?.configured ? 'CLI 已安装' : '待连接'}</Badge></div><button className="button outline full" onClick={() => go('settings')}>连接与配置<ArrowUpRight size={15} /></button></Panel></div>
      <div className="dashboard-grid"><Panel title="最近的内容" kicker="ON YOUR DESK" aside={<button className="text-button" onClick={() => go('studio')}>全部内容<ArrowRight size={14} /></button>}>{articles.length ? <div className="article-list">{articles.slice(0, 4).map(article => <button className="article-row" key={article.id} onClick={() => { setSelectedId(article.id); go('studio'); }}><div className="tiny-cover">{article.media?.[0] ? <img src={article.media[0].url} alt="" /> : <FileText size={20} />}</div><div><strong>{article.title}</strong><small>{article.category} · {time(article.created_at)}</small></div><Badge status={article.status} /><ChevronRight size={16} /></button>)}</div> : <Empty icon={NotebookPen} title="你的创作桌，准备好了" text="说一个内容方向，或从近期热点选一个话题。" />}</Panel><Panel title="任务进度" kicker="RECENT TASKS">{dashboard?.agents?.length ? <div className="agent-list">{dashboard.agents.filter(agent => ['Topic Research', 'Content Writer', 'Publishing', 'Analytics & Growth'].includes(agent.name ?? '')).map((agent, i) => <div className="agent-row" key={`${agent.name}-${i}`}><div className="agent-number">{String(i + 1).padStart(2, '0')}</div><div><strong>{agentLabels[agent.name ?? ''] ?? agent.name ?? agent.task}</strong><small>{time(agent.last_run)}</small></div><Badge status={agent.status} /></div>)}</div> : <Empty icon={Sparkles} title="等待 Agent 运行记录" text="实际执行研究或创作后，状态将在这里更新。" />}</Panel></div>
    </>;
  }

  function topicsPage() { return <HotspotsPage onCreate={openCreation} />; }

  function studioPage() {
    return <><PageHeading kicker="CONTENT STUDIO" title="把一个想法，写得具体。" text="标题、文案与图文在同一个地方打磨，保存后自动创建新版本。" /><div className="toolbar panel"><span className="muted">从你的方向开始，完成后到审核中心筛选。</span><button className="button primary" onClick={() => openCreation()}><Plus size={16} />准备新内容</button></div>{creationProgress()}{!articles.length ? <Panel><Empty icon={NotebookPen} title="第一篇内容，从这里开始" text="先写一个方向，生活、旅行、美食、职场都可以。" /></Panel> : <div className="studio-layout"><aside className="studio-picker panel"><div className="small-heading">本地草稿 <span>{articles.length}</span></div>{articles.map(article => <button key={article.id} className={`draft-item ${selectedId === article.id ? 'selected' : ''}`} onClick={() => setSelectedId(article.id)}><strong>{article.title}</strong><div><Badge status={article.status} /><small>{article.mode === 'mock' ? 'Mock · ' : ''}v{article.version}</small></div></button>)}</aside>{selected && <><div className="studio-editor"><Panel title="文案编辑" aside={<div className="button-row"><span className="muted">v{selected.version}</span><button className="button primary small" disabled={!!busy} onClick={save}><Check size={14} />保存新版本</button></div>}><div className="editor-fields"><label className="field">最终标题<span className={`field-counter ${edit.title.length > 20 ? 'red' : ''}`}>{edit.title.length} / 20 字</span><input value={edit.title} onChange={e => setEdit({ ...edit, title: e.target.value })} /></label><div className="candidate-titles"><span>候选标题</span>{selected.title_candidates?.map(title => <button key={title} className={edit.title === title ? 'chosen' : ''} onClick={() => setEdit({ ...edit, title })}><Copy size={13} />{title}</button>)}</div><label className="field">正文<span className={`field-counter ${edit.body.length > 1000 ? 'red' : ''}`}>{edit.body.length} / 1000 字</span><textarea className="body-editor" value={edit.body} onChange={e => setEdit({ ...edit, body: e.target.value })} /></label><label className="field">话题标签<input value={edit.tags} onChange={e => setEdit({ ...edit, tags: e.target.value })} placeholder="用顿号或逗号分隔" /></label><div className="inline-note"><LockKeyhole size={14} />任何文案或图片调整，都会使原审批和发布授权失效。</div></div></Panel><Panel title="封面与配图" kicker="VISUAL STORY"><div className="cover-controls"><select value={coverTemplate} onChange={e => setCoverTemplate(e.target.value)}><option value="minimal">极简高级感</option><option value="magazine">杂志封面型</option><option value="technology">数码科技型</option><option value="guide">攻略信息卡</option><option value="comparison">对比测评型</option><option value="data">数据图表型</option><option value="travel">旅行摄影型</option><option value="opinion">热点观点型</option><option value="lifestyle">生活方式型</option></select><button className="button outline small" disabled={!!busy} onClick={() => act('重新生成封面', () => api(`/articles/${selected.id}/cover`, 'POST', { template: coverTemplate }), '封面已重新生成，请重新审核图片与内容。')}><ImagePlus size={15} />仅重生成封面</button></div><div className="media-grid">{orderedMedia.map((media, i) => <div className="media-item" key={media.id}><img src={media.url} alt={`第 ${i + 1} 张配图`} /><div className="media-order"><span>{i === 0 ? '封面' : `配图 ${i}`}</span><button className="icon-button" disabled={i === 0} onClick={() => moveMedia(i, -1)} title="前移图片"><ArrowUp size={14} /></button><button className="icon-button" disabled={i === orderedMedia.length - 1} onClick={() => moveMedia(i, 1)} title="后移图片"><ArrowDown size={14} /></button></div><span className="media-license" title={`${media.source ?? '来源待记录'} · ${media.license ?? '版权待记录'}`}>{media.source ?? '本地图片'}</span><span className="hash" title={media.sha256}>SHA256 · {media.sha256?.slice(0, 10)}</span></div>)}</div>{!orderedMedia.length && <p className="muted">暂无图片，请生成封面。</p>}<small className="muted">第一张为封面。调整排序后点击“保存新版本”。</small></Panel><Panel title="请 Agent 帮你修改" kicker="EDITORIAL FEEDBACK"><textarea className="revision-input" value={revision} onChange={e => setRevision(e.target.value)} placeholder="例如：开头更直接，补充一个具体操作步骤，保留来源链接。" /><div className="panel-action"><small className="muted">{settings?.model_configured ? '本机 Codex CLI · gpt-6.1-sol · high' : 'CLI 未安装或认证失败时会明确返回限制'}</small><button className="button outline small" disabled={!!busy || !revision.trim()} onClick={() => act('Agent 修改内容', () => api(`/articles/${selected.id}/revise`, 'POST', { instruction: revision }), '修改已执行，新的内容版本等待审核。')}><Sparkles size={15} />提出修改</button></div></Panel><Panel title="质量与来源" kicker="EVIDENCE FIRST"><Quality article={selected} /><Sources sources={selected.sources} /></Panel></div><aside className="preview-column"><div className="preview-label"><Eye size={15} />手机效果预览<Badge tone="neutral">本地</Badge></div>{previewArticle && <NotePreview article={previewArticle} />}</aside></>}</div>}</>;
  }

  function reviewPage() {
    const rows = pending.filter(article => (reviewScope === 'all' || creation.task?.article_ids?.includes(article.id)) && (!filter || article.title.includes(filter)));
    const approvableIds = rows.filter(article => article.status === 'PENDING_REVIEW').map(article => article.id);
    const checkedIds = selectedReviews.filter(id => approvableIds.includes(id));
    return <><PageHeading kicker="REVIEW CENTER" title="最后一眼，由你把关。" text="新稿和质检退回都在这里。保留喜欢的，修改需要调整的，过滤不合适的。" />{creationProgress()}<div className="review-summary"><div><ShieldCheck size={22} /><span><strong>{rows.length}</strong> 篇等待审核</span></div><p>{approvalToQueue ? '批准并入队：将当前版本发布到绑定账号，后台按配额串行处理。' : '当前仅审核内容。请在设置开启审批自动入队后使用发布队列。'}</p></div><div className="section-toolbar"><label className="select-all"><input type="checkbox" checked={approvableIds.length > 0 && approvableIds.every(id => selectedReviews.includes(id))} onChange={e => setSelectedReviews(e.target.checked ? approvableIds : [])} />选择可通过的稿件</label><div className="segmented"><button className={reviewScope === "all" ? "active" : ""} onClick={() => { setReviewScope("all"); setSelectedReviews([]); }}>全部待审</button><button disabled={!creation.task} className={reviewScope === "current" ? "active" : ""} onClick={() => { setReviewScope("current"); setSelectedReviews([]); }}>本次创作</button></div><div className="button-row"><label className="search"><Search size={16} /><input value={filter} onChange={e => setFilter(e.target.value)} placeholder="搜索待审内容" /></label><button className="button primary" disabled={!!busy || !checkedIds.length} onClick={() => act(approvalToQueue ? '批量批准并入队' : '批量审核通过', async () => { let approvedCount = 0; try { for (const id of checkedIds) { await api(`/articles/${id}/review`, 'POST', { decision: 'approve', reviewer: '本地人工批量审核' }); approvedCount += 1; } } finally { setSelectedReviews([]); await refresh(true); } return { count: approvedCount }; }, approvalToQueue ? '所选内容已批准并加入队列，后台将处理真实内容；Mock 示例不会公开发布。' : '所选内容已审核通过；自动入队策略尚未开启。')}><CheckCheck size={16} />{approvalToQueue ? '批准选中并入队' : '批准选中'} {checkedIds.length ? `(${checkedIds.length})` : ''}</button></div></div>{rows.length ? <div className="review-grid">{rows.map(article => <div className="review-card panel" key={article.id}><div className="review-card-top">{article.mode === 'mock' && <Badge tone="blue">Mock 示例</Badge>}<label><input type="checkbox" disabled={article.status !== "PENDING_REVIEW"} checked={selectedReviews.includes(article.id)} onChange={e => setSelectedReviews(e.target.checked ? [...selectedReviews, article.id] : selectedReviews.filter(id => id !== article.id))} />v{article.version}</label><Badge status={article.status} /></div><NotePreview article={article} compact /><div className="review-evidence"><Quality article={article} /><details className="source-details"><summary><Globe size={14} />核对引用来源<ChevronRight size={14} /></summary><Sources sources={article.sources} /></details></div><div className="review-card-actions"><button className="button subtle small" onClick={() => { setSelectedId(article.id); go('studio'); }}><SquarePen size={14} />编辑</button><button className="button outline small" disabled={!!busy} onClick={() => review(article, 'reject')}><X size={14} />过滤</button><button className="button green-button small" disabled={!!busy || article.status !== "PENDING_REVIEW"} onClick={() => review(article, 'approve')}><Check size={14} />{article.mode === 'mock' ? '通过（Mock）' : approvalToQueue ? '批准并入队' : '通过'}</button></div></div>)}</div> : <Panel><Empty icon={ShieldCheck} title="审核桌上，暂时没有待办" text={creation.running ? "内容正在后台准备，完成后自动显示；你可以继续浏览。" : reviewScope === "current" ? "本次没有待审核稿，已通过或过滤的稿件可在内容工坊查看。" : "先输入方向准备内容，新稿会自动来到这里。"} ><button className="button outline" onClick={() => go('studio')}>去内容工坊<ArrowRight size={15} /></button></Empty></Panel>}</>;
  }

  function publishPage() {
    const realApproved = approved.filter(article => article.mode !== 'mock');
    const queueCount = jobs.filter(job => job.mode === 'live' && ['QUEUED', 'SCHEDULED', 'PUBLISHING'].includes(job.status)).length;
    return <>
      <PageHeading kicker="PUBLISH CENTER" title="批准之后，交给发布队列。" text="审核确认一次，后台串行执行。账号绑定、配额和停止开关持续生效。" />
      <div className={`publish-status ${paused ? 'is-paused' : ''}`}>
        <div><div className="pause-or-play">{paused ? <Pause size={22} /> : <Play size={22} />}</div><span><strong>{paused ? '全部发布已暂停' : '发布队列已开启'}</strong><small>每日真实发布上限 {dashboard?.daily_limit ?? settings?.daily_limit ?? '—'} 篇 · 当前待执行 {queueCount} 篇 · 串行执行</small></span></div>
        <button className={`button ${paused ? 'outline' : 'danger'}`} disabled={pauseBusy || !settings} onClick={() => void setPublishingPause(!paused)}>{paused ? <Play size={16} /> : <Pause size={16} />}{paused ? '继续发布队列' : '停止全部发布'}</button>
      </div>
      <div className="queue-policy-card"><div className="queue-policy-icon"><ShieldCheck size={22} /></div><div><strong>{approvalToQueue ? '审批通过自动入队 · 已启用' : '审批通过自动入队 · 未启用'}</strong><p>{approvalToQueue ? `批准的真实内容将按当前版本与图片哈希，发布到 ${settings?.approved_account_name || '已绑定账号'}。无需再次逐篇审阅或输入确认字符串。` : '自动发布策略尚未启用。先在系统设置核实并绑定当前登录账号，再使用审批入队流程。'}</p>{settings?.approved_account_id && <small>绑定账号 ID：{settings.approved_account_id}</small>}</div><button className="text-button" onClick={() => go('settings')}>管理策略<ArrowRight size={14} /></button></div>
      <div className="publish-notice"><LockKeyhole size={16} /><span>修改内容会撤销旧版本审批与队列授权。停止开关阻止后续请求；已提交到平台的任务可能无法撤回。Mock 示例不会公开发布。</span></div>
      <Panel title="已批准的本地内容" kicker="APPROVED CONTENT" aside={<div className="button-row"><Badge tone="green">{approved.length} 篇</Badge><button className="button primary small" disabled={!!busy || !approvalToQueue || !mcp?.logged_in || !realApproved.length} onClick={enqueueApproved}><Send size={14} />{paused ? '加入发布队列' : '发布已批准内容'}</button></div>}>
        {approved.length ? <div className="publish-list">{approved.map(article => <div className="publish-row" key={article.id}><div className="publish-thumb">{article.media?.[0] ? <img src={article.media[0].url} alt="封面" /> : <FileText size={25} />}</div><div className="publish-note"><strong>{article.title}</strong><span>v{article.version} · {article.media?.length ?? 0} 张图片 · 规则预检 {article.quality?.score ?? '—'}</span><small>{article.id}</small></div><div className="publish-buttons"><button className="button subtle small" onClick={() => { setSelectedId(article.id); go('studio'); }}><Eye size={14} />查看内容</button><button className="button outline small" disabled={!!busy} onClick={() => act('Mock 发布测试', () => api(`/articles/${article.id}/publish`, 'POST', { mode: 'mock' }), 'Mock 发布流程测试已记录，没有向小红书公开发布。')}><Flame size={14} />Mock 测试</button></div></div>)}</div> : <Empty icon={Send} title="已批准内容，会自动出发" text="审批入队策略启用后，批准的真实笔记自动进入后台队列；可在下方查看执行结果。" />}
      </Panel>
      {!mcp?.logged_in && <div className="mode-notice"><Globe size={15} />真实发布尚未就绪：{mcp?.connected ? '请前往系统设置获取二维码并登录小红书。' : '请启动本地 MCP 服务，并完成账号登录。'}<button className="text-button" onClick={() => go('settings')}>查看连接<ArrowRight size={14} /></button></div>}
      {queueError && <div className="mode-notice"><CircleAlert size={15} />队列状态暂时无法刷新：{queueError}</div>}
      <Panel title="发布执行记录" kicker="DELIVERY LOG" aside={<span className="queue-poll-label"><span className="status-light online" />每 10 秒刷新本地队列</span>}>
        {jobs.length ? <div className="table-scroll"><table><thead><tr><th>内容</th><th>执行类型</th><th>结果</th><th>提交时间</th><th>详细记录</th></tr></thead><tbody>{jobs.map(job => <tr key={job.id}><td><strong>{job.title || articles.find(article => article.id === job.article_id)?.title || job.article_id}</strong><small className="table-sub">{job.id}</small></td><td><Badge tone={job.mode === 'mock' ? 'blue' : 'amber'}>{job.mode === 'mock' ? 'Mock 测试' : '真实平台'}</Badge></td><td><Badge status={job.status} />{job.status === 'VERIFY_REQUIRED' && job.mode === 'live' && <button className="text-button verify-button" disabled={!!busy} onClick={() => act('重新核实发布结果', () => api(`/jobs/${job.id}/verify`, 'POST'), '已重新核实发布结果；请查看执行记录。全局暂停需手动恢复。')}><RefreshCw size={12} />只读重新核实</button>}</td><td>{time(job.created_at)}</td><td><details className="job-detail"><summary>查看记录</summary><pre>{job.error ? `错误：${job.error}\n` : ''}{readable(job.response)}</pre></details></td></tr>)}</tbody></table></div> : <Empty icon={Clock3} title="每次提交，都有记录" text="Mock 测试与真实发布分别记录。未知结果暂停队列，先只读核实，不会自动重发。" />}
      </Panel>
    </>;
  }

  function analyticsPage() {
    const metrics = report?.metrics ?? dashboard?.metrics;
    return <><PageHeading kicker="ANALYTICS & GROWTH" title="用真实反馈，写下一篇。" text="保留来源与不确定性，样本不足时不急于解释增长。" aside={<button className="button outline" disabled={!!busy} onClick={() => act('采集真实互动指标', () => api('/metrics/collect', 'POST'), '指标采集已执行，结果与来源限制已记录。')}><RefreshCw size={16} />采集可用指标</button>} /><div className="metrics-grid">{[{ label: '点赞', value: metrics?.likes }, { label: '收藏', value: metrics?.saves }, { label: '评论', value: metrics?.comments }, { label: '浏览 / 曝光', value: metrics?.views }].map(item => <div className="metric-card" key={item.label}><div className="metric-top"><span>{item.label}</span><ArrowUpRight size={16} /></div><strong>{item.value == null ? '—' : item.value.toLocaleString()}</strong><small>{item.value == null ? '暂不可用 · 未取得真实数据' : '已采集的真实平台指标'}</small></div>)}</div><div className="dashboard-grid"><Panel title="今日运营记录" kicker={report?.date ?? 'DAILY REPORT'} aside={<button className="text-button" disabled={!!busy} onClick={() => runTask('daily_review')}>生成复盘<ArrowRight size={14} /></button>}><div className="report-facts"><ReportItem title="内容产出" value={report?.production} /><ReportItem title="审核情况" value={report?.approvals} /><ReportItem title="真实发布" value={report?.published} /><ReportItem title="阻塞与缺口" value={report?.blocked} /></div></Panel><Panel title="把不确定，也留下来" kicker="WHAT WE ACTUALLY KNOW"><div className="uncertainty-card"><CircleAlert size={23} /><div><h3>尚未积累足够的运营样本</h3><p>优先验证发布状态与可获取的互动数据。浏览、曝光、粉丝变化只有获得真实来源后才展示。</p></div></div><div className="report-text">{readable(report?.uncertainty)}</div></Panel></div><div className="dashboard-grid"><Panel title="编辑观察" kicker="EDITORIAL INSIGHTS"><div className="report-text">{readable(report?.insights)}</div></Panel><Panel title="策略实验记录" kicker="CONTROLLED EXPERIMENTS"><div className="report-text">{readable(report?.experiments)}</div><p className="footnote">实验需保留旧策略、新策略与依据。暂不根据少量短期波动判断成功。</p></Panel></div><Panel title="Agent 运行记录" kicker="ACTIVITY TRAIL">{runs.length ? <div className="table-scroll"><table><thead><tr><th>任务</th><th>状态</th><th>模式</th><th>执行时间</th><th>记录</th></tr></thead><tbody>{runs.slice(0, 30).map((run, i) => <tr key={run.id ?? i}><td><strong>{agentLabels[run.name ?? run.task ?? run.agent ?? ''] ?? run.name ?? run.task ?? run.agent}</strong></td><td><Badge status={run.status} /></td><td>{run.mode ?? '—'}</td><td>{time(run.created_at ?? run.started_at ?? run.last_run)}</td><td><details className="job-detail"><summary>查看</summary><pre>{readable(run.detail ?? run.result)}</pre></details></td></tr>)}</tbody></table></div> : <Empty icon={BarChart3} title="数据从真实运行中来" text="完成研究、创作或发布测试后，可以在这里查看执行记录。" />}</Panel></>;
  }

  function settingsPage() {
    const updateSettings = () => act('保存系统配置', () => api('/settings', 'PATCH', { account_positioning: settingsForm.positioning, keywords: split(settingsForm.keywords), rss_urls: settingsForm.rss.split('\n').map(value => value.trim()).filter(Boolean), daily_limit: settingsForm.dailyLimit, production_target: settingsForm.target, quality_threshold: settingsForm.threshold, scheduler_enabled: settingsForm.scheduler, model_mode: settingsForm.modelMode, mcp_url: settingsForm.mcpUrl }), '设置已保存。');
    return <><PageHeading kicker="SETTINGS" title="为你的工作方式，留好空间。" text="连接账号与模型，定义内容定位、质量阈值和发布边界。" aside={<button className="button primary" disabled={!!busy || !settings} onClick={updateSettings}><Check size={16} />保存设置</button>} /><div className="settings-grid"><div><Panel title="审批通过自动入队" kicker="APPROVAL TO PUBLISH"><div className="queue-policy-state"><ShieldCheck size={24} /><div><h3>{approvalToQueue ? '已启用 · 审批后自动发布' : '尚未启用审批入队'}</h3><p>启用时后台核实当前登录账号并绑定发布策略。人工批准当前版本后，后台自动入队，无需再次逐篇确认。</p></div><Badge tone={approvalToQueue ? 'green' : 'neutral'}>{approvalToQueue ? '已启用' : '已关闭'}</Badge></div><div className="bound-account"><Globe size={18} /><div><strong>{settings?.approved_account_name || (settings?.approved_account_id ? '已核实账号' : '尚未绑定发布账号')}</strong><small>{settings?.approved_account_id ? `账号 ID：${settings.approved_account_id}` : '开启策略时将从 MCP 获取当前账号，前端不能自行指定账号 ID'}</small></div></div><label className="toggle-row"><span><strong>审批通过，自动加入发布队列</strong><small>真实内容 · 公开可见 · 当前版本与图片绑定</small></span><input type="checkbox" checked={approvalToQueue} disabled={!!busy || !settings || (!approvalToQueue && !mcp?.logged_in)} onChange={e => updateQueuePolicy(e.target.checked)} /></label><div className="inline-note"><Pause size={15} />关闭策略后暂停全部发布，并取消未提交的自动队列；已提交任务可能无法撤回。停止开关、配额与未知结果保护始终生效。</div></Panel><Panel title="小红书 MCP 连接" kicker="PLATFORM CONNECTION"><div className="settings-connection"><div className="connection-icon"><Globe size={23} /></div><div><h3>{mcp?.logged_in ? '已登录小红书' : mcp?.connected ? '服务就绪，等待登录' : '尚未连接本地 MCP'}</h3><p>{mcp?.detail ?? '正在检查连接状态'}</p></div><Badge tone={mcp?.logged_in ? 'green' : 'amber'}>{mcp?.logged_in ? '已登录' : mcp?.connected ? '待扫码' : '未连接'}</Badge></div><label className="field">MCP 地址<input value={settingsForm.mcpUrl} onChange={e => setSettingsForm({ ...settingsForm, mcpUrl: e.target.value })} placeholder="http://localhost:18060/mcp" /></label><div className="button-row"><button className="button outline" disabled={!!busy || !mcp?.connected} onClick={() => act('获取登录二维码', async () => { const result = await api<{ image_url: string; detail: string }>('/mcp/qrcode', 'POST'); setQr(result); return result; }, '请使用小红书 App 扫码登录，随后刷新登录状态。')}><Globe size={16} />获取登录二维码</button><button className="button subtle" disabled={!!busy} onClick={() => act('刷新账号状态', async () => { const result = await api<McpStatus>('/mcp/status?refresh=true'); setMcp(result); return result; }, '连接状态已刷新。')}><RefreshCw size={15} />刷新状态</button></div>{qr && <div className="qr-panel">{qr.image_url ? <img src={qr.image_url} alt="小红书登录二维码，请使用小红书 App 扫码" /> : <CircleAlert size={30} />}<div><strong>使用小红书 App 扫码</strong><p>{qr.detail}</p><small>账号登录由你完成；Cookie 与 Token 不会在控制台显示。</small></div></div>}<details className="source-details"><summary><Layers3 size={14} />当前发现的 MCP 工具（{mcp?.tools?.length ?? 0}）<ChevronRight size={14} /></summary><div className="tool-tags">{mcp?.tools?.map(tool => <code key={tool}>{tool}</code>)}</div></details></Panel><Panel title="内容定位与来源" kicker="EDITORIAL DIRECTION"><label className="field">账号定位<textarea value={settingsForm.positioning} onChange={e => setSettingsForm({ ...settingsForm, positioning: e.target.value })} rows={3} /></label><label className="field">核心关键词<input value={settingsForm.keywords} onChange={e => setSettingsForm({ ...settingsForm, keywords: e.target.value })} placeholder="旅行、美食、生活、职场…" /></label><label className="field">RSS 来源<textarea value={settingsForm.rss} onChange={e => setSettingsForm({ ...settingsForm, rss: e.target.value })} placeholder="每行一个已授权或公开 RSS 地址" rows={4} /></label><small className="muted">研究来源需保留发布时间与出处；不会递归读取电脑上的其他项目。</small></Panel><details className="advanced-settings"><summary>高级任务与诊断</summary><Panel title="手动运行任务" kicker="AGENT OPERATIONS"><div className="task-grid">{Object.entries(agentLabels).filter(([key]) => key.includes('_')).map(([key, label]) => <button className="task-button" key={key} disabled={!!busy || (key === 'publish_approved' && paused)} onClick={() => runTask(key)}><span>{label}<small>{key}</small></span><Play size={15} /></button>)}</div><p className="footnote">发布队列只处理按策略批准的内容。停止开关、账号绑定与发布配额始终生效。</p></Panel></details></div><div><Panel title="Codex CLI 创作" kicker="LOCAL CODEX"><div className="model-status"><Sparkles size={22} /><div><strong>{settings?.model_configured ? 'Codex CLI 已安装' : 'Codex CLI 尚未找到'}</strong><p>{settings?.model_detail || '使用本机 Codex 登录身份；安装状态不代表登录成功；认证以真实调用结果为准。'}</p></div></div><details className="advanced-settings"><summary>测试模式</summary><label className="field">创作模式<select value={settingsForm.modelMode} onChange={e => setSettingsForm({ ...settingsForm, modelMode: e.target.value })}><option value="live">Live · 本机 Codex CLI</option><option value="mock">Mock · 本地流程测试</option></select></label></details><label className="field">模型<input readOnly value="gpt-6.1-sol" /></label><label className="field">推理强度<input readOnly value="high" /></label><div className="cost-row"><div><span>已记录模型调用</span><strong>{dashboard?.costs?.calls ?? '—'}<small>次</small></strong></div><div><span>CLI 使用额度</span><strong style={{ fontSize: 14 }}>Codex 账户</strong></div></div><div className="inline-note"><LockKeyhole size={15} />选题、策划、写稿与修改均通过本机 CLI。请在终端运行 codex login；真实调用可能需要数分钟，结果见运行记录。</div></Panel><Panel title="质量与发布边界" kicker="CONTROL & LIMITS"><div className="two-fields"><label className="field">每日生产目标<input type="number" min={1} max={100} value={settingsForm.target} onChange={e => setSettingsForm({ ...settingsForm, target: Number(e.target.value) })} /></label><label className="field">每日发布上限<input type="number" min={0} max={50} value={settingsForm.dailyLimit} onChange={e => setSettingsForm({ ...settingsForm, dailyLimit: Number(e.target.value) })} /></label></div><label className="field">质量评分阈值<div className="range-row"><input type="range" min={0} max={100} value={settingsForm.threshold} onChange={e => setSettingsForm({ ...settingsForm, threshold: Number(e.target.value) })} /><strong>{settingsForm.threshold}</strong></div></label><label className="toggle-row"><span><strong>内容研究与生产调度</strong><small>独立于 Codex 进程运行</small></span><input type="checkbox" checked={settingsForm.scheduler} onChange={e => setSettingsForm({ ...settingsForm, scheduler: e.target.checked })} /></label><div className="inline-note"><ShieldCheck size={15} />生产目标是创作容量。真实发布数量由账号状态、平台限制与已启用的审批入队策略决定。</div></Panel><Panel className="safety-panel"><Pause size={24} /><h3>{paused ? '全部发布当前已暂停' : '你始终可以停止发布'}</h3><p>停止开关阻止后续提交；已经发往平台的请求可能无法撤回。异常登录、验证码或结果不确定时，交由人工处理。</p><button className="button outline full" disabled={pauseBusy || !dashboard} onClick={() => void setPublishingPause(true)}><Pause size={16} />停止全部发布</button></Panel></div></div></>;
  }

  return <div className="app-shell"><aside className={`sidebar ${mobileNav ? 'open' : ''}`}><button className="brand" onClick={() => go('dashboard')}><div className="brand-mark"><NotebookPen size={23} /></div><span>XHS GROWTH<small>你的内容运营工作室</small></span></button><div className="workspace-chip"><span className="workspace-icon">文</span><div><strong>我的内容工作室</strong><small>本地工作空间</small></div><ChevronRight size={14} /></div><span className="nav-label">工作空间 / WORKSPACE</span><nav>{nav.map(item => <button key={item.id} className={`nav-item ${page === item.id ? 'active' : ''}`} onClick={() => go(item.id)}><item.icon size={19} /><span>{item.name}</span>{item.id === 'review' && pending.length > 0 && <small>{pending.length}</small>}{page === item.id && <span className="nav-active-dot" />}</button>)}</nav><div className="sidebar-bottom"><div className="sidebar-note"><div><Sparkles size={17} /><strong>人类主编，Agent 协作</strong></div><p>把重复工作交给系统。<br />把观点和判断留给你。</p></div><button className={`sidebar-pause ${paused ? 'paused' : ''}`} disabled={pauseBusy || !dashboard} onClick={() => void setPublishingPause(!paused)}><span className="status-light" />{paused ? '发布已暂停' : '停止全部发布'}<Pause size={16} /></button><div className="local-user"><span className="avatar">K</span><div><strong>本地主编</strong><small>Asia / Shanghai</small></div><Settings2 size={17} /></div></div></aside>{mobileNav && <button className="nav-scrim" aria-label="关闭导航" onClick={() => setMobileNav(false)} />}<div className="main-shell"><header className="topbar"><div className="breadcrumb"><button className="mobile-menu icon-button" aria-label="打开导航" onClick={() => setMobileNav(true)}><Menu size={20} /></button><span>工作空间</span><ChevronRight size={13} /><strong>{currentNav.name}</strong></div><div className="topbar-right"><span className="header-date">{dateText}</span><button className="refresh-button" aria-label="刷新所有数据" title="刷新数据" disabled={loading || !!busy} onClick={() => { setLoading(true); void refresh(); }}><RefreshCw size={16} className={loading ? 'spin' : ''} /></button></div></header><main className="main-content">{errors.length > 0 && <div className="backend-error"><CircleAlert size={19} /><div><strong>部分本地数据暂时无法读取</strong><p>请确认后端在 127.0.0.1:18760 运行。数据不会由前端模拟填充。</p><details><summary>查看诊断（{errors.length}）</summary>{errors.map(error => <p key={error}>{error}</p>)}</details></div><button className="text-button" onClick={() => void refresh()}>重试<RefreshCw size={14} /></button></div>}{notice && <div className={`notice ${notice.kind}`} role="status">{notice.kind === 'success' ? <Check size={19} /> : <CircleAlert size={19} />}<span>{notice.text}</span><button className="icon-button" aria-label="关闭通知" onClick={() => setNotice(undefined)}><X size={16} /></button></div>}{loading && !dashboard ? <div className="initial-loading"><LoaderCircle size={30} className="spin" /><p>连接本地创作工作空间…</p></div> : page === 'dashboard' ? dashboardPage() : page === 'topics' ? topicsPage() : page === 'studio' ? studioPage() : page === 'review' ? reviewPage() : page === 'publish' ? publishPage() : page === 'analytics' ? analyticsPage() : settingsPage()}<footer className="app-footer"><span>XHS GROWTH AGENT <span>·</span> 让创作回到有价值的表达。</span><span><span className="status-light online" />输入方向 · 审核筛选 · 自动队列</span></footer></main></div>{creationSeed && <CreationDialog seed={creationSeed} submitting={creation.submitting} error={creation.error} onClose={() => setCreationSeed(undefined)} onSubmit={async request => { await creation.submit(request); setCreationSeed(undefined); setReviewScope("current"); setSelectedReviews([]); go("review"); }} />}{busy && <div className="busy-indicator" role="status"><LoaderCircle size={18} className="spin" />{busy}…</div>}</div>;
}

function PageHeading({ kicker, title, text, aside }: { kicker: string; title: string; text: string; aside?: ReactNode }) {
  return <div className="page-heading"><div><span className="eyebrow">{kicker}</span><h1>{title}</h1><p>{text}</p></div>{aside}</div>;
}
function ReportItem({ title, value }: { title: string; value: unknown }) {
  return <div className="report-item"><span>{title}</span><div>{readable(value)}</div></div>;
}
