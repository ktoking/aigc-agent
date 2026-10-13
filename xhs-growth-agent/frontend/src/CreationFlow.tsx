import { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowRight, Check, CircleAlert, ExternalLink, Flame, LoaderCircle, RefreshCw, X } from 'lucide-react';
import { api, type Topic } from './api';

export interface BackgroundTask {
  id: string; status: string; stage: string; direction?: string; article_ids?: string[];
  error?: string | null; created_at?: string;
}
export interface CreationRequest { direction: string; count: number; topic_ids?: string[]; material?: string }
export interface CreationSeed { direction?: string; topic_ids?: string[]; material?: string }
const active = (task?: BackgroundTask | null) => !!task && ['QUEUED', 'RUNNING', 'PENDING'].includes(task.status);
const terminalSuccess = (task: BackgroundTask) => ['SUCCEEDED', 'COMPLETED', 'SUCCESS'].includes(task.status);
const errorText = (error: unknown) => error instanceof Error ? error.message : String(error);
const stageLabel: Record<string, string> = {
  queued: '等待创作', research: '查找相关资料', researching: '查找相关资料', planning: '确定写作角度',
  writing: '撰写正文', generating: '撰写正文', rendering: '制作配图', quality: '检查内容',
  blocked: '任务暂时无法完成', review_ready: '稿件已就绪', fetching: '查找公开资讯', collecting: '查找公开资讯', interrupted: '任务已中断',
  review: '整理待审核稿', completed: '等待你审核', done: '等待你审核', failed: '执行失败',
};
export function taskStage(task: BackgroundTask) { return stageLabel[task.stage?.toLowerCase()] ?? task.stage ?? task.status; }

/** The task lives above page routing: navigation never cancels creation. */
export function useCreationFlow(onComplete: (task: BackgroundTask) => Promise<void>) {
  const [task, setTask] = useState<BackgroundTask>();
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const reportedArticles = useRef('');
  const complete = useRef(onComplete);
  complete.current = onComplete;
  useEffect(() => {
    let mounted = true;
    void api<BackgroundTask | null>('/creation/tasks/latest').then(value => {
      if (mounted && value?.id) { setTask(value); if (!active(value)) reportedArticles.current = `${value.id}:${value.article_ids?.join(',') ?? ''}`; }
    }).catch(() => {});
    return () => { mounted = false; };
  }, []);
  const poll = useCallback(async (id: string) => {
    const next = await api<BackgroundTask>(`/creation/tasks/${id}`);
    setTask(next); setError('');
    const available = `${next.id}:${next.article_ids?.join(',') ?? ''}`;
    if (next.article_ids?.length && reportedArticles.current !== available) {
      await complete.current(next); // show each ready draft without waiting for the whole batch
      reportedArticles.current = available;
    }
  }, []);
  useEffect(() => {
    if (!task || !active(task)) return;
    let disposed = false;
    let timer: ReturnType<typeof setTimeout>;
    const tick = async () => {
      try { await poll(task.id); } catch (error) { if (!disposed) setError(errorText(error)); }
      if (!disposed) timer = setTimeout(tick, 2500);
    };
    timer = setTimeout(tick, 1000);
    return () => { disposed = true; clearTimeout(timer); };
  }, [task?.id, task?.status, poll]);
  const submit = async (request: CreationRequest) => {
    setSubmitting(true); setError('');
    try {
      const next = await api<BackgroundTask>('/creation/tasks', 'POST', request);
      setTask(next); reportedArticles.current = '';
      return next;
    } catch (error) { setError(errorText(error)); throw error; }
    finally { setSubmitting(false); }
  };
  return { task, error, submitting, running: active(task), submit, retryRead: () => task && poll(task.id).catch(error => setError(errorText(error))) };
}

export function CreationDialog({ seed, submitting, error, onClose, onSubmit }: {
  seed: CreationSeed; submitting: boolean; error: string; onClose: () => void;
  onSubmit: (request: CreationRequest) => Promise<void>;
}) {
  const [direction, setDirection] = useState(seed.direction ?? '');
  const [material, setMaterial] = useState(seed.material ?? '');
  const [count, setCount] = useState(1);
  return <div className="modal-backdrop" onClick={event => { if (event.target === event.currentTarget && !submitting) onClose(); }}>
    <section className="creation-dialog" role="dialog" aria-modal="true" aria-labelledby="creation-heading">
      <div className="modal-heading"><div><span className="eyebrow">从你的方向开始</span><h2 id="creation-heading">这次，想写什么？</h2></div><button className="icon-button" aria-label="关闭准备内容" disabled={submitting} onClick={onClose}><X size={20} /></button></div>
      <form onSubmit={event => { event.preventDefault(); if (direction.trim() && !submitting) void onSubmit({ direction: direction.trim(), count, ...(material.trim() ? { material: material.trim() } : {}), ...(seed.topic_ids?.length ? { topic_ids: seed.topic_ids } : {}) }).catch(() => {}); }}>
        <label className="field">内容方向 <span className="muted">必填，可以写任何领域</span><textarea autoFocus rows={3} required maxLength={300} value={direction} onChange={event => setDirection(event.target.value)} placeholder="例如：给周末去杭州的朋友写一篇轻松的两日游攻略，预算 800 元，少排队。" /></label>
        <div className="direction-presets">{['生活', '旅行', '美食', '职场'].map(value => <button type="button" key={value} onClick={() => setDirection(value)}>{value}</button>)}</div>
        <label className="field">补充素材 <span className="muted">可选，粘贴经历、要点或参考链接</span><textarea rows={4} maxLength={10000} value={material} onChange={event => setMaterial(event.target.value)} placeholder="你亲自经历的细节、一定要写的内容、不能写的内容…" /></label>
        <div className="creation-bottom"><label className="field">生成篇数<select value={count} onChange={event => setCount(Number(event.target.value))}>{[1, 2, 3].map(value => <option key={value} value={value}>{value} 篇</option>)}</select></label><p>提交后进入审核中心。你可以继续浏览，完成后筛选、修改或批准发布。</p></div>
        {error && <p className="flow-error" role="alert">{error}</p>}
        <button className="button primary full" type="submit" disabled={!direction.trim() || submitting}>{submitting ? <LoaderCircle className="spin" size={17} /> : <ArrowRight size={17} />}{submitting ? '提交任务…' : '准备内容，去审核'}</button>
      </form>
    </section>
  </div>;
}

export function CreationProgress({ task, error, onRetry, onShow }: { task?: BackgroundTask; error: string; onRetry: () => void; onShow: () => void }) {
  if (!task) return null;
  const running = active(task);
  return <section className={`creation-progress ${running ? 'running' : ''}`} role="status">
    {running ? <LoaderCircle className="spin" size={22} /> : terminalSuccess(task) ? <Check size={22} /> : <CircleAlert size={22} />}
    <div><strong>{taskStage(task)}</strong><p>{task.direction ?? '本次创作'}{running ? ' · 后台继续运行，可以离开此页。' : task.article_ids?.length ? ` · 已生成 ${task.article_ids.length} 篇，等待你筛选。` : ''}</p>{(task.error || error) && <p className="flow-error">{task.error || error}</p>}</div>
    {error ? <button className="button outline small" onClick={onRetry}>刷新进度</button> : !!task.article_ids?.length && <button className="button outline small" onClick={onShow}>只看本次</button>}
  </section>;
}

interface Hotspots { items: Topic[]; updated_at?: string | null; loading?: boolean; sources?: string[]; errors?: unknown[] }
export function HotspotsPage({ onCreate }: { onCreate: (seed: CreationSeed) => void }) {
  const [data, setData] = useState<Hotspots>({ items: [] });
  const [direction, setDirection] = useState('');
  const [appliedDirection, setAppliedDirection] = useState('');
  const appliedRef = useRef(appliedDirection);
  appliedRef.current = appliedDirection;
  const [task, setTask] = useState<BackgroundTask>();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState<string[]>([]);
  const [hidden, setHidden] = useState<string[]>([]);
  const [loaded, setLoaded] = useState(false);
  const mounted = useRef(true);
  const load = useCallback(async () => {
    try {
      const next = await api<Hotspots>(`/hotspots?direction=${encodeURIComponent(appliedDirection)}`);
      if (mounted.current && appliedRef.current === appliedDirection) { setData(next); setError(''); }
    } catch (error) { if (mounted.current && appliedRef.current === appliedDirection) setError(errorText(error)); }
    finally { if (mounted.current && appliedRef.current === appliedDirection) setLoaded(true); }
  }, [appliedDirection]);
  useEffect(() => { mounted.current = true; void load(); return () => { mounted.current = false; }; }, [load]);
  useEffect(() => {
    if (!active(task) && !data.loading) return;
    let disposed = false;
    let timer: ReturnType<typeof setTimeout>;
    const tick = async () => {
      try {
        if (task?.id) {
          const next = await api<BackgroundTask>(`/hotspots/tasks/${task.id}`);
          if (!disposed) setTask(next);
        }
        await load();
      } catch (error) { if (!disposed) setError(errorText(error)); }
      if (!disposed) timer = setTimeout(tick, 2500);
    };
    timer = setTimeout(tick, 1000);
    return () => { disposed = true; clearTimeout(timer); };
  }, [task?.id, task?.status, data.loading, load]);
  const refresh = async () => {
    const requested = direction.trim();
    setSubmitting(true); setError(''); setSelected([]); setHidden([]);
    if (requested !== appliedDirection) { setData({ items: [] }); setAppliedDirection(requested); setLoaded(false); }
    try { setTask(await api<BackgroundTask>('/hotspots/refresh', 'POST', { direction: requested })); }
    catch (error) { setError(errorText(error)); }
    finally { setSubmitting(false); }
  };
  const writing = (ids: string[]) => {
    const chosen = data.items.filter(topic => ids.includes(topic.id));
    onCreate({ topic_ids: ids, direction: `${appliedDirection ? appliedDirection + '：' : ''}${chosen.map(topic => topic.title).join('；')}`.slice(0, 300) });
  };
  const items = data.items.filter(topic => !hidden.includes(topic.id));
  const loading = submitting || active(task) || data.loading;
  return <>
    <div className="page-heading"><div><span className="eyebrow">最近热点</span><h1>看看今天，大家在聊什么。</h1><p>从公开资讯找到近期话题，选中后按你的方向写成草稿。</p></div></div>
    <form className="toolbar panel hotspots-toolbar" onSubmit={event => { event.preventDefault(); void refresh(); }}><label className="search"><Flame size={17} /><input maxLength={150} value={direction} onChange={event => setDirection(event.target.value)} placeholder="不限领域，或输入旅行、美食、职场…" /></label><button className="button primary" type="submit" disabled={loading}>{loading ? <LoaderCircle className="spin" size={16} /> : <RefreshCw size={16} />}{loading ? '查找近期热点…' : '刷新近期热点'}</button></form>
    {loading && <div className="creation-progress"><LoaderCircle className="spin" size={20} /><div><strong>{task ? taskStage(task) : '查找公开资讯'}</strong><p>后台获取来源，页面可以继续操作。</p></div></div>}
    {error && <p className="flow-error" role="alert">{error}</p>}
    <div className="section-toolbar"><div><h2>近期话题 <span className="count-pill">{items.length}</span></h2><p>{data.updated_at ? `更新于 ${new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Shanghai', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(data.updated_at))}` : '刷新后显示真实来源结果'}{data.sources?.length ? ` · ${data.sources.join(' / ')}` : ''} · 最多选 5 个话题</p></div><button className="button outline" disabled={!selected.length} onClick={() => writing(selected)}>用选中话题写草稿 {selected.length ? `(${selected.length})` : ''}<ArrowRight size={15} /></button></div>
    {items.length ? <div className="topic-grid">{items.map((topic, i) => <section className="topic-card panel" key={topic.id}><div className="topic-top"><label className="select-all"><input type="checkbox" disabled={selected.length >= 5 && !selected.includes(topic.id)} checked={selected.includes(topic.id)} onChange={event => setSelected(event.target.checked ? [...selected, topic.id] : selected.filter(id => id !== topic.id))} /><span className="topic-index">{String(i + 1).padStart(2, '0')}</span></label><span className="badge neutral">{topic.category}</span></div><h3>{topic.title}</h3><div className="topic-reasons">{topic.reasons?.slice(0, 2).map((reason, j) => <p key={j}>{reason}</p>)}</div><div className="hotspot-sources">{topic.sources?.map((source, j) => /^https?:\/\//i.test(source.url) && <a href={source.url} target="_blank" rel="noreferrer" key={j}>{source.title || '查看出处'}<ExternalLink size={12} /></a>)}</div><div className="topic-actions"><button className="text-button" onClick={() => writing([topic.id])}>用此选题写草稿<ArrowRight size={14} /></button><button className="icon-button" title="隐藏此话题" onClick={() => { setHidden([...hidden, topic.id]); setSelected(selected.filter(id => id !== topic.id)); }}><X size={15} /></button></div></section>)}</div> : <section className="panel"><div className="empty"><div className="empty-icon"><Flame size={25} /></div><h3>{!loaded ? '读取近期热点…' : loading ? '正在整理近期资讯' : '先看看近期热点'}</h3><p>{!loaded || loading ? '找到的来源会显示在这里。' : '点“刷新近期热点”，也可以先输入你感兴趣的领域。'}</p></div></section>}
    {!!data.errors?.length && <details className="source-details"><summary>部分来源暂时不可用 ({data.errors.length})</summary>{data.errors.map((value, i) => <p className="muted" key={i}>{typeof value === 'string' ? value : JSON.stringify(value)}</p>)}</details>}
  </>;
}
