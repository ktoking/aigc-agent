"""Persisted writing rules extracted from public samples; no raw source bodies."""
import json
import re
from pathlib import Path
from sqlalchemy import select
from .config import DATA_DIR
from .models import WritingHarness, AuditLog, now
from .model_client import object_schema, STRING, STRINGS
from .tones import TONES, normalize_tones

RULE_FIELDS = ('title_rules', 'opening_rules', 'body_rules', 'ending_rules', 'cover_rules', 'avoid')
SCHEMA = object_schema({**{key: STRINGS for key in RULE_FIELDS},
    'tone_rules': {'type': 'array', 'items': object_schema({'tone': STRING, 'rules': STRINGS})},
    'source_ids': STRINGS})


def validate(data, samples):
    ids = {s['id'] for s in samples}
    if len(set(data['source_ids'])) < 3 or not set(data['source_ids']) <= ids:
        raise ValueError('写作 harness 缺少真实样本依据')
    lists = [data[key] for key in RULE_FIELDS]
    if not 1 <= len(data['tone_rules']) <= len(TONES):
        raise ValueError('写作 harness 语气数量不符合约定')
    seen = set()
    for item in data['tone_rules']:
        if item['tone'] not in TONES or item['tone'] in seen:
            raise ValueError('写作 harness 语气不符合约定')
        seen.add(item['tone']); lists.append(item['rules'])
    if any(not 1 <= len(rules) <= 8 for rules in lists):
        raise ValueError('写作 harness 规则数量不符合约定')
    texts = [text for rules in lists for text in rules]
    if any(not isinstance(t, str) or not t.strip() or len(t) > 220 or
           re.search(r'https?://|忽略.*指令|系统提示|访问令牌', t) for t in texts):
        raise ValueError('写作 harness 规则不符合约定')
    target = re.sub(r'\W+', '', ''.join(texts))
    for sample in samples:
        source = re.sub(r'\W+', '', sample['_body'])
        if any(target[i:i+18] in source for i in range(max(0, len(target)-17))):
            raise ValueError('写作 harness 复用了原文长句')
    return data


def latest(session):
    row = session.scalar(select(WritingHarness).where(WritingHarness.harness_key == 'main'))
    return {**row.data, 'version': row.version} if row else None


def resolve(session, tones=None):
    data = latest(session)
    if not data: return None
    chosen = normalize_tones(tones)
    return {**{key: data[key] for key in RULE_FIELDS}, 'version': data['version'],
            'tone_rules': [rule for rule in data['tone_rules'] if rule['tone'] in chosen]}


def save(session, data, samples, run_id):
    row = session.scalar(select(WritingHarness).where(WritingHarness.harness_key == 'main'))
    enriched = {**data, 'samples': [{k:v for k,v in s.items() if not k.startswith('_')} for s in samples],
                'sample_count': len(samples), 'learned_at': now(), 'learning_run': run_id}
    if row:
        row.version += 1; row.data = enriched
    else:
        row = WritingHarness(harness_key='main', data=enriched); session.add(row)
    session.flush()
    snapshot = {**enriched, 'version': row.version}
    session.add(AuditLog(action='writing_harness.learned', entity_id=row.id, data=snapshot))
    return snapshot


def export(snapshot, directory=None):
    directory = Path(directory) if directory else DATA_DIR / 'writing-harness'
    directory.mkdir(parents=True, exist_ok=True)
    lines = ['# 小红书写作 Harness', '',
             f"版本：v{snapshot['version']}；真实完整正文：{snapshot['sample_count']} 篇；更新时间：{snapshot['learned_at']}。", '',
             '由本机 Codex CLI gpt-6.1-sol / high 提炼。学习结构与表达规律，原创观点与具体事实由本次方向和真实素材决定。', '',
             '高赞是采样时观察值，不证明写法带来热度；未分析图片像素，封面规则仅为设计建议。', '']
    names = dict(zip(RULE_FIELDS, ('标题切口','开头进入','正文组织','收尾','单图封面','避免的问题')))
    for key in RULE_FIELDS:
        lines += [f'## {names[key]}', ''] + ['- '+rule for rule in snapshot[key]] + ['']
    lines += ['## 内置语气约定', '', '这些是主编可选的语气定义，与下方样本提炼分开；可组合最多4个。', '']
    for label, instruction in TONES.values():
        lines += [f'- **{label}**：{instruction}']
    lines += ['', '组合时，客观约束事实，主观或批判作用于判断；犀利表达可以配温和措辞。不在发布正文里介绍标签。', '', '## 样本提炼的语气规则', '']
    for item in snapshot['tone_rules']:
        lines += [f"### {TONES[item['tone']][0]}", ''] + ['- '+rule for rule in item['rules']] + ['']
    lines += ['## 真实样本', '', '| 标题 | 采样时点赞 | 领域关键词 |', '| --- | --- | --- |']
    for sample in snapshot['samples']:
        title = sample['title'].replace('|','／').replace('\n',' ')
        lines += [f"| [{title}]({sample['url']}) | {sample['likes_display']} | {sample['keyword']} |"]
    lines += ['', '## 运行闭环', '',
              '填写方向与素材 → 组合语气 → 选择写法 → 冻结 Harness 和模板版本 → Codex 生成 → 单图渲染 → 人工过滤或批准 → 记录真实审核与发布指标。', '',
              '普通生成直接读本地规则，不临时采集。审核反馈至少三次才调整模板推荐；新学习保留旧版本。学习与生成不自动批准或发布。']
    content = '\n'.join(lines)+'\n'
    for name, text in [(f"v{snapshot['version']}.json", json.dumps(snapshot, ensure_ascii=False, indent=2)),
                       (f"v{snapshot['version']}.md",content),('current.md',content)]:
        temporary = directory / (name+'.tmp')
        temporary.write_text(text, encoding='utf-8'); temporary.replace(directory / name)
    return str(directory / 'current.md')
