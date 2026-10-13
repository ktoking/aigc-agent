import pytest
from sqlalchemy import select
from backend.models import Article, ArticleVersion, AgentRun
from backend.service import edit_article, recover


def test_failed_render_is_persisted_and_not_left_as_generating(session, article_factory, monkeypatch):
    from backend import visual
    article = article_factory()
    def failure(*_args, **_kwargs):
        raise RuntimeError('renderer failed')
    monkeypatch.setattr(visual, 'render_article', failure)
    with pytest.raises(RuntimeError):
        edit_article(session, article, {'title': '新的标题'})
    session.expire_all()
    assert session.get(Article, article.id).status == 'FAILED'
    assert session.scalar(select(AgentRun).where(AgentRun.name == 'Visual Designer')).status == 'FAILED'
    assert session.scalar(select(ArticleVersion).where(ArticleVersion.article_id == article.id, ArticleVersion.version == 2)) is None


def test_restart_marks_interrupted_graphic_regeneration_as_failed(session, article_factory):
    article = article_factory()
    article.status = 'GENERATING'
    session.commit()
    recover(session)
    assert session.get(Article, article.id).status == 'FAILED'
