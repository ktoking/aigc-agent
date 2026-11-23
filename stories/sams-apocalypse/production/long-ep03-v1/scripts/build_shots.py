from pathlib import Path
import json, math

P=Path(__file__).resolve().parents[1]
plan=json.loads((P/'voice-plan.json').read_text())
events=json.loads((P/'scene-events.json').read_text())
text=(P/'narration.txt').read_text().strip().split('\n\n')
cursor=0;cues=[]
for i,c in enumerate(plan):
    meta=P/'audio/final'/(c['id']+'.json')
    if not meta.exists():break
    if i:cursor+=3
    frames=json.loads(meta.read_text())['frames']
    cues.append(dict(**c,start_frame=cursor,end_frame_exclusive=cursor+frames))
    cursor+=frames
lookup={c['id']:c for c in cues};shots=[];jobs=[]
refs={'male':['male-neutral.png'],'female':['female-neutral.png'],
      'both':['male-neutral.png','female-neutral.png'],'outsiders':['outsiders-identity.png'],'none':[]}
identity={'male':'只出现男主：参考演员同一约30岁中国男子，青绿针织帽、芥末黄帽衫、深蓝马甲、深灰裤。',
          'female':'只出现许棠：参考演员同一26岁中国女子，低马尾、橘色维修外套、灰上衣、深灰工装裤。',
          'both':'室内实体人物只出现男女主两人：男主同一青绿帽黄帽衫深蓝马甲男子；许棠同一低马尾橘色维修夹克女子。参考只取脸、发型与衣服，不继承灰色背景。',
          'outsiders':'参考群像只取所点名的外部人物身份：灰夹克方脸中年男子为周强，黑夹克短寸男子为黑夹克，米白外套眼镜女子为林岚，白发老人为父亲；只画本事件指定的人，不复制其余路人。他们绝不进入主角室内。',
          'none':'不出现男女主，也不要添加无关人物；只有事件明确要求的送油人员才可出现。'}
common='Use case: photorealistic-natural / identity-preserve. 为山姆核灾后第一人称叙事视频新绘一张单幅横向16:9真人电影静帧，不是拼图、分镜表或旧图裁切。主体清楚、真实中国成人比例、自然皮肤、克制电影光、中等细节。室内物资有序且干燥，墙地哑光，不加泥污、积水、湿反光或满屏微纹理。只有台词需要的受损前场才有局部碎玻璃与掉落灯架；核后室外必须是昏黄天空、干燥尘土污染，不画雨景。没有字幕、标题、水印、边框、科幻界面或魔法绿辐射。底部正常画面留给后期字幕。'
for key,opts in events.items():
    ps=[int(x) for x in key.split('-')]
    if len(ps)==2:ps=list(range(ps[0],ps[1]+1))
    pcs=[c for c in plan if c['paragraph'] in ps]
    if not all(c['id'] in lookup for c in pcs):break
    cs=[lookup[c['id']] for c in pcs]
    start=cs[0]['start_frame'];end=cs[-1]['end_frame_exclusive']+(0 if pcs[-1]['id']==plan[-1]['id'] else 3)
    duration=(end-start)/30
    n=min(range(1,len(opts)+1),key=lambda n:abs(duration/n-5)+max(0,4-duration/n)*5+max(0,duration/n-6)*5)
    inds=[round(i*(len(opts)-1)/(n-1)) for i in range(n)] if n>1 else [0]
    bounds=[start]
    possible=[c['start_frame'] for c in cs[1:]]
    for i in range(1,n):
        target=round(start+(end-start)*i/n)
        near=[x for x in possible if abs(x-target)<=15 and x-bounds[-1]>=105 and end-x>=(n-i)*105 and (not 120<=(end-start)/n<=180 or (120<=x-bounds[-1]<=180 and 120<=(end-x)/(n-i)<=180))]
        bounds.append(min(near,key=lambda x:abs(x-target)) if near else target)
    bounds.append(end)
    narrative=''.join(text[k-1] for k in ps)
    for i,ei in enumerate(inds):
        cast,event=opts[ei];sid=f'p{len(shots)+1:03d}';a,b=bounds[i:i+2]
        stage=('核爆尚未发生，停电深夜。室外也是黑夜，仅应急灯与路灯照明；绝不出现核后黄天、白昼阳光或城市已毁。门外只通向内部走廊，不能直通室外。' if max(ps)<=4 else '核冲击发生时，地下楼梯只受白色闪光与少量顶灰影响，不是户外火球。' if ps==[5] else '核爆后，地下与封闭后仓仍完整，光线来自应急照明。按本事件地点选择：室外是黄色尘土污染，室内保持有序干燥。')
        ident=identity[cast]
        if cast=='outsiders':
            ident=('参考群像只取黑夹克短寸男子与灰夹克周强的身份。只画这两人，且两人只能出现在监控画面内部。' if '周强' in event else '参考群像只取米白外套眼镜女子林岚和白发父亲的身份。只画这两人，且两人只能出现在监控画面内部。')
        if any(w in event for w in ['地下','避难','门内','休息间']):
            stage+=' 当前是没有窗户的地下室或封闭内部房间，没有直通室外的门洞，没有任何窗外黄天；室外信息只能出现在监控屏中。'
        if cast in ['male','female','both']:stage+=' 人物看向任务对象，不看镜头，不摆拍。'
        prompt=common+'\n时序与空间：'+stage+'\n'+ident+'\n本镜唯一可见事件：'+event
        if cast=='outsiders':prompt+='\n整张图只以一台显示器作主体，画面只显示唯一一路监控，只有指定的两人出现在其中。屏幕外完全没有人、手或身体，不画第二路屏幕，不把其他旁白事件拼进来。'
        args={'prompt':prompt,'transparent_background':False}
        if refs[cast]:args['referenced_image_paths']=[str((P/'references'/x).resolve()) for x in refs[cast]]
        overlap=[c['id'] for c in cs if c['start_frame']<b and c['end_frame_exclusive']>a]
        boundary_is_gap=a==0 or a in [c['start_frame'] for c in cues]
        row=dict(id=sid,asset='assets/'+sid+'.png',start_frame=a,end_frame_exclusive=b,duration_frames=b-a,seconds=(b-a)/30,paragraphs=ps,cue_ids=overlap,cast=cast,event=event,prompt_file='prompts/'+sid+'.json',transition_location='cue_gap' if boundary_is_gap else 'within_continuous_speech_no_extra_wait',duration_exception=None if 4<=(b-a)/30<=6 else 'Complete short paragraph or available narrative event; no padding added.')
        shots.append(row);jobs.append(dict(id=sid,args=args,event=event))
        (P/'prompts'/(sid+'.json')).write_text(json.dumps(args,ensure_ascii=False,indent=2))
(P/'shot-plan.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
(P/'image-jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2))
if len(cues)==len(plan) and (P/'timeline.json').exists():
    t=json.loads((P/'timeline.json').read_text());t['shots']=shots
    assert shots[0]['start_frame']==0 and shots[-1]['end_frame_exclusive']==t['frame_count']
    assert all(x['end_frame_exclusive']==y['start_frame'] for x,y in zip(shots,shots[1:]))
    (P/'timeline.json').write_text(json.dumps(t,ensure_ascii=False,indent=2))
print(json.dumps(dict(measured_cues=len(cues),total_cues=len(plan),planned_shots=len(shots),planned_seconds=shots[-1]['end_frame_exclusive']/30 if shots else 0,complete=len(cues)==len(plan))))
