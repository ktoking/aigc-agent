from sqlalchemy import select, func
from backend.models import Article
from backend.service import demo

def test_demo_reuses_existing_revised_article_instead_of_cloning_old_fixture(session, article_factory, render_stub):
    article = article_factory("Codex跑偏？先把验收写清楚")
    article.body += "用户明确修改后的正文。"
    article.version = 3
    session.commit()
    first = demo(session)
    second = demo(session)
    assert first["article_ids"] == second["article_ids"]
    assert first["article_ids"][0] == article.id
    assert article.version == 3 and article.body.endswith("用户明确修改后的正文。")
    assert session.scalar(select(func.count()).select_from(Article)) == 3
