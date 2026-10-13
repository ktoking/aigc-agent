import hashlib
from pathlib import Path
import pytest
from sqlalchemy.orm import sessionmaker
from backend.db import Base, make_engine, migrate
from backend.models import Article, uid
from backend.service import quality_review

@pytest.fixture(autouse=True)
def isolated_pause_control():
    from backend.control import request_pause
    request_pause(False)
    yield
    request_pause(False)

@pytest.fixture
def session(tmp_path):
    engine = make_engine(f"sqlite:///{tmp_path / 'test.db'}")
    migrate(engine)
    with sessionmaker(bind=engine, expire_on_commit=False)() as value:
        yield value
    engine.dispose()

@pytest.fixture
def render_stub(monkeypatch, tmp_path):
    from backend import visual
    def render(article_id, title, cards, template="minimal"):
        assets = []
        for index in range(4):
            path = tmp_path / f"{article_id}-{index}.png"
            # Pipeline test double; the genuine browser rendering is verified separately.
            path.write_bytes((title + str(index)).encode())
            assets.append({"id": uid(), "url": f"/media/{path.name}", "path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "source": "test fixture original card", "license": "test-owned"})
        return assets
    monkeypatch.setattr(visual, "render_article", render)
    return render

@pytest.fixture
def article_factory(session, render_stub):
    def make(title="MCP验收清单", mode="live"):
        body = f"先核验{title}的来源与权限。" * 15 + "具体方法：检查输入、正常分支、失败恢复和结果回读，保留实际响应。AI辅助创作。"
        article = Article(id=uid(), title=title, title_candidates=[title], body=body, tags=["开发测试"], sources=[{"title": "原始技术文档", "url": "https://example.com/docs", "verified": True}], media=[], cards=[{"title": "操作", "body": "步骤"}], mode=mode, fingerprint=hashlib.sha256(body.encode()).hexdigest())
        article.media = render_stub(article.id, article.title, article.cards)
        session.add(article)
        session.commit()
        quality_review(session, article)
        session.commit()
        return article
    return make
