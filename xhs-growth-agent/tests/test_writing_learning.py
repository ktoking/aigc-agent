import asyncio
import copy
import json
from datetime import datetime, timedelta

import httpx
import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker

from backend import creation, learning, main, writing_templates as templates, writing_harness
from backend.db import get_db
from backend.models import AgentRun, Approval, AuditLog, Article, PublishJob, StyleUsage, WritingTemplate
from backend.publishing_worker import PublishingWorker
from backend.service import WorkflowError, save_settings
from tests.test_creation import output


def factory(session):
    return sessionmaker(bind=session.get_bind(), expire_on_commit=False)


def feed(id, title='下班后如何休息', likes='1200'):
    return {'id':id, 'xsecToken':'private-test-access', 'noteCard':{'type':'normal', 'displayTitle':title, 'interactInfo':{'likedCount':likes}}}


def learned():
    item=copy.deepcopy(templates.BUILTINS[0])
    item['key']=item.pop('id')
    item['source_ids']=['a','b','c']
    return {'templates':[item], 'harness':harness()}


def harness():
    return {**{key:['围绕本次问题选择具体细节，结合真实素材组织表达。'] for key in writing_harness.RULE_FIELDS},
            'tone_rules':[{'tone':'subjective','rules':['表达个人取舍，不能推广为所有人的答案。']}], 'source_ids':['a','b','c']}


def test_sampling_counts_and_filters():
    assert learning.number('1.2万')==(12000,True)
    assert learning.number('12,300')==(12300,False)
    assert learning.number(None)==(None,False)
    data={'feeds':[feed('a'),feed('b',likes='1.3万'),feed('c','原帖没了存一下'),feed('d','选举结果'),feed('e',likes='499'),feed('f',likes='未知')]}
    assert [s['id'] for s in learning.candidates(data,'生活')]==['b','a']


def test_provenance_and_copy_rejection():
    samples=[{'id':id,'_body':'具体事实用于测试，不能伪装成用户经历。'} for id in ['a','b','c']]
    assert learning.validate_templates(learned(),samples)
    invalid=learned();invalid['templates'][0]['source_ids']=['a','invented']
    with pytest.raises(WorkflowError,match='样本'):learning.validate_templates(invalid,samples)
    invalid=learned();invalid['templates'][0]['outline'][0]='这是一段连续十八字以上的原创句子不能被复制到写法模板中'
    samples[0]['_body']=invalid['templates'][0]['outline'][0]
    with pytest.raises(WorkflowError,match='原文'):learning.validate_templates(invalid,samples)


def test_tone_recommendation_and_manual_selection(session):
    assert templates.resolve_template(session,tones=['natural'])['id']=='personal_view'
    assert templates.resolve_template(session,tones=['subjective'])['id']=='personal_view'
    assert templates.resolve_template(session,tones=['objective'])['id']=='objective_explain'
    assert templates.resolve_template(session,tones=['critical'])['id']=='critical_rule'
    assert templates.resolve_template(session,'light_observation',tones=['subjective'])['id']=='light_observation'
    with pytest.raises(ValueError):templates.resolve_template(session,'missing')


def test_feedback_requires_valid_exact_versions_and_three_decisions(session):
    for i in range(3):
        session.add(StyleUsage(article_id=str(i),article_version=1,template_key='personal_view',template_version=1,tones=['subjective']))
        session.add(Approval(article_id=str(i),version=1,reviewer='test',decision='approve',content_hash='h',valid=i<2))
        session.add(Approval(article_id=str(i),version=2,reviewer='test',decision='reject',content_hash='h'))
    session.commit()
    get=lambda:next(t for t in templates.catalogue(session,['subjective']) if t['id']=='personal_view')
    original=get()
    assert original['feedback']['approved']==2 and original['feedback']['filtered']==0
    assert original['feedback']['observed_likes'] is None
    approval=session.scalar(select(Approval).where(Approval.article_id=='2',Approval.version==1))
    approval.valid=True;session.commit()
    assert get()['recommendation_score']==original['recommendation_score']+1
    assert templates.feedback(session,'personal_view',2)['uses']==0


class SampleAdapter:
    body='休息时消息提醒会打断注意力。可以按事情的紧急程度安排回应时间，并提前约定沟通方式。' * 4
    calls=[]
    def __init__(self,url):pass
    async def call(self,name,args):
        self.calls.append(name)
        if name=='search_feeds':return {'structuredContent':{'feeds':[feed(id) for id in ['a','b','c','d']]}}
        return {'structuredContent':{'data':{'note':{'title':'休息的边界','desc':self.body,'imageList':[{}],'type':'normal','time':datetime.now().timestamp()*1000}}}}
    async def close(self):pass


@pytest.mark.asyncio
async def test_learning_versions_preserve_snapshots_and_no_private_material(session,monkeypatch):
    captured=[]
    async def request(self,db,agent,instruction,payload,schema,**kwargs):
        captured.append(payload);return learned()
    monkeypatch.setattr(learning.ModelClient,'request',request)
    monkeypatch.setattr(learning.writing_harness,'export',lambda snapshot: 'test-only-export')
    for _ in range(2):
        run=AgentRun(name=learning.RUN_NAME,mode='live',result={'keywords':['生活'],'samples':[]})
        session.add(run);session.commit()
        await learning.execute(run.id,factory(session),SampleAdapter)
        session.expire_all()
        assert session.get(AgentRun,run.id).status=='COMPLETED'
    row=session.scalar(select(WritingTemplate))
    assert row.version==2
    logs=session.scalars(select(AuditLog).where(AuditLog.action=='style.learned').order_by(AuditLog.created_at)).all()
    assert [l.data['version'] for l in logs]==[1,2]
    assert all(l.data['template']['outline'] for l in logs)
    stored=json.dumps([l.data for l in logs])+json.dumps(row.data)
    assert 'private-test-access' not in stored and SampleAdapter.body not in stored
    assert captured[0]['samples'][0]['body']==SampleAdapter.body
    assert all(not s['visual_reviewed'] for s in row.data['samples'])
    assert session.scalar(select(func.count(PublishJob.id)))==0
    assert writing_harness.latest(session)['version']==2
    assert writing_harness.resolve(session,['objective'])['tone_rules']==[]


def test_harness_export_and_copy_validation(session,tmp_path):
    samples=[{'id':id,'_body':'真实原文', 'title':'休息的边界','url':'https://example.com/note','likes_display':'1200','keyword':'生活'} for id in ['a','b','c']]
    writing_harness.validate(harness(),samples)
    snapshot=writing_harness.save(session,harness(),samples,'run')
    session.commit()
    path=writing_harness.export(snapshot,tmp_path)
    assert (tmp_path/'v1.json').is_file() and (tmp_path/'v1.md').is_file()
    assert '原文' not in (tmp_path/'current.md').read_text()
    assert path==str(tmp_path/'current.md')
    invalid=harness();invalid['body_rules']=['这是连续十八个字以上的原句应当禁止未经改写直接复制到规则中']
    samples[0]['_body']=invalid['body_rules'][0]
    with pytest.raises(ValueError,match='原文'):writing_harness.validate(invalid,samples)


def test_deep_sampling_requires_known_recent_date():
    assert learning.recent_note(datetime.now().timestamp()*1000)
    assert not learning.recent_note(None)
    assert not learning.recent_note((datetime.now()-timedelta(days=200)).timestamp()*1000)
    assert not learning.recent_note((datetime.now()+timedelta(days=1)).timestamp()*1000)


@pytest.mark.asyncio
async def test_insufficient_bodies_never_call_model(session,monkeypatch):
    class Short(SampleAdapter):body='图片内文字未读取'
    async def forbidden(*args,**kwargs):raise AssertionError('must not call model')
    monkeypatch.setattr(learning.ModelClient,'request',forbidden)
    run=AgentRun(name=learning.RUN_NAME,mode='live',result={'keywords':['生活'],'samples':[]})
    session.add(run);session.commit()
    await learning.execute(run.id,factory(session),Short)
    session.expire_all()
    assert session.get(AgentRun,run.id).status=='BLOCKED'
    assert session.scalar(select(func.count(WritingTemplate.id)))==0


@pytest.mark.asyncio
async def test_generation_freezes_template_version_and_avoids_repeated_openings(session,render_stub,monkeypatch):
    data=copy.deepcopy(templates.BUILTINS[0]);data.pop('id')
    row=WritingTemplate(template_key='learned-personal_view',data=data,version=3)
    session.add(row);session.commit()
    samples=[{'id':id,'_body':'原始研究材料'} for id in ['a','b','c']]
    writing_harness.save(session,harness(),samples,'original');session.commit()
    gate,release=asyncio.Event(),asyncio.Event();briefs=[]
    async def write(self,db,brief,config):
        briefs.append(brief);gate.set();await release.wait();return output()
    monkeypatch.setattr(creation.ModelClient,'write',write)
    task=await creation.start_task(session,'散步',count=2,tones=['subjective'],template_id=row.template_key,session_factory=factory(session))
    await gate.wait()
    row.version=4;row.data={**data,'example':'新模板示例'}
    writing_harness.save(session,{**harness(),'body_rules':['新版本组织规则']},samples,'updated')
    session.commit();release.set()
    await asyncio.gather(*list(creation._tasks));session.expire_all()
    usages=session.scalars(select(StyleUsage)).all()
    assert len(usages)==2 and all(u.template_version==3 for u in usages)
    assert briefs[0]['writing_template']['example']==data['example']
    assert task['harness_version']==1
    assert all(b['writing_harness']['version']==1 for b in briefs)
    assert briefs[0]['writing_harness']['body_rules']==harness()['body_rules']
    assert briefs[1]['previous_openings']==[output()['body'][:120]]
    assert session.scalar(select(func.count(PublishJob.id)))==0
    assert all(a.status in {'PENDING_REVIEW','QUALITY_REJECTED'} for a in session.scalars(select(Article)))


@pytest.mark.asyncio
async def test_reading_holds_queue_analyzing_releases(session,monkeypatch):
    save_settings(session,{'paused':False})
    run=AgentRun(name=learning.RUN_NAME,mode='live',result={'stage':'READING'})
    session.add(run);session.commit()
    worker=PublishingWorker(session_factory=factory(session))
    assert await worker.tick()=='READ_WAIT'
    run.result={'stage':'ANALYZING'};session.commit()
    assert await worker.tick()=='IDLE'


@pytest.mark.asyncio
async def test_learning_api_fast_background_and_recovery(session,monkeypatch):
    gate=asyncio.Event()
    async def execute(run_id,factory):await gate.wait()
    monkeypatch.setattr(learning,'execute',execute)
    main.app.dependency_overrides[get_db]=lambda:session
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app),base_url='http://test') as client:
            response=await asyncio.wait_for(client.post('/api/writing/learn',json={'keywords':['生活']}),.5)
            assert response.status_code==202
            assert (await client.get('/api/writing/learning/latest')).json()['status']=='RUNNING'
            assert (await client.get('/api/writing/templates?tones=subjective')).json()['items'][0]['id']=='personal_view'
        gate.set();await asyncio.gather(*list(learning._tasks))
        learning.recover_learning(session)
        assert learning.latest(session)['status']=='INTERRUPTED'
    finally:
        gate.set();main.app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_completed_cache_avoids_repeat_platform_reads(session,monkeypatch):
    run=AgentRun(name=learning.RUN_NAME,status='COMPLETED',finished_at=learning.now(),result={'keywords':['生活'],'stage':'DONE','harness_version':1})
    session.add(run);session.commit()
    assert (await learning.start(session,['生活']))['id']==run.id
    assert session.scalar(select(func.count(AgentRun.id)))==1


@pytest.mark.asyncio
async def test_deep_sampling_is_bounded_and_balanced(session,monkeypatch):
    calls=[]
    class Many(SampleAdapter):
        async def call(self,name,args):
            calls.append((name,args))
            if name=='search_feeds':
                return {'structuredContent':{'feeds':[feed(f"{args['keyword']}-{i}") for i in range(20)]}}
            return await super().call(name,args)
    async def request(self,db,agent,instruction,payload,schema,**kwargs):
        assert len(payload['samples'])==20
        assert len({s['keyword'] for s in payload['samples']})==4
        result=learned();ids=[s['id'] for s in payload['samples'][:4]]
        result['templates'][0]['source_ids']=ids
        result['harness']['source_ids']=ids
        return result
    monkeypatch.setattr(learning.ModelClient,'request',request)
    monkeypatch.setattr(learning.writing_harness,'export',lambda snapshot:'test-only')
    run=AgentRun(name=learning.RUN_NAME,mode='live',result={'keywords':['生活','消费','休息','职场'],'target_samples':20,'samples':[]})
    session.add(run);session.commit()
    await learning.execute(run.id,factory(session),Many);session.expire_all()
    result=learning.view(session.get(AgentRun,run.id))
    assert result['status']=='COMPLETED' and result['sample_count']==20
    assert len([c for c in calls if c[0]=='get_feed_detail'])==20
    assert result['candidate_count']==40 and result['harness_version']==1


@pytest.mark.asyncio
async def test_keyword_failure_does_not_discard_other_pools(session,monkeypatch):
    class Partial(SampleAdapter):
        async def call(self,name,args):
            if name=='search_feeds' and args['keyword']=='失败领域':raise RuntimeError('private diagnostic')
            return await super().call(name,args)
    async def request(*args,**kwargs):return learned()
    monkeypatch.setattr(learning.ModelClient,'request',request)
    monkeypatch.setattr(learning.writing_harness,'export',lambda snapshot:'test-only')
    run=AgentRun(name=learning.RUN_NAME,mode='live',result={'keywords':['失败领域','生活'],'samples':[]})
    session.add(run);session.commit()
    await learning.execute(run.id,factory(session),Partial);session.expire_all()
    run=session.get(AgentRun,run.id)
    assert run.status=='COMPLETED' and len(run.result['samples'])==4
    assert run.result['search_errors']==[{'keyword':'失败领域','code':'RuntimeError'}]
    assert 'private diagnostic' not in json.dumps(run.result)
