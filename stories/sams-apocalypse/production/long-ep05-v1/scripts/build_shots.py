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
refs={'male':'male-neutral.png','female':'female-neutral.png','raiders':'raiders-neutral.png','truck':'truck-neutral.png','foreman':'foreman-neutral.png','driver':'driver-neutral.png','bridge':'bridge-reference.png','sealed':'warehouse-sealed-reference.png'}
identity={'male':'男主身份只取男参考：约30岁中国男子，青绿针织帽、芥末黄帽衫、深蓝马甲、深灰裤。',
'female':'许棠身份只取女参考：26岁中国女子，低马尾、橘色维修夹克、灰上衣、深灰裤。',
'raiders':'三名外人身份按参考从左到右：A约40岁方脸短寸壮实，浅灰防护服胸前棕色无字补丁；B约32岁瘦高长脸短发，无补丁；C约45岁较矮圆脸短发，无补丁。只画事件点名者，不默认补齐三人。正式室外全部戴好兜帽、护目镜、半面罩，除事件明确允许摘下。',
'driver':'原司机取司机参考，约35岁较窄脸短发，浅灰白防护服左上臂蓝色胶带，无棕补丁；室外戴好兜帽护目镜半面罩，室内可挂颈。',
'foreman':'油库负责人取负责人参考，中年中国男子短发略灰，灰色防护服；室内面罩挂颈，室外防护完整。',
'none':'严格按事件的人数，事件没有人物就零人物零手臂零人影。',
'truck':'车辆参考只锁同一辆浅灰单排驾驶室、白色方形封闭货箱小型厢式货车；不是油罐车皮卡军车，牌照模糊。',
'bridge':'桥参考只锁地点：完整可通小货车的双车道短混凝土桥，低栏杆，右侧铁皮棚。路障状态严格按本镜事件，通路后两辆废轿车移开、收费牌拆下；桥始终没塌。',
'sealed':'场景参考只锁外院空间：旧大卸货洞已完全用整块钢板封闭，侧小门保留且关闭，不恢复卷帘门或破洞。'}
common='Use case: photorealistic-natural. 生成一张全新单幅16:9横向真人电影静帧，用于山姆核灾第五集。不是拼图分镜表，不是旧图裁切。自然可信中国成年人，中等细节，清楚大形，克制电影光。室内有序干净干燥、完整墙面和哑光地面；室外黄尘污染天空但干燥不湿，完整建筑，不画满地垃圾。无字幕标题水印，底部普通场景留给后期字幕。冲突只拍虚构电影事件和结果，不展示战术部署、武器操作、制造或使用教程。不继承演员参考的灰棚背景。'
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
        target=round(bounds[-1]+(end-bounds[-1])/(n-i+1))
        near=[x for x in possible if abs(x-target)<=15 and x-bounds[-1]>=105 and end-x>=(n-i)*105 and (not 120<=(end-start)/n<=180 or (120<=x-bounds[-1]<=180 and 120<=(end-x)/(n-i)<=180))]
        bounds.append(min(near,key=lambda x:abs(x-target)) if near else target)
    bounds.append(end)
    narrative=''.join(text[k-1] for k in ps)
    for i,ei in enumerate(inds):
        cast,event=opts[ei];sid=f'p{len(shots)+1:03d}';a,b=bounds[i:i+2]
        stage='核灾后，山姆核心后仓和地下住处完整，独立机房一直在运行。上集旧大卸货洞已用钢板封死，侧小门与转角后厚内门保留并关闭。外人只在外围，不能进核心后仓、监控房或地下住处；男女主只在封闭内侧活动。地下室没有窗户或直通室外开口。'
        if max(ps)<=73:stage+=' 桥头路障尚未清除，两辆废车挡桥；本集没有新增柴油交付。'
        elif min(ps)>=86:stage+=' 桥头路障已清，两辆废车挪走、收费牌拆除；仍没有新增柴油交付。'
        else:stage+=' 当前依据旁白报告或后来带回录像表现桥头事件；不把男主送到桥头或让油库人员进入核心仓内。'
        keys=cast.split(',') if cast!='both' else ['male','female']
        ident=' '.join(identity[k] for k in keys)
        prompt=common+'\n时序与空间：'+stage+'\n参考职责：'+ident+'\n本镜唯一可见事件：'+event
        args={'prompt':prompt,'transparent_background':False}
        selected=[str((P/'references'/refs[k]).resolve()) for k in keys if k in refs]
        if selected:args['referenced_image_paths']=selected
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
