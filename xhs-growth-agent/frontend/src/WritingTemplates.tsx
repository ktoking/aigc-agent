import {useEffect,useState} from 'react';
import {api} from './api';
import type {Tone} from './TonePicker';
interface Sample {id:string;title:string;likes_display:string;url:string}
interface Template {id:string;name:string;outline:string[];opening:string;example:string;ending:string;origin:string;sample_count:number;version:number;samples?:Sample[];feedback:{approved:number;filtered:number;observed_likes:number|null}}
interface Learning {status:string;stage:string;sample_count:number;target_samples:number;candidate_count:number;read_count:number;harness_version?:number;error?:string|null}
interface Harness {version:number;sample_count:number;title_rules:string[];body_rules:string[]}
export function WritingTemplates({tones,value,onChange,disabled=false}:{tones:Tone[];value:string;onChange:(value:string)=>void;disabled?:boolean}) {
 const [items,setItems]=useState<Template[]>([]),[learning,setLearning]=useState<Learning|null>(null),[harness,setHarness]=useState<Harness|null>(null),[error,setError]=useState(''),[busy,setBusy]=useState(false),[keywords,setKeywords]=useState('职场感悟、消费体验、生活感悟、周末生活');
 const key=tones.join(',')||'natural';
 const [refresh,setRefresh]=useState(0);
 useEffect(()=>{let gone=false;void api<{items:Template[];learning:Learning|null;harness:Harness|null}>(`/writing/templates?tones=${encodeURIComponent(key)}`).then(data=>{if(!gone){setItems(data.items);setLearning(data.learning);setHarness(data.harness);setError('')}}).catch(e=>{if(!gone)setError(e instanceof Error?e.message:String(e))});return()=>{gone=true}},[key,refresh]);
 useEffect(()=>{if(learning?.status!=='RUNNING')return;let gone=false;const timer=setInterval(()=>{void api<Learning|null>('/writing/learning/latest').then(next=>{if(!gone){setLearning(next);if(next?.status!=='RUNNING')setRefresh(v=>v+1)}}).catch(()=>{})},3000);return()=>{gone=true;clearInterval(timer)}},[learning?.status]);
 const selected=items.find(t=>t.id===value)||items[0];
 const learn=async(target_samples:number)=>{setBusy(true);setError('');try{const next=await api<Learning>('/writing/learn','POST',{keywords:keywords.split(/[、,，]/).map(v=>v.trim()).filter(Boolean),target_samples});setLearning(next);if(next.status!=='RUNNING')setRefresh(v=>v+1)}catch(e){setError(e instanceof Error?e.message:String(e))}finally{setBusy(false)}};
 return <section className="writing-templates">
  <label className="field">写法模板 <span className="muted">跟随语气推荐，也可以手选</span><select value={value} disabled={disabled} onChange={e=>onChange(e.target.value)}><option value="auto">自动选写法</option>{items.map(t=><option key={t.id} value={t.id}>{t.name}{t.origin==='learned'?' · 高赞样本提炼':''}</option>)}</select></label>
  {selected&&<div className="writing-template-preview"><strong>{selected.name}</strong><small>{selected.origin==='learned'?`${selected.sample_count} 篇真实样本 · v${selected.version}`:'内置结构 · 不保证热度'}</small><p>{selected.outline.join(' → ')}</p><blockquote>开头示例：{selected.example}</blockquote><details><summary>查看开头公式与样本</summary><p>{selected.opening}</p><p>收尾：{selected.ending}</p>{selected.samples?.map(sample=><p key={sample.id}><a href={sample.url} target="_blank" rel="noreferrer">{sample.title}</a> · 采样时 {sample.likes_display} 赞</p>)}</details><small>只借结构；亲历、数字和对话必须来自你的真实素材。</small>{!!(selected.feedback.approved+selected.feedback.filtered)&&<small>已采用 {selected.feedback.approved} 次 · 已过滤 {selected.feedback.filtered} 次</small>}</div>}
  {harness&&<details><summary>写作 Harness v{harness.version} · {harness.sample_count} 篇完整正文</summary><p>标题切口：{harness.title_rules.join('；')}</p><p>正文组织：{harness.body_rules.join('；')}</p><small>语气组合、开头、收尾与避免的问题会一起传给模型，使用当前版本，优先你的本次要求。</small></details>}
  <details><summary>学习高赞写法</summary><p>读取半年内的高赞图文，提炼模板、语气和内容组织规则，保存成 Harness 新版本。生成直接用本地结果，审核反馈调整推荐。</p><input aria-label="学习关键词" maxLength={123} value={keywords} onChange={e=>setKeywords(e.target.value)} placeholder="1至4个关键词，用顿号分开"/><button type="button" className="button outline small" disabled={disabled||busy||learning?.status==='RUNNING'} onClick={()=>void learn(20)}>{learning?.status==='RUNNING'?'后台学习中…':'深入学习 · 20篇'}</button><button type="button" className="button outline small" disabled={disabled||busy||learning?.status==='RUNNING'} onClick={()=>void learn(4)}>快速更新 · 4篇</button></details>
  {learning&&<p className="template-learning-status">{learning.status==='RUNNING'?`完整正文 ${learning.sample_count}/${learning.target_samples} 篇，${learning.stage==='ANALYZING'?'正在提炼 Harness':`已尝试读取 ${learning.read_count} 篇`}。可以关闭表单。`:learning.status==='COMPLETED'?`学习完成：${learning.sample_count} 篇真实正文${learning.harness_version?`，Harness v${learning.harness_version}`:''}。`:learning.error}</p>}
  {error&&<p className="flow-error">{error}；自动写法仍可用。</p>}
 </section>;
}
