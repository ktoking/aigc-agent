import asyncio
import pytest
import httpx
from sqlalchemy import select,func
from backend import creation,main,model_client
from backend.db import get_db
from backend.models import AgentRun,PublishJob,Article
from backend.tones import normalize_tones,tone_prompt
from backend.service import WorkflowError
from tests.test_creation import factory,output,drained
from tests.test_codex_model import fake_cli


def test_empty_selection_defaults_to_natural_and_duplicates_are_removed():
 assert normalize_tones()==['natural']
 assert normalize_tones([])==['natural']
 assert normalize_tones(['objective','subjective','objective'])==['objective','subjective']


@pytest.mark.parametrize('values',[['unknown'],['自然'],'critical',['natural','objective','subjective','critical','sharp'],[None]])
def test_invalid_tones_are_rejected(values):
 with pytest.raises(ValueError):normalize_tones(values)


@pytest.mark.asyncio
async def test_tones_persist_and_reach_every_article_brief_without_publish(session,monkeypatch,render_stub):
 seen=[]
 async def write(_self,_session,brief,_settings):
  seen.append(brief)
  return output('周末休息'+str(len(seen)))
 monkeypatch.setattr(creation.ModelClient,'write',write)
 chosen=['objective','subjective','gentle']
 started=await creation.start_task(session,'休息与工作消息',count=2,tones=chosen,session_factory=factory(session))
 assert started['tones']==chosen
 await drained();session.expire_all()
 result=creation.get_task(session,started['id'])
 assert result['tones']==chosen and result['status']=='COMPLETED'
 assert len(seen)==2 and all(brief['tones']==chosen for brief in seen)
 assert session.get(AgentRun,started['id']).result['tones']==chosen
 assert session.scalar(select(func.count(PublishJob.id)))==0


@pytest.mark.asyncio
async def test_request_passes_tone_combination_in_actual_cli_prompt(session,monkeypatch):
 captured=fake_cli(monkeypatch)
 await model_client.ModelClient().write(session,{'direction':'休息','tones':['objective','subjective','gentle']},{})
 prompt=captured['prompt'].decode()
 assert tone_prompt(['objective','subjective','gentle']) in prompt
 assert '你是一个愤世嫉俗' not in prompt
 assert '抓一个最值得批判' not in prompt
 assert '"tones": ["objective", "subjective", "gentle"]' in prompt


@pytest.mark.asyncio
async def test_tone_http_validation_and_background_contract(session,monkeypatch,render_stub):
 async def write(_self,_session,brief,_settings):
  assert brief['tones']==['objective','humorous']
  return output()
 monkeypatch.setattr(creation.ModelClient,'write',write)
 main.app.dependency_overrides[get_db]=lambda:session
 try:
  async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app),base_url='http://test') as c:
   for tones in [['unknown'],['natural','critical','objective','subjective','sharp']]:
    assert (await c.post('/api/creation/tasks',json={'direction':'休息','tones':tones})).status_code==422
   assert session.scalar(select(func.count(AgentRun.id)))==0
   response=await c.post('/api/creation/tasks',json={'direction':'休息','tones':['objective','humorous']})
   assert response.status_code==202 and response.json()['tones']==['objective','humorous']
   await drained()
   read=await c.get('/api/creation/tasks/'+response.json()['id'])
   assert read.json()['tones']==['objective','humorous'] and read.json()['completed']==1
 finally:main.app.dependency_overrides.clear()


def test_legacy_task_does_not_claim_a_tone_that_was_not_recorded():
 old=AgentRun(name='Content Creation',mode='live',status='COMPLETED',result={'direction':'旧稿','article_ids':[]})
 assert creation.task_view(old)['tones']==[]
