from sqlalchemy import select, func
from backend.models import PublishJob, PublishAuthorization
from backend.service import review_article, edit_article

def test_manual_filter_leaves_review_pool_without_publishing_and_can_be_edited_back(session, article_factory):
    article = article_factory()
    review_article(session, article, 'reject', 'test reviewer')
    assert article.status == 'REJECTED'
    assert session.scalar(select(func.count()).select_from(PublishJob)) == 0
    assert session.scalar(select(func.count()).select_from(PublishAuthorization)) == 0
    edit_article(session, article, {'title': '修改后的草稿标题'})
    assert article.status == 'PENDING_REVIEW' and article.version == 2
