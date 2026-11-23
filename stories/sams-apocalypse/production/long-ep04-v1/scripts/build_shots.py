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
refs={'male':['male-neutral.png'],'female':['female-neutral.png'],'both':['male-neutral.png','female-neutral.png'],'raiders':['raiders-neutral.png'],'none':[]}
identity={'male':'只出现参考同一男主，约30岁中国男子，青绿针织帽、芥末黄帽衫、深蓝马甲、深灰裤。',
'female':'只出现参考同一许棠，26岁中国女子，低马尾、橘色维修夹克、灰上衣、深灰工装裤。',
'both':'实体人物只出现男女主两人。参考1锁男主脸和青绿帽黄帽衫深蓝马甲；参考2锁许棠脸和低马尾橘色维修夹克。不继承灰背景。',
'raiders':'参考只取本事件指定的新强盗身份，不复制灰背景：A左一土黄夹克清瘦男；B左二深蓝外套高个男；C左三灰棒球帽黑马甲窄脸男；D右一棕衣壮实男。只画事件点名的人，其余人不补入，绝不进入核心后仓或主角住处。',
'none':'不添加男女主。只有事件明确要求的外围工人、押运人员或屏幕人物才能出现。'}
common='Use case: photorealistic-natural / identity-preserve. 为山姆核灾后第四集绘制一张全新单幅横向16:9真人电影静帧，不是拼图、分镜表、旧图裁切或动画。自然真实中国成年人，中等细节，清晰大形、克制电影光。室内货物有序、干净干燥、哑光，不画泥污积水湿反光、不堆微纹理。室外是黄尘污染的郊区物流园，干燥没有雨，不画魔法绿辐射。无字幕标题水印边框。画面下方保持普通干净场景供后期字幕。危险冲突仅表现虚构事件结果，绝不画燃烧瓶制作、原料、引线、门触发装置结构、机关布设示意、武器装填或操作教学。'
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
        stage='核爆后的几周，后仓和地下住处完整可用。空间：室外院子→空收货亭（朝院子的大卷帘门，侧面小门）→转角→关闭厚内门→后仓。外来者不能越过厚内门。'
        if max(ps)<=26:stage+=' 当前外大卷帘门完整关闭，没有破洞、没有开口、没有向内掀开，厚内门也始终关闭；即使摄像头受损，也不能提前画破大门。'
        elif max(ps)<=37:stage+=' 当前外大卷帘门按事件刚被撬开，出现局部变形，厚内门始终未开；不显示机关结构。'
        elif min(ps)>=76:stage+=' 当前修复阶段：按事件进度旧大卷帘门拆下、原大门洞用钢板封住；侧小门和转角后厚内门保留，不把封口画成仍可开的卷帘门。'
        else:stage+=' 当前袭击后修复准备阶段，旧大外门损坏，厚内门保持完好，后仓货没被抢。'
        if cast in ['male','female','both']:stage+=' 男女主只在封闭后仓、监控房或地下内侧活动，人物看任务对象不摆拍。地下室没有窗户、没有直通室外的敞开门洞。'
        ident=identity[cast]
        prompt=common+'\n时序与空间：'+stage+'\n'+ident+'\n本镜唯一可见事件：'+event
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
