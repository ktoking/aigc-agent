import asyncio
from datetime import datetime
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo
import feedparser
import httpx
from sqlalchemy import select, func, update, or_
from .config import DEFAULTS, ROOT
from .models import *
from .mcp import XiaohongshuMcpAdapter, result_data, safe_data
from .model_client import ModelClient, configured, model_status, ModelUnavailable, MODEL_NAME, PROVIDER, REASONING_EFFORT
from .control import pause_requested, request_pause

AGENTS = ["Topic Research", "Chief Editor", "Content Writer", "Visual Designer", "Quality Reviewer", "Publishing", "Analytics & Growth"]

class WorkflowError(ValueError):
    pass

def serialize(record):
    return {column.name: getattr(record, column.name) for column in record.__table__.columns}

def settings(session):
    result = DEFAULTS.copy()
    result.update({row.key: row.value for row in session.scalars(select(Setting)).all()})
    result.update(model_name=MODEL_NAME, model_provider=PROVIDER, model_reasoning_effort=REASONING_EFFORT, model_detail=model_status()["detail"])
    result["model_configured"] = configured()
    result["paused"] = result["paused"] or pause_requested()
    return result

def save_settings(session, data):
    if any(key in data and data[key] != value for key, value in {"model_name": MODEL_NAME, "model_provider": PROVIDER, "model_reasoning_effort": REASONING_EFFORT}.items()):
        raise WorkflowError("模型固定使用本机 Codex CLI gpt-6.1-sol / high")
    if "paused" in data:
        request_pause(bool(data["paused"]))
    for key, value in data.items():
        if key not in DEFAULTS:
            raise WorkflowError(f"不支持设置项 {key}")
        row = session.get(Setting, key)
        if row:
            row.value = value
        else:
            session.add(Setting(key=key, value=value))
    session.commit()
    return settings(session)

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def text_key(text):
    return re.sub(r"\W+", "", text.lower())

def content_hash(article):
    return digest({"title": article.title, "body": article.body, "tags": article.tags, "version": article.version,
                   "ai_assisted": article.ai_assisted, "sources": article.sources,
                   "media": [{"id": m["id"], "sha256": m["sha256"], "path": m["path"]} for m in article.media]})

def audit(session, action, entity_id, data=None):
    session.add(AuditLog(action=action, entity_id=entity_id, data=safe_data(data or {})))

def start_run(session, name, mode="mock"):
    run = AgentRun(name=name, mode=mode)
    session.add(run)
    session.commit()
    return run

def finish_run(session, run, result, status="COMPLETED"):
    run.status = status
    run.result = safe_data(result)
    run.finished_at = now()
    session.commit()

def snapshot(session, article):
    existing = session.scalar(select(ArticleVersion).where(ArticleVersion.article_id == article.id, ArticleVersion.version == article.version))
    if not existing:
        session.add(ArticleVersion(article_id=article.id, version=article.version, data=serialize(article), content_hash=content_hash(article)))

def invalidate(session, article):
    session.execute(update(Approval).where(Approval.article_id == article.id).values(valid=False))
    session.execute(update(PublishAuthorization).where(PublishAuthorization.article_id == article.id).values(valid=False))
    jobs = session.scalars(select(PublishJob).where(PublishJob.article_id == article.id, PublishJob.status == "QUEUED")).all()
    for job in jobs:
        job.status = "CANCELLED"
        job.error = "文章编辑使原授权失效"

def assert_editable(session, article):
    if article.status in {"PUBLISHING", "PUBLISHED", "VERIFY_REQUIRED"}:
        raise WorkflowError("已提交或结果待核实的内容不能编辑，请先人工核实发布结果")

def quality_review(session, article):
    risks, reasons = [], []
    score = 100
    dimensions = {}
    if len(article.title) > 20 or not article.title.strip():
        risks.append("标题必须为 1 至 20 字")
        score -= 35
    else:
        reasons.append("标题长度符合 20 字上限")
    if len(article.body) > 1000 or len(article.body.strip()) < 100:
        risks.append("正文需要 100 至 1000 字，避免空洞内容")
        score -= 35
    else:
        reasons.append("正文有完整内容，符合 1000 字上限")
    if any(term in article.body + article.title for term in ["保证收益", "稳赚", "亲测月入", "亲身体验"]):
        risks.append("存在无法验证的体验或收益表达，需要人工补充事实证据")
        score -= 40
    if article.style == "通用建议" and not article.sources:
        reasons.append("通用建议没有冒充已核验个案；发布前由主编检查事实与适用条件")
    elif not article.sources:
        risks.append("缺少引用来源")
        score -= 30
    elif article.mode == "live" and not any(source.get("verified") for source in article.sources):
        risks.append("未读取到可靠来源，不能进入真实发布池")
        score -= 40
    else:
        reasons.append("保留来源链接；事实准确性仍需人工逐项核对")
    if len(article.media) < 3:
        risks.append("缺少封面或内容图，至少需要 3 张")
        score -= 30
    else:
        reasons.append("已生成原创封面及内容图")
    hashes = [media.get("sha256") for media in article.media]
    if len(set(hashes)) != len(hashes):
        risks.append("同篇重复图片")
        score -= 30
    if any(not media.get("source") or not media.get("license") for media in article.media):
        risks.append("图片来源或版权状态缺失")
        score -= 30
    for other in session.scalars(select(Article).where(Article.id != article.id)).all():
        similarity = SequenceMatcher(None, text_key(article.title + article.body), text_key(other.title + other.body)).ratio()
        threshold = 0.99 if article.mode == other.mode == "mock" else 0.90
        if similarity >= threshold:
            risks.append(f"与历史内容 {other.id[:8]} 文本相似度 {similarity:.0%}")
            score -= 50
            break
        other_hashes = {m.get("sha256") for m in other.media}
        if hashes and hashes[0] in other_hashes:
            risks.append("封面与历史内容图片哈希重复")
            score -= 40
            break
    if article.mode == "mock":
        reasons.append("Mock 内容仅验证系统生产容量，不能用于真实发布")
    score = max(0, score)
    dimensions.update({"title_and_limits": "checked", "platform_label": "follow_current_platform_requirements", "text_similarity": "checked",
                       "media_hashes": "checked", "fact_accuracy": "human_review_required", "visual_legibility": "human_review_required"})
    article.quality = {"score": score, "reasons": reasons, "risks": risks, "dimensions": dimensions,
                       "method": "规则预检，非事实核验或流量预测"}
    article.status = "PENDING_REVIEW" if score >= settings(session)["quality_threshold"] and not risks else "QUALITY_REJECTED"
    session.add(QualityReview(article_id=article.id, version=article.version, score=score, reasons=reasons, risks=risks))
    return article.quality

def render(session, article, template="minimal"):
    from .visual import render_article
    run = start_run(session, "Visual Designer", article.mode)
    try:
        media = render_article(article.id, article.title, article.cards, template=template)
        article.media = media
        for item in media:
            session.add(MediaAsset(article_id=article.id, path=item["path"], sha256=item["sha256"], source=item["source"], license=item["license"]))
        finish_run(session, run, {"article_id": article.id, "images": len(media), "template": template})
    except Exception as error:
        article.status = "FAILED"
        finish_run(session, run, {"error": type(error).__name__}, "FAILED")
        raise

def make_article(session, data, mode="live", topic_id=None):
    article = Article(id=uid(), topic_id=topic_id, title=data["title"], title_candidates=data.get("title_candidates", [data["title"]]),
        body=data["body"], tags=data.get("tags", []), sources=data.get("sources", []), category=data.get("category", "AI 与开发技术"),
        style=data.get("style", "技术实操教程"), cards=data.get("cards", []), comment_prompt=data.get("comment_prompt", ""),
        mode=mode, ai_assisted=True, fingerprint=digest(text_key(data["title"] + data["body"])))
    session.add(article)
    for source in article.sources:
        session.add(Source(title=source.get("title", "引用来源"), url=source.get("url", ""), verified=bool(source.get("verified")), retrieved_at=source.get("retrieved_at"), credibility="retrieved" if source.get("verified") else "unverified", details={"article_id": article.id}))
    session.commit()
    render(session, article, data.get("template", "minimal"))
    run = start_run(session, "Quality Reviewer", mode)
    quality_review(session, article)
    snapshot(session, article)
    finish_run(session, run, {"article_id": article.id, "quality": article.quality})
    audit(session, "article.generated", article.id, {"mode": mode, "version": article.version})
    session.commit()
    return article

MOCK_DOMAINS = ["日志诊断", "依赖管理", "幂等发布", "内容缓存", "密钥管理", "来源核验", "失败恢复", "本地数据库", "队列调度", "人工审核"]
MOCK_TASKS = ["最小输入", "异常边界", "版本记录", "状态迁移", "操作审计", "运行成本", "权限检查", "测试设计", "结果回读", "每日复盘"]

class TopicResearchAgent:
    async def run(self, session, mode="mock", count=100, keywords=None):
        run = start_run(session, "Topic Research", mode)
        candidates, blocked = [], []
        try:
            if mode == "mock":
                for domain in MOCK_DOMAINS:
                    for task in MOCK_TASKS:
                        candidates.append({"title": f"{domain}：{task}怎么做", "category": "AI 与开发技术", "sources": [{"title": "系统容量测试合成选题", "url": "", "verified": False}], "evidence": {"synthetic": True, "domain": domain, "task": task}})
            else:
                config = settings(session)
                async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                    for url in config["rss_urls"]:
                        try:
                            response = await client.get(url)
                            response.raise_for_status()
                            feed = feedparser.parse(response.content)
                            for entry in feed.entries[:40]:
                                title, link = entry.get("title", ""), entry.get("link", "")
                                if title and link:
                                    candidates.append({"title": title, "category": "AI 与开发技术", "sources": [{"title": title, "url": link, "verified": True, "retrieved_at": now()}], "evidence": {"source": "rss", "published": entry.get("published"), "excerpt": re.sub("<[^>]+>", "", entry.get("summary", ""))[:1500]}})
                        except Exception as error:
                            blocked.append(f"RSS {url}: {type(error).__name__}")
                    try:
                        response = await client.get("https://api.github.com/search/repositories", params={"q": "topic:ai-agent archived:false", "sort": "updated", "per_page": 30}, headers={"Accept": "application/vnd.github+json"})
                        response.raise_for_status()
                        for item in response.json().get("items", []):
                            candidates.append({"title": f"开源项目 {item['full_name']} 能解决什么", "category": "Codex / MCP / Agent 实战", "sources": [{"title": item["full_name"], "url": item["html_url"], "verified": True, "retrieved_at": now()}], "evidence": {"source": "github", "description": item.get("description"), "stars": item.get("stargazers_count"), "updated_at": item.get("updated_at"), "trend": "未取得历史增长数据"}})
                    except Exception as error:
                        blocked.append(f"GitHub: {type(error).__name__}")
                adapter = XiaohongshuMcpAdapter(config["mcp_url"])
                try:
                    health = await adapter.health()
                    if health["logged_in"]:
                        for keyword in (keywords or config["keywords"])[:5]:
                            data = await adapter.search(keyword)
                            feeds = data.get("feeds", data.get("items", []))
                            for feed in feeds[:25]:
                                card = feed.get("noteCard", feed.get("note_card", {}))
                                title = card.get("displayTitle", card.get("title", ""))
                                feed_id = feed.get("id", "")
                                if title and feed_id:
                                    candidates.append({"title": f"{title}：独立分析与补充", "category": "AI 与开发技术", "sources": [{"title": title, "url": f"https://www.xiaohongshu.com/explore/{feed_id}", "verified": True, "retrieved_at": now()}], "evidence": {"source": "xiaohongshu", "keyword": keyword, "public_summary": safe_data(card), "usage": "研究问题和搜索意图，不复制文案或素材"}})
                    else:
                        blocked.append(health["detail"])
                except Exception as error:
                    blocked.append(f"小红书研究：{type(error).__name__}")
                finally:
                    await adapter.close()
            candidates = candidates[:count]
            evaluations = {}
            if mode == "live" and candidates:
                ranked = await ModelClient().rank(session, candidates, settings(session))
                evaluations = {item["index"]: item for item in ranked}
            inserted = 0
            for index, item in enumerate(candidates):
                key = digest(text_key(item["title"]))
                if session.scalar(select(Topic).where(Topic.fingerprint == key)):
                    continue
                components = {"heat_trend": 0 if mode == "mock" else 8, "user_need": 16, "original_value": 16, "account_fit": 15, "click_appeal": 7, "save_value": 8, "materials": 4}
                evidence = item.get("evidence", {}) | {"score_components": components, "score_basis": "编辑规则估计；无已验证热度增长时不给趋势满分"}
                evaluation = evaluations.get(index)
                if evaluation:
                    evidence.update(model_evaluation=evaluation, score_basis="Codex CLI 编辑评价，不代表真实热度预测", model=MODEL_NAME, reasoning_effort=REASONING_EFFORT)
                session.add(Topic(title=item["title"], category=item["category"], score=evaluation["score"] if evaluation else sum(components.values()), reasons=evaluation["reasons"] if evaluation else ["符合技术账号定位", "存在可展开的教程或独立分析方向", "热度与增长未取得历史数据，不作趋势断言"], sources=item["sources"], fingerprint=key, mode=mode, evidence=evidence))
                for source in item["sources"]:
                    session.add(Source(title=source["title"], url=source["url"], verified=source["verified"], retrieved_at=source.get("retrieved_at"), credibility="retrieved" if source["verified"] else "synthetic"))
                inserted += 1
            result = {"count": inserted, "requested": count, "shortfall": max(0, count - inserted), "mode": mode, "blocked": blocked, "run_id": run.id}
            finish_run(session, run, result, "BLOCKED" if not inserted and blocked else "COMPLETED")
            return result
        except ModelUnavailable as error:
            result = {"count": 0, "requested": count, "mode": mode, "blocked": [str(error)], "shortfall": count}
            finish_run(session, run, result, "BLOCKED")
            return result
        except Exception as error:
            finish_run(session, run, {"error": type(error).__name__}, "FAILED")
            raise

class ChiefEditorAgent:
    def run(self, session, limit=50):
        """Deterministic Mock planning; live callers must use run_live."""
        run = start_run(session, "Chief Editor", "mock")
        candidates = session.scalars(select(Topic).where(Topic.status == "DISCOVERED", Topic.mode == "mock").order_by(Topic.score.desc(), Topic.created_at).limit(limit)).all()
        for topic in candidates:
            brief = {"title": topic.title, "target_user": "希望搭建可维护 AI 工作流的开发者", "core_view": "围绕具体问题给出步骤、边界与检查方法", "keywords": [topic.title.split("：")[0]], "style": "技术实操教程", "image_needs": "原创封面及三张步骤信息卡", "sources": topic.sources, "evidence": topic.evidence, "forecast": {"type": "编辑估计", "value": None, "reason": "无历史运营样本，不预测流量"}}
            session.add(ContentBrief(topic_id=topic.id, data=brief))
            topic.status = "PLANNED"
        result = {"count": len(candidates), "requested": limit, "mode": "mock", "shortfall": max(0, limit - len(candidates))}
        finish_run(session, run, result)
        return result

    async def run_live(self, session, limit=50):
        config = settings(session)
        run = start_run(session, "Chief Editor", "live")
        candidates = session.scalars(select(Topic).where(Topic.status == "DISCOVERED", Topic.mode == "live").order_by(Topic.score.desc(), Topic.created_at).limit(limit)).all()
        try:
            if not configured():
                raise ModelUnavailable("本机未找到官方 Codex CLI")
            if not candidates:
                raise ModelUnavailable("没有可策划的真实选题，请先运行真实研究")
            inputs = [{"topic_id": topic.id, "title": topic.title, "sources": topic.sources, "evidence": topic.evidence} for topic in candidates]
            plans = await ModelClient().plan(session, inputs, config)
            by_id = {topic.id: topic for topic in candidates}
            for plan in plans:
                topic = by_id[plan["topic_id"]]
                brief = {key: value for key, value in plan.items() if key != "topic_id"}
                brief.update(sources=topic.sources, evidence=topic.evidence, model=MODEL_NAME, reasoning_effort=REASONING_EFFORT,
                             forecast={"type": "编辑估计", "value": None, "reason": "无历史运营样本，不预测流量"})
                session.add(ContentBrief(topic_id=topic.id, data=brief))
                topic.status = "PLANNED"
            result = {"count": len(plans), "requested": limit, "mode": "live", "shortfall": max(0, limit - len(plans))}
            finish_run(session, run, result)
            return result
        except ModelUnavailable as error:
            result = {"count": 0, "requested": limit, "mode": "live", "shortfall": limit, "blocked": [str(error)]}
            finish_run(session, run, result, "BLOCKED")
            return result
        except Exception as error:
            session.rollback()
            finish_run(session, run, {"error": type(error).__name__}, "FAILED")
            raise

class ContentWriterAgent:
    async def run(self, session, count=3, mode="mock"):
        run = start_run(session, "Content Writer", mode)
        if mode == "live" and not configured():
            result = {"count": 0, "requested": count, "shortfall": count, "mode": mode, "article_ids": [], "blocked": ["本机未找到官方 Codex CLI；请安装并登录已有 Codex 账号。"]}
            finish_run(session, run, result, "BLOCKED")
            return result
        briefs = session.scalars(select(ContentBrief).join(Topic, Topic.id == ContentBrief.topic_id).where(ContentBrief.status == "PLANNED", Topic.mode == mode).order_by(ContentBrief.created_at).limit(count)).all()
        created, blocked = [], []
        if not briefs:
            blocked.append("没有可生成的已策划选题，请先研究选题并执行主编策划")
        for brief in briefs:
            topic = session.get(Topic, brief.topic_id)
            if mode == "live" and topic.mode == "mock":
                blocked.append("Mock 选题不能用于真实模型生产，请先运行真实研究")
                continue
            try:
                if mode == "live":
                    data = await ModelClient().write(session, brief.data, settings(session))
                    data["sources"] = brief.data["sources"]
                else:
                    domain = topic.evidence.get("domain", "工作流")
                    task = topic.evidence.get("task", "输入检查")
                    title = f"{domain}的{task}清单"[:20]
                    data = {"title": title, "title_candidates": [title, f"拆解{domain}里的{task}"[:20], f"{task}需要检查哪几项"[:20]],
                            "body": f"【Mock 容量测试样本，禁止真实发布】\n讨论问题：{topic.title}。这篇合成内容用于检验从选题到人工审核的系统链路。\n\n① 明确{domain}场景下{task}的输入。保留原始参数、来源和时间，缺失信息要标记待补充。\n② 为{task}选择一个最小可观察步骤。在{domain}中记录执行前后的状态，把预期结果和实际结果分开。\n③ 模拟{domain}的正常与失败分支：围绕{task}记录触发条件、错误类型和恢复方式；未知结果交给人工核实。\n④ 将{task}结论放回{domain}检查清单，记录版本、审阅人和下一步动作。不能将Mock测试结果当作真实平台表现。\n\n这不是个人体验或案例业绩。AI辅助创作，内容为系统测试合成数据。",
                            "tags": ["AI工作流", "开发测试", domain], "sources": topic.sources,
                            "cards": [{"title": f"{task}输入检查", "body": f"围绕{domain}核对{task}的输入、来源和时间。"}, {"title": f"{domain}状态对照", "body": f"记录{task}执行前后的状态与实际响应。"}, {"title": f"{task}异常恢复", "body": f"{domain}中的未知结果暂停处理，由人工核实。"}], "comment_prompt": f"你的{domain}工作流里，{task}最常遗漏什么？"}
                    session.add(ModelUsage(agent="Content Writer", model="deterministic-mock", mode="mock", cost_usd=0))
                # Playwright's synchronous renderer must run outside the asyncio event loop.
                article = await asyncio.to_thread(make_article, session, data, mode, topic.id)
                brief.status = "GENERATED"
                topic.status = "GENERATED"
                created.append(article.id)
            except Exception as error:
                session.rollback()
                blocked.append(f"{topic.title}: {str(error) if isinstance(error, ModelUnavailable) else type(error).__name__}")
                break
        result = {"count": len(created), "requested": count, "shortfall": max(0, count - len(created)), "mode": mode, "article_ids": created, "blocked": blocked}
        finish_run(session, run, result, "BLOCKED" if blocked else "COMPLETED")
        return result

def demo(session):
    path = ROOT / "fixtures" / "demo_articles.json"
    if not path.exists():
        raise WorkflowError("今日三篇内容资料尚未准备好")
    items = json.loads(path.read_text())
    created = []
    for item in items:
        existing = session.scalar(select(Article).where(Article.mode == "live", or_(Article.fingerprint == digest(text_key(item["title"] + item["body"])), Article.title == item["title"])).order_by((Article.status == "PUBLISHED").desc(), Article.created_at))
        if existing:
            created.append(existing.id)
        else:
            created.append(make_article(session, item, "live").id)
    return {"article_ids": created}

def edit_article(session, article, patch):
    assert_editable(session, article)
    snapshot(session, article)
    regenerate = any(field in patch for field in ("title", "cards", "template"))
    template = patch.get("template", article.media[0].get("template", "minimal") if article.media else "minimal")
    if "media_order" in patch:
        order = patch.pop("media_order")
        current = {m["id"]: m for m in article.media}
        if len(order) != len(current) or set(order) != set(current):
            raise WorkflowError("配图排序必须包含每一张图且不重复")
        article.media = [current[item] for item in order]
    for field in ("title", "body", "tags", "cards"):
        if field in patch:
            setattr(article, field, patch[field])
    article.version += 1
    article.fingerprint = digest(text_key(article.title + article.body))
    invalidate(session, article)
    if regenerate:
        article.status = "GENERATING"
        render(session, article, template)
    quality_review(session, article)
    snapshot(session, article)
    audit(session, "article.edited", article.id, {"version": article.version, "fields": list(patch), "media_regenerated": regenerate})
    session.commit()
    return article

def review_article(session, article, decision, reviewer):
    assert_editable(session, article)
    if not reviewer.strip():
        raise WorkflowError("审阅人不能为空")
    if decision == "approve":
        quality_review(session, article)
        if article.status != "PENDING_REVIEW":
            raise WorkflowError("自动预检未通过，请先修正文案、来源或图片风险")
    invalidate(session, article)
    session.add(Approval(article_id=article.id, version=article.version, reviewer=reviewer, decision=decision, content_hash=content_hash(article)))
    article.status = "APPROVED" if decision == "approve" else "REJECTED"
    audit(session, "article.reviewed", article.id, {"decision": decision, "reviewer": reviewer, "version": article.version})
    session.commit()
    if decision == "approve" and settings(session)["approval_to_queue"]:
        if article.mode == "mock":
            audit(session, "publish.policy_mock_blocked", article.id, {"reason": "Mock 审批不授予真实发布权限"})
            session.commit()
        else:
            queue_approved_article(session, article)
    return article

def authorize(session, article, confirmation, visibility, *, verified_account=None, policy="manual"):
    if article.mode == "mock":
        raise WorkflowError("Mock 合成内容不能获得真实发布授权")
    if article.status != "APPROVED":
        raise WorkflowError("文章必须先经人工审核通过")
    expected = f"授权发布：{article.id}：v{article.version}"
    if policy == "approval_to_queue":
        config = settings(session)
        if not config["approval_to_queue"] or not config["approved_account_id"] or not config["approved_account_verified_at"]:
            raise WorkflowError("审核即发布策略尚未绑定经核实的账号")
        if not verified_account or verified_account.get("id") != config["approved_account_id"]:
            raise WorkflowError("自动授权账号与已启用策略的账号不一致")
    elif confirmation != expected:
        raise WorkflowError("请精确确认：" + expected)
    if visibility not in {"公开可见", "仅自己可见", "仅互关好友可见"}:
        raise WorkflowError("请使用 MCP 支持的中文可见性")
    valid = session.scalar(select(Approval).where(Approval.article_id == article.id, Approval.version == article.version, Approval.valid == True, Approval.decision == "approve"))
    if not valid or valid.content_hash != content_hash(article):
        raise WorkflowError("审批内容版本或图片哈希已变更")
    if not verified_account or not verified_account.get("verified") or not verified_account.get("id"):
        raise WorkflowError("必须通过 MCP 核实当前登录账号后才能授权")
    session.execute(update(PublishAuthorization).where(PublishAuthorization.article_id == article.id).values(valid=False))
    record = PublishAuthorization(article_id=article.id, version=article.version, content_hash=content_hash(article), visibility=visibility, account_id=verified_account["id"], account_name=verified_account.get("name", ""), policy=policy)
    session.add(record)
    audit(session, "publish.authorized", article.id, {"version": article.version, "visibility": visibility, "content_hash": record.content_hash, "account_id": record.account_id, "account_name": record.account_name, "account_verification": "get_my_profile" if policy == "manual" else "verified global approval_to_queue policy", "policy": policy, "authority": "用户显式启用：人工审批当前版本即授权该账号发布" if policy == "approval_to_queue" else "逐篇确认"})
    session.commit()
    return {"id": record.id, "article_id": article.id, "version": article.version, "content_hash": record.content_hash, "visibility": visibility, "account_id": record.account_id, "account_name": record.account_name, "consumed": False}

async def set_approval_policy(session, enabled, adapter_factory=XiaohongshuMcpAdapter):
    if enabled:
        adapter = adapter_factory(settings(session)["mcp_url"])
        try:
            health = await adapter.health()
            if not health.get("connected") or not health.get("logged_in") or "get_my_profile" not in health.get("tools", []):
                raise WorkflowError("启用审核即发布前，必须连接 MCP 并核实已登录账号")
            profile = profile_data(await adapter.call("get_my_profile"))
            binding = profile_baseline(profile, settings(session)["user_id"])
            name = profile.get("userBasicInfo", {}).get("nickname", "")
            save_settings(session, {"approval_to_queue": True, "approved_account_id": binding["owner_id"], "approved_account_name": name, "approved_account_verified_at": now()})
            audit(session, "publish.policy_enabled", "system", {"policy": "approval_to_queue", "account_id": binding["owner_id"], "account_name": name, "authority": "用户显式启用：人工审批当前版本即授权绑定账号发布；无需逐篇输入确认字符串"})
            session.commit()
        finally:
            await adapter.close()
    else:
        save_settings(session, {"approval_to_queue": False, "paused": True})
        authorizations = session.scalars(select(PublishAuthorization).where(PublishAuthorization.policy == "approval_to_queue", PublishAuthorization.consumed == False)).all()
        for authorization in authorizations:
            authorization.valid = False
            queued = session.scalars(select(PublishJob).where(PublishJob.authorization_id == authorization.id, PublishJob.status == "QUEUED")).all()
            for job in queued:
                if not session.scalar(select(PublishAttempt).where(PublishAttempt.job_id == job.id)):
                    job.status = "CANCELLED"
                    job.error = "用户停用审核即发布策略，未提交任务已取消"
                    article = session.get(Article, job.article_id)
                    if article and article.status == "SCHEDULED":
                        article.status = "APPROVED"
        audit(session, "publish.policy_disabled", "system", {"paused": True, "unsubmitted_auto_jobs_cancelled": True})
        session.commit()
    return settings(session)

def queue_approved_article(session, article):
    config = settings(session)
    if not config["approval_to_queue"] or not config["approved_account_id"] or not config["approved_account_verified_at"]:
        raise WorkflowError("请先显式启用并绑定审核即发布策略")
    if article.mode != "live":
        raise WorkflowError("Mock 合成内容不能进入真实发布队列")
    publisher = PublishingAgent()
    key = digest({"article": article.id, "version": article.version, "mode": "live"})
    existing = session.scalar(select(PublishJob).where(PublishJob.idempotency_key == key))
    if existing and existing.status != "CANCELLED":
        return existing
    if article.status != "APPROVED":
        raise WorkflowError("只能将当前经人工批准的版本入队")
    verify_files(article)
    authorize(session, article, None, "公开可见", verified_account={"id": config["approved_account_id"], "name": config["approved_account_name"], "verified": True}, policy="approval_to_queue")
    return publisher.enqueue(session, article, "live", "公开可见")

def enqueue_approved(session, article_ids=None):
    if not settings(session)["approval_to_queue"]:
        raise WorkflowError("审核即发布策略尚未显式启用")
    query = select(Article).where(Article.status.in_(["APPROVED", "SCHEDULED"]))
    if article_ids is not None:
        query = query.where(Article.id.in_(article_ids))
    enqueued, blocked = [], []
    for article in session.scalars(query.order_by(Article.created_at)).all():
        try:
            job = queue_approved_article(session, article)
            if job.status == "QUEUED":
                enqueued.append({"job_id": job.id, "article_id": article.id, "status": job.status})
            else:
                blocked.append({"article_id": article.id, "reason": f"已有发布任务状态为 {job.status}，不会重复提交"})
        except WorkflowError as error:
            blocked.append({"article_id": article.id, "reason": str(error)})
    return {"count": len(enqueued), "enqueued": enqueued, "blocked": blocked}

async def authorize_with_account(session, article, confirmation, visibility, adapter_factory=XiaohongshuMcpAdapter):
    """The remote API cannot supply account proof; it always comes from the current MCP session."""
    if confirmation != f"授权发布：{article.id}：v{article.version}" or article.status != "APPROVED":
        raise WorkflowError("需要先审批当前版本并精确确认授权字符串")
    adapter = adapter_factory(settings(session)["mcp_url"])
    try:
        health = await adapter.health()
        if not health.get("connected") or not health.get("logged_in"):
            raise WorkflowError("授权前必须确认 MCP 已连接且账号已登录")
        if "get_my_profile" not in health.get("tools", []):
            raise WorkflowError("当前 MCP 缺少 get_my_profile，无法核实授权账号")
        profile = profile_data(await adapter.call("get_my_profile"))
        binding = profile_baseline(profile, settings(session)["user_id"])
        name = profile.get("userBasicInfo", {}).get("nickname", "")
        session.refresh(article)  # edits during account lookup invalidate the original confirmation
        return authorize(session, article, confirmation, visibility, verified_account={"id": binding["owner_id"], "name": name, "verified": True})
    finally:
        await adapter.close()

def verify_files(article):
    if not article.media:
        raise WorkflowError("没有可发布图片")
    for media in article.media:
        path = Path(media["path"])
        if not path.is_absolute() or not path.is_file():
            raise WorkflowError("图片绝对路径不存在")
        if hashlib.sha256(path.read_bytes()).hexdigest() != media["sha256"]:
            raise WorkflowError("图片文件已改变，原审批和授权失效")

def profile_data(result):
    data = result_data(result)
    return data.get("data", data)

def profile_baseline(profile, configured_owner=""):
    feeds = profile.get("feeds", [])
    owners = {feed.get("noteCard", {}).get("user", {}).get("userId") for feed in feeds}
    owners.discard(None)
    owners.discard("")
    direct = profile.get("userBasicInfo", {}).get("userId", "")
    owner = direct or (next(iter(owners)) if len(owners) == 1 else "")
    if configured_owner and owner and configured_owner != owner:
        raise WorkflowError("登录账号与设置中的账号 ID 不一致")
    if not owner:
        raise WorkflowError("当前账号主页未提供可确认的账号 ID，请先人工配置 user_id")
    return {"feed_ids": [feed["id"] for feed in feeds if feed.get("id")], "owner_id": owner}

async def independently_verify(adapter, article, attempt):
    baseline = attempt.request.get("baseline", {})
    if not baseline.get("owner_id"):
        return None
    profile = profile_data(await adapter.call("get_my_profile"))
    candidates = [feed for feed in profile.get("feeds", []) if feed.get("id") not in baseline.get("feed_ids", []) and feed.get("noteCard", {}).get("displayTitle") == article.title]
    if len(candidates) != 1:
        return None
    feed = candidates[0]
    note_id, token = feed.get("id"), feed.get("xsecToken", feed.get("xsec_token"))
    if not note_id or not token:
        return None
    result = await adapter.feed_detail(note_id, token)
    note = result.get("data", {}).get("note", result.get("note", {}))
    author = note.get("user", {}).get("userId")
    body_match = bool(article.body) and text_key(article.body) in text_key(note.get("desc", ""))
    images_match = len(note.get("imageList", [])) == len(article.media)
    stamp = note.get("time")
    try:
        epoch = float(stamp) / (1000 if float(stamp) > 1e11 else 1)
        fresh = epoch >= datetime.fromisoformat(attempt.created_at).timestamp() - 120
    except (ValueError, TypeError):
        fresh = False
    if note.get("noteId") == note_id and note.get("title") == article.title and author == baseline["owner_id"] and body_match and images_match and fresh:
        published_at = datetime.fromtimestamp(epoch, ZoneInfo("Asia/Shanghai")).isoformat()
        return {"note_id": note_id, "xsec_token": token, "published_at": published_at, "evidence": {"method": "get_my_profile + get_feed_detail", "new_id": True, "title_matched": True, "body_matched": True, "author_matched": True, "media_count": len(article.media), "published_time_matched": True, "published_at": published_at, "verified_at": now()}}
    return None

def confirm_published(session, job, article, attempt, verification):
    job.status = article.status = "PUBLISHED"
    job.error = None
    attempt.status = "VERIFIED"
    job.response = job.response | {"platform_id": verification["note_id"], "verification": verification["evidence"]}
    session.add(PublishedPost(article_id=article.id, job_id=job.id, platform_id=verification["note_id"], xsec_token=verification["xsec_token"], published_at=verification["published_at"], verification=verification["evidence"]))
    audit(session, "publish.independently_verified", article.id, verification["evidence"])
    session.commit()

class PublishingAgent:
    _lock = asyncio.Lock()

    def __init__(self, adapter_factory=XiaohongshuMcpAdapter):
        self.adapter_factory = adapter_factory

    def resolve_not_submitted(self, session, job, log_line, operator, explanation):
        """Operator reconciliation for the one audited creator-session failure only.

        A missing note or a timeout is never evidence of non-submission.
        The native error is emitted before NewPublishImageAction returns, hence
        before image upload or action.Publish. Preserve the original attempt.
        """
        if self._lock.locked() or not settings(session)["paused"]:
            raise WorkflowError("恢复操作需要发布暂停且没有执行中的任务")
        if job.mode != "live" or job.status != "VERIFY_REQUIRED":
            raise WorkflowError("只能处理待核实的真实任务")
        attempt = session.scalar(select(PublishAttempt).where(PublishAttempt.job_id == job.id))
        if not attempt or attempt.status != "VERIFY_REQUIRED" or "McpError" not in (job.error or ""):
            raise WorkflowError("缺少原始 MCP 失败记录；超时不能按未提交处理")
        expected = f'发布内容失败: title={job.title} 创作者中心登录失效，请重新扫码登录'
        match = re.fullmatch(r'time="([^"]+)" level=error msg="' + re.escape(expected) + r'"', log_line)
        if not match or not operator.strip() or len(explanation.strip()) < 20:
            raise WorkflowError("需要精确平台错误行、操作人和提交前失败的源码说明")
        delta = (datetime.fromisoformat(match[1]) - datetime.fromisoformat(attempt.created_at)).total_seconds()
        log_path = ROOT / ".runtime/logs/mcp.log"
        if not 0 <= delta <= 1200 or not log_path.is_file() or log_line not in log_path.read_text().splitlines():
            raise WorkflowError("错误行必须来自本任务开始后的本地 MCP 日志")
        if session.scalar(select(PublishedPost).where(PublishedPost.article_id == job.article_id)):
            raise WorkflowError("已有发布结果，禁止恢复提交")
        evidence = {"job_id": job.id, "operator": operator, "log": ".runtime/logs/mcp.log", "log_line": log_line,
                    "source": "v2.5.5/a5c8f779: xiaohongshu/creator_session.go:36; publish.go NewPublishImageAction; service.go publishContent",
                    "explanation": explanation, "resolved_at": now(), "classification": "NO_SUBMISSION"}
        attempt.status = job.status = "NO_SUBMISSION"
        attempt.response = (attempt.response or {}) | {"resolution": evidence}
        job.response = (job.response or {}) | {"resolution": evidence}
        job.error = "已核实：创作者会话初始化失败，未上传或提交；等待恢复登录"
        session.get(Article, job.article_id).status = "APPROVED"
        audit(session, "publish.operator_resolved_no_submission", job.id, evidence)
        session.commit()
        return job

    async def retry_pre_submit(self, session, original):
        """One explicit recovery job, using the existing human approval and policy."""
        async with self._lock:
            session.refresh(original)
            if not settings(session)["paused"] or original.status != "NO_SUBMISSION":
                raise WorkflowError("只允许暂停时恢复已证实未提交的任务")
            attempt = session.scalar(select(PublishAttempt).where(PublishAttempt.job_id == original.id))
            if not attempt or attempt.status != "NO_SUBMISSION" or not attempt.response.get("resolution"):
                raise WorkflowError("缺少未提交的审计证据")
            key = digest({"pre_submit_retry_of": original.id, "retry": 1})
            existing = session.scalar(select(PublishJob).where(PublishJob.idempotency_key == key))
            if existing:
                return existing  # never create a second recovery, even after failure
            article = session.get(Article, original.article_id)
            config = settings(session)
            if article.status != "APPROVED" or article.version != original.version or content_hash(article) != original.content_hash:
                raise WorkflowError("原审批内容已变化，禁止恢复原任务")
            approval = session.scalar(select(Approval).where(Approval.article_id == article.id, Approval.version == article.version, Approval.valid == True, Approval.decision == "approve"))
            old_auth = session.get(PublishAuthorization, original.authorization_id)
            if not approval or approval.content_hash != original.content_hash or not old_auth or not old_auth.valid:
                raise WorkflowError("原审批或账号授权失效")
            if not config["approval_to_queue"] or config["approved_account_id"] != old_auth.account_id:
                raise WorkflowError("审批入队策略或绑定账号已变化")
            verify_files(article)
            adapter = self.adapter_factory(config["mcp_url"])
            try:
                profile = profile_data(await adapter.call("get_my_profile"))
                binding = profile_baseline(profile, old_auth.account_id)
                if binding["owner_id"] != old_auth.account_id:
                    raise WorkflowError("当前登录账号不一致")
                if any(f.get("noteCard", {}).get("displayTitle") == article.title for f in profile.get("feeds", [])):
                    raise WorkflowError("主页已有同标题笔记，需核实，禁止重发")
            finally:
                await adapter.close()
            session.expire_all()
            if not settings(session)["approval_to_queue"] or not old_auth.valid or article.status != "APPROVED" or content_hash(article) != original.content_hash or not approval.valid:
                raise WorkflowError("账号核验期间审批或策略发生变化")
            authorize(session, article, None, original.visibility, verified_account={"id": old_auth.account_id, "name": old_auth.account_name, "verified": True}, policy="approval_to_queue")
            auth = session.scalar(select(PublishAuthorization).where(PublishAuthorization.article_id == article.id, PublishAuthorization.valid == True, PublishAuthorization.consumed == False))
            job = PublishJob(article_id=article.id, title=article.title, version=article.version, content_hash=original.content_hash,
                             mode="live", visibility=original.visibility, authorization_id=auth.id, idempotency_key=key,
                             response={"pre_submit_retry_of": original.id, "retry_number": 1})
            article.status = "SCHEDULED"
            session.add(job)
            audit(session, "publish.operator_recovery_queued", original.id, {"retry_number": 1, "version": article.version})
            session.commit()
            return job

    def enqueue(self, session, article, mode, visibility=None):
        if article.status not in {"APPROVED", "SCHEDULED", "PUBLISHED", "VERIFY_REQUIRED"}:
            raise WorkflowError("内容必须先审核通过")
        key = digest({"article": article.id, "version": article.version, "mode": mode})
        existing = session.scalar(select(PublishJob).where(PublishJob.idempotency_key == key))
        if existing and existing.status != "CANCELLED":
            return existing
        if existing and session.scalar(select(PublishAttempt).where(PublishAttempt.job_id == existing.id)):
            raise WorkflowError("已存在提交记录，取消状态也不能重新发布")
        if article.status in {"PUBLISHED", "VERIFY_REQUIRED"}:
            raise WorkflowError("内容已提交或待核实，不允许重新提交")
        verify_files(article)
        approval = session.scalar(select(Approval).where(Approval.article_id == article.id, Approval.version == article.version, Approval.valid == True, Approval.decision == "approve"))
        if not approval or approval.content_hash != content_hash(article):
            raise WorkflowError("缺少有效的当前版本审批")
        authorization = None
        if mode == "live":
            if article.mode == "mock":
                raise WorkflowError("禁止真实发布 Mock 测试内容")
            authorization = session.scalar(select(PublishAuthorization).where(PublishAuthorization.article_id == article.id, PublishAuthorization.version == article.version, PublishAuthorization.valid == True, PublishAuthorization.consumed == False))
            if not authorization or authorization.content_hash != content_hash(article):
                raise WorkflowError("缺少绑定当前内容和图片哈希的单篇执行授权")
            if visibility and authorization.visibility != visibility:
                raise WorkflowError("发布可见性与授权不一致")
            visibility = authorization.visibility
        job = existing or PublishJob(article_id=article.id, title=article.title, version=article.version, content_hash=content_hash(article), mode=mode, visibility=visibility or "公开可见", authorization_id=authorization.id if authorization else None, idempotency_key=key)
        if existing:
            job.status, job.error, job.response = "QUEUED", None, {}
            job.authorization_id = authorization.id if authorization else None
            job.visibility = visibility or "公开可见"
            job.content_hash = content_hash(article)
        session.add(job)
        if mode == "live":
            article.status = "SCHEDULED"
        audit(session, "publish.enqueued", article.id, {"mode": mode, "version": article.version})
        session.commit()
        return job

    async def execute(self, session, job):
        async with self._lock:
            session.refresh(job)
            if job.status != "QUEUED":
                return job
            if settings(session)["paused"]:
                job.error = "全部发布已暂停；任务保留在队列"
                session.commit()
                return job
            article = session.get(Article, job.article_id)
            try:
                verify_files(article)
                if content_hash(article) != job.content_hash or article.version != job.version:
                    raise WorkflowError("队列中的文章版本已过期")
                if job.mode == "mock":
                    job.status = "MOCK_PUBLISHED"
                    job.response = {"mock": True, "platform_effect": False, "message": "模拟发布通过，未调用平台写工具、未消耗授权或真实配额"}
                    session.add(PublishAttempt(job_id=job.id, request={"title": article.title, "mode": "mock"}, response=job.response, status="MOCK_COMPLETED"))
                    audit(session, "publish.mock", article.id)
                    session.commit()
                    return job
                authorization = session.get(PublishAuthorization, job.authorization_id)
                if not authorization or not authorization.valid or authorization.consumed or authorization.content_hash != job.content_hash:
                    raise WorkflowError("单篇执行授权已失效或已使用")
                daily_start = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
                used = session.scalar(select(func.count()).select_from(PublishAttempt).join(PublishJob, PublishJob.id == PublishAttempt.job_id).where(PublishJob.mode == "live", PublishAttempt.created_at >= daily_start, PublishAttempt.status != "NO_SUBMISSION"))
                if used >= settings(session)["daily_limit"]:
                    job.error = "今日真实提交配额已用完；不包括Mock，但未知结果占用配额"
                    session.commit()
                    return job
                adapter = self.adapter_factory(settings(session)["mcp_url"])
                try:
                    health = await adapter.health()
                    if not health["connected"] or not health["logged_in"]:
                        job.error = health["detail"]
                        save_settings(session, {"paused": True})
                        session.commit()
                        return job
                    if settings(session)["paused"]:
                        job.error = "账号检查期间发布已暂停"
                        session.commit()
                        return job
                    if "get_my_profile" not in health.get("tools", []):
                        raise WorkflowError("当前 MCP 不支持独立核实账号主页，暂不提交")
                    profile = profile_data(await adapter.call("get_my_profile"))
                    baseline = profile_baseline(profile, settings(session)["user_id"])
                    # Re-read all gates after browser/network waits. Edits and pause requests may arrive while awaiting them.
                    session.refresh(job)
                    session.refresh(article)
                    session.refresh(authorization)
                    session.expire_all()
                    if settings(session)["paused"] or job.status != "QUEUED":
                        job.error = "提交前发布被暂停或任务状态已改变"
                        session.commit()
                        return job
                    if article.status != "SCHEDULED" or article.version != job.version or content_hash(article) != job.content_hash:
                        raise WorkflowError("账号检查期间文章被编辑，原队列失效")
                    approval = session.scalar(select(Approval).where(Approval.article_id == article.id, Approval.version == article.version, Approval.valid == True, Approval.decision == "approve"))
                    if not approval or approval.content_hash != job.content_hash:
                        raise WorkflowError("提交前当前版本审批失效")
                    if not authorization.valid or authorization.consumed or authorization.content_hash != job.content_hash:
                        raise WorkflowError("提交前单篇授权失效")
                    if not authorization.account_id or baseline["owner_id"] != authorization.account_id:
                        authorization.valid = False
                        save_settings(session, {"paused": True})
                        audit(session, "publish.account_mismatch", article.id, {"authorized_account_id": authorization.account_id, "current_account_id": baseline["owner_id"]})
                        raise WorkflowError("当前登录账号与执行授权绑定的账号不一致；已暂停全部发布并撤销原授权")
                    verify_files(article)
                    used = session.scalar(select(func.count()).select_from(PublishAttempt).join(PublishJob, PublishJob.id == PublishAttempt.job_id).where(PublishJob.mode == "live", PublishAttempt.created_at >= daily_start, PublishAttempt.status != "NO_SUBMISSION"))
                    if used >= settings(session)["daily_limit"]:
                        job.error = "提交前今日真实提交配额已满"
                        session.commit()
                        return job
                    # Transaction persists the single attempt BEFORE a network write. A crash cannot silently retry it.
                    authorization.consumed = True
                    job.status, job.error, article.status = "PUBLISHING", None, "PUBLISHING"
                    attempt = PublishAttempt(job_id=job.id, request={"title": article.title, "content_hash": job.content_hash, "images": [{"path": m["path"], "sha256": m["sha256"]} for m in article.media], "visibility": job.visibility, "baseline": baseline})
                    session.add(attempt)
                    session.commit()
                    response = await adapter.publish(article.title, article.body, [m["path"] for m in article.media], article.tags, job.visibility)
                    result = result_data(response)
                    job.response = safe_data(result)
                    attempt.response = safe_data(result)
                    # Upstream currently returns 发布完成 without a note ID. It is not independently verified.
                    verification = await independently_verify(adapter, article, attempt)
                    if verification:
                        confirm_published(session, job, article, attempt, verification)
                    else:
                        job.status = article.status = "VERIFY_REQUIRED"
                        attempt.status = "VERIFY_REQUIRED"
                        job.error = "平台写调用已返回，但缺少可独立核实的笔记 ID；请在小红书 App 检查，系统禁止自动重试"
                        save_settings(session, {"paused": True})
                    audit(session, "publish.result", article.id, {"status": job.status, "response": job.response})
                    session.commit()
                    return job
                except BaseException as error:
                    if job.status == "PUBLISHING":
                        job.status = article.status = "VERIFY_REQUIRED"
                        job.error = f"平台提交后发生 {type(error).__name__}，结果未知；禁止自动重试"
                        attempt.status = "VERIFY_REQUIRED"
                        save_settings(session, {"paused": True})
                        audit(session, "publish.unknown", article.id, {"error_type": type(error).__name__})
                        session.commit()
                        if isinstance(error, (KeyboardInterrupt, SystemExit, asyncio.CancelledError)):
                            raise
                        return job
                    raise
                finally:
                    await adapter.close()
            except Exception as error:
                job.status = "BLOCKED"
                job.error = str(error)[:400] if isinstance(error, WorkflowError) else type(error).__name__
                session.commit()
                return job

    async def run(self, session):
        run = start_run(session, "Publishing", "live")
        jobs = session.scalars(select(PublishJob).where(PublishJob.status == "QUEUED").order_by(PublishJob.created_at)).all()
        processed = []
        for job in jobs:
            if settings(session)["paused"]:
                break
            await self.execute(session, job)
            processed.append({"id": job.id, "status": job.status})
        result = {"processed": processed, "paused": settings(session)["paused"]}
        finish_run(session, run, result)
        return result

    async def verify(self, session, job):
        """Read-only reconciliation: never calls publish and never creates another attempt."""
        async with self._lock:
            if job.status == "PUBLISHED":
                return job
            if job.mode != "live" or job.status != "VERIFY_REQUIRED":
                raise WorkflowError("只能核实真实提交后状态为 VERIFY_REQUIRED 的任务")
            article = session.get(Article, job.article_id)
            attempt = session.scalar(select(PublishAttempt).where(PublishAttempt.job_id == job.id))
            if not attempt:
                raise WorkflowError("缺少原始提交记录")
            adapter = self.adapter_factory(settings(session)["mcp_url"])
            try:
                verification = await independently_verify(adapter, article, attempt)
                if verification:
                    confirm_published(session, job, article, attempt, verification)
                else:
                    job.error = "只读核实尚未找到与账号、标题、正文、图片数和时间一致的新笔记；保持暂停，禁止重发"
                    session.commit()
                return job
            finally:
                await adapter.close()

def recover(session):
    jobs = session.scalars(select(PublishJob).where(PublishJob.status == "PUBLISHING")).all()
    for job in jobs:
        job.status = "VERIFY_REQUIRED"
        job.error = "上次进程在提交期间中断；请人工核实，禁止自动重试"
        article = session.get(Article, job.article_id)
        if article:
            article.status = "VERIFY_REQUIRED"
        attempt = session.scalar(select(PublishAttempt).where(PublishAttempt.job_id == job.id))
        if attempt:
            attempt.status = "VERIFY_REQUIRED"
        audit(session, "publish.recovered_unknown", job.article_id)
    if jobs:
        save_settings(session, {"paused": True})
    interrupted_articles = session.scalars(select(Article).where(Article.status == "GENERATING")).all()
    for article in interrupted_articles:
        article.status = "FAILED"
        invalidate(session, article)
        audit(session, "article.recovered_incomplete", article.id, {"reason": "进程在图文重绘期间中断，需要重新生成并审核"})
    interrupted = session.scalars(select(AgentRun).where(AgentRun.status == "RUNNING")).all()
    for run in interrupted:
        run.status = "INTERRUPTED"
        run.finished_at = now()
    session.commit()
    return len(jobs)

class AnalyticsGrowthAgent:
    async def collect(self, session):
        run = start_run(session, "Analytics & Growth", "live")
        posts = session.scalars(select(PublishedPost)).all()
        blocked, collected = [], 0
        adapter = XiaohongshuMcpAdapter(settings(session)["mcp_url"])
        try:
            for post in posts:
                if not post.xsec_token:
                    blocked.append(f"笔记 {post.platform_id} 缺少可读取详情的访问参数")
                    continue
                try:
                    data = await adapter.feed_detail(post.platform_id, post.xsec_token)
                    note = data.get("data", {}).get("note", data.get("note", data))
                    try:
                        stamp = float(note.get("time"))
                        platform_at = datetime.fromtimestamp(stamp / (1000 if stamp > 1e11 else 1), ZoneInfo("Asia/Shanghai")).isoformat()
                        post.published_at = platform_at
                        post.verification = post.verification | {"published_at_source": "get_feed_detail.note.time", "platform_published_at": platform_at, "published_at_refreshed_at": now()}
                        session.commit()
                    except (TypeError, ValueError, OverflowError):
                        pass
                    interact = note.get("interactInfo", note.get("interact_info", {}))
                    metrics = {"likes": parse_count(interact.get("likedCount", interact.get("liked_count"))), "saves": parse_count(interact.get("collectedCount", interact.get("collected_count"))), "comments": parse_count(interact.get("commentCount", interact.get("comment_count"))), "shares": parse_count(interact.get("sharedCount", interact.get("shareCount", interact.get("share_count")))), "views": None, "followers": None}
                    if all(value is None for value in metrics.values()):
                        blocked.append(f"笔记 {post.platform_id} 详情未提供可解析指标")
                        continue
                    age = (datetime.now(ZoneInfo("Asia/Shanghai")) - datetime.fromisoformat(post.published_at)).total_seconds() / 3600
                    window = "7d" if age >= 168 else "72h" if age >= 72 else "24h" if age >= 24 else "current"
                    session.add(PostMetricsSnapshot(post_id=post.id, metrics=metrics, age_hours=age, window=window, evidence={"source": "get_feed_detail", "retrieved_at": now()}))
                    collected += 1
                except Exception as error:
                    blocked.append(f"笔记 {post.platform_id}: {type(error).__name__}")
            if not posts:
                blocked.append("尚无独立核实的已发布笔记；真实互动、浏览与曝光暂不可用")
            result = {"collected": collected, "blocked": blocked}
            finish_run(session, run, result, "BLOCKED" if not collected else "COMPLETED")
            return result
        finally:
            await adapter.close()

    def report(self, session):
        date = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
        articles = session.scalars(select(Article).where(Article.created_at >= date)).all()
        approvals = session.scalars(select(Approval).where(Approval.created_at >= date)).all()
        jobs = session.scalars(select(PublishJob).where(PublishJob.created_at >= date)).all()
        experiments = [serialize(e) for e in session.scalars(select(GrowthExperiment)).all()]
        result = {"date": date, "production": {"total": len(articles), "mock": sum(a.mode == "mock" for a in articles), "real_content": sum(a.mode == "live" for a in articles), "target": settings(session)["production_target"]},
            "approvals": {"approved": sum(a.decision == "approve" for a in approvals), "rejected": sum(a.decision == "reject" for a in approvals)},
            "published": sum(job.mode == "live" and job.status == "PUBLISHED" for job in jobs),
            "blocked": [{"article_id": job.article_id, "status": job.status, "reason": job.error} for job in jobs if job.error and job.status not in {"NO_SUBMISSION", "CANCELLED", "PUBLISHED", "MOCK_PUBLISHED"}],
            "insights": ["可比较本次内容方向、开头和配图；当前样本不足以判断增长效果。"],
            "uncertainty": ["Mock 生产容量不证明真实模型质量或平台发布能力。", "质量评分是规则预检，事实与视觉需要人工确认。", "无足够真实运营样本，不做短期归因。", "浏览与曝光未取得真实来源。"],
            "metrics": aggregate_metrics(session), "experiments": experiments,
            "recommendations": ["围绕本次选择的内容方向创作，保留素材依据和具体细节。", "内容审批后按已绑定账号直接进入发布队列，继续核实结果并遵守每日发布额度。"]}
        row = session.scalar(select(DailyReport).where(DailyReport.date == date))
        if row:
            row.data = result
        else:
            session.add(DailyReport(date=date, data=result))
        session.commit()
        return result

def parse_count(value):
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.replace(",", "").isdigit():
        return int(value.replace(",", ""))
    return None  # rounded counts such as 1.2万 cannot be treated as exact metrics

def aggregate_metrics(session):
    latest = {}
    for row in session.scalars(select(PostMetricsSnapshot).order_by(PostMetricsSnapshot.created_at)).all():
        latest[row.post_id] = row.metrics
    result = {}
    for key in ("likes", "saves", "comments", "shares", "views", "followers"):
        values = [m[key] for m in latest.values() if m.get(key) is not None]
        result[key] = sum(values) if values else None
    return result
