from backend.service import quality_review
from backend import creation
from backend.models import Topic,now
from backend.service import WorkflowError
import pytest


def test_one_cover_passes_quality_but_missing_cover_blocks(session,article_factory):
    a=article_factory()
    a.media=a.media[:1]
    assert quality_review(session,a)['risks'] == []
    assert a.status == 'PENDING_REVIEW'
    a.media=[]
    assert '缺少封面，需要 1 张首图' in quality_review(session,a)['risks']
    assert a.status == 'QUALITY_REJECTED'


@pytest.mark.asyncio
async def test_cached_political_topic_cannot_start_creation(session):
    t=Topic(title='总统大选',fingerprint='political-selection',mode='live',evidence={'source':'hotspot'},sources=[{'verified':True,'retrieved_at':now()}])
    session.add(t);session.commit()
    with pytest.raises(WorkflowError,match='政治'):
        await creation.start_task(session,'评论',topic_ids=[t.id])
