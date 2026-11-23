"""Reusable structures and observed feedback, not promises of virality."""
from sqlalchemy import select
from .models import WritingTemplate, StyleUsage, Approval, PublishedPost, PostMetricsSnapshot, PublishJob
from .tones import normalize_tones

BUILTINS = [
 {'id':'personal_view','name':'主观 · 小事到看法','tones':['subjective','natural','gentle'],'outline':['一个具体问题或小场景','我原先怎么看','让我重新考虑的细节或理由','现在更看重什么，停在具体判断上'],'opening':'[具体小事]让我重新想了想[原来的看法]。没有真实经历时，从“我更看重[偏好]”进入。','example':'我更在意下班后能不能真正放下手机，而不只是离开办公室。','ending':'留一个具体偏好或尚未想通的问题，不升华成万能道理。','cover_hint':'标题只点出一个具体念头，别把全文放上图。','avoid':['编造亲历和对话','每段都以“我认为”开头']},
 {'id':'objective_explain','name':'客观 · 一个问题讲清楚','tones':['objective','natural'],'outline':['先指出最容易混淆的地方','讲清已知事实和条件','一个可核对的例子或假设','说明适用边界与未知'],'opening':'[A]和[B]经常被混在一起，但差别在[具体条件]。','example':'价格涨得慢了，和结账时少付钱，是两回事。','ending':'回答开头的问题，保留真正未知的部分。','cover_hint':'突出两件容易混淆的事，不使用夸张结论。','avoid':['假装有实时数字','为了平衡强凑双方观点']},
 {'id':'critical_rule','name':'批判 · 谁在替规则买单','tones':['critical','sharp','subjective'],'outline':['一句明确的不认同','规则造成的具体代价','谁获得方便，谁多承担成本','给出自己的判断和理由'],'opening':'我不接受[具体做法]，因为[谁]得额外承担[具体代价]。','example':'陪人坐一会儿，却必须再买一杯，这个门槛让我不舒服。','ending':'回到具体规则，不把矛盾放大为人身攻击。','cover_hint':'用争议规则作标题，不杜撰内幕。','avoid':['先骂后编证据','把对方动机当已证实事实']},
 {'id':'empathy_detail','name':'共情 · 被忽略的小压力','tones':['empathetic','gentle','subjective'],'outline':['日常处境里一个不起眼的细节','这个细节为什么让人累','把压力说具体','留一个能够落地的小选择'],'opening':'有时候让人累的，不是[大事]，而是[具体细节]。','example':'工作群又亮了。还没看见消息，休息的心情已经被打断。','ending':'给读者一个选择，不替所有人总结感受。','cover_hint':'少量文字，留白，突出一个生活细节。','avoid':['伪造读者普遍遭遇','鸡汤式拥抱和泛泛安慰']},
 {'id':'light_observation','name':'幽默 · 一点生活反差','tones':['humorous','natural','subjective'],'outline':['真实或明确假设的反差','一句贴切轻吐槽','补一个有用的观察','轻轻收住'],'opening':'[一个承诺]听起来很美，到了[具体场景]却变成[反差]。','example':'本来只是回一条消息，回过神来，半小时休息已经替群聊加班了。','ending':'停在反差本身，不加“你怎么看”或硬求互动。','cover_hint':'短标题和一句反差，不堆表情包。','avoid':['硬塞流行梗','拿事故和伤害取乐']},
]


def compatible_tones(key, tones):
    base=next(t for t in BUILTINS if t['id']==key.removeprefix('learned-'))
    return list(dict.fromkeys([base['tones'][0],*tones]))


def feedback(session,key,version=None):
    query=select(StyleUsage).where(StyleUsage.template_key==key)
    if version is not None:query=query.where(StyleUsage.template_version==version)
    uses=session.scalars(query).all()
    approved=rejected=0;post_ids=[]
    for use in uses:
        decisions=session.scalars(select(Approval).where(Approval.article_id==use.article_id,Approval.version==use.article_version,Approval.valid==True)).all()
        if decisions:
            decision=max(decisions,key=lambda d:d.created_at).decision
            approved+=decision=='approve';rejected+=decision=='reject'
        post=session.scalar(select(PublishedPost).join(PublishJob,PublishJob.id==PublishedPost.job_id).where(PublishedPost.article_id==use.article_id,PublishJob.version==use.article_version))
        if post:post_ids.append(post.id)
    observed=[]
    for pid in post_ids:
        snap=session.scalar(select(PostMetricsSnapshot).where(PostMetricsSnapshot.post_id==pid).order_by(PostMetricsSnapshot.created_at.desc()))
        if snap and snap.metrics.get('likes') is not None:observed.append(snap.metrics['likes'])
    return {'uses':len(uses),'approved':approved,'filtered':rejected,'published':len(post_ids),'observed_like_posts':len(observed),'observed_likes':sum(observed) if observed else None}


def catalogue(session,tones=None):
    chosen=normalize_tones(tones)
    items=[{**t,'version':1,'origin':'builtin','sample_count':0} for t in BUILTINS]
    for row in session.scalars(select(WritingTemplate).where(WritingTemplate.status=='ACTIVE')):
        items.append({**row.data,'tones':compatible_tones(row.template_key,row.data['tones']),'id':row.template_key,'version':row.version,'origin':'learned'})
    for item in items:
        f=feedback(session,item['id'],item['version']);item['feedback']=f
        matched=len((set(chosen)-{'natural'}) & set(item['tones']))
        # Reviews steer recommendations only after three observed decisions;
        # missing reach data never becomes a fabricated engagement rate.
        reviews=f['approved']+f['filtered']
        adjustment=(f['approved']-f['filtered'])/reviews if reviews>=3 else 0
        primary=item['tones'][0] in chosen
        base=item['id'].removeprefix('learned-')
        neutral_bonus=(2 if base=='personal_view' else 1 if base=='objective_explain' else 0) if set(chosen)=={'natural'} else 0
        item['recommendation_score']=matched*10+primary*2+('natural' in item['tones'])+neutral_bonus+adjustment+(0.5 if item['origin']=='learned' else 0)
    return sorted(items,key=lambda t:(-t['recommendation_score'],t['id']))


def resolve_template(session,template_id='auto',tones=None,direction=''):
    items=catalogue(session,tones)
    if template_id!='auto':
        item=next((t for t in items if t['id']==template_id),None)
        if not item:raise ValueError('写法模板不存在，请重新选择')
        return item
    return items[0]


def record_usage(session,article_id,version,template,tones):
    session.add(StyleUsage(article_id=article_id,article_version=version,template_key=template['id'],template_version=template['version'],tones=normalize_tones(tones)))
    session.commit()
