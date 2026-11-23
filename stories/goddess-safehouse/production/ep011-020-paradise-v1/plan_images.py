from pathlib import Path
import json,math,re,hashlib,fcntl
P=Path(__file__).resolve().parent;R=P.parents[1];FPS=30
lock=(P/'.image.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX)
src=json.loads((P/'episode-source.json').read_text());results={x['cue_id']:x for x in json.loads((P/'voice-results.json').read_text()) if x['status']=='PASS'}
old={x['shot_id']:x for x in json.loads((P/'image-queue.json').read_text())} if (P/'image-queue.json').exists() else {}
overrides=json.loads((P/'image-overrides.json').read_text()) if (P/'image-overrides.json').exists() else {}
extra=json.loads((P/'extra-events.json').read_text()) if (P/'extra-events.json').exists() else {}
refs={k:str((R/'assets/baselines'/v).resolve()) for k,v in {'CHEN':'CHEN-v1.png','XIA':'XIA-v3.png','XU':'XU-v3.png','QIAO':'QIAO-v1.png','WANG':'WANG-v1.png'}.items()}
names={'陈屿':'CHEN','夏凛':'XIA','许知意':'XU','乔星野':'QIAO','王大富':'WANG'}
queue=[];needs=[];summary=[]
for ep in src:
 eid=ep['episode'];D=R/'episodes'/eid
 cues=json.loads((D/'cues.json').read_text())
 if not all(c['cue_id'] in results for c in cues): continue
 pos=0
 for i,c in enumerate(cues):
  a=results[c['cue_id']];gap=3 if i else 0
  c.update(a);c['start_frame']=pos+gap;c['end_frame']=c['start_frame']+math.ceil(a['actual_duration_seconds']*FPS);c['external_gap_before_frames']=gap
  pos=c['end_frame']
 n=max(1,round(pos/150));spans=[];counts={}
 for i in range(n):
  st=pos*i//n;en=pos*(i+1)//n;mid=(st+en)/2
  c=next((c for c in cues if c['start_frame']<=mid<c['end_frame']),min(cues,key=lambda c:abs((c['start_frame']+c['end_frame'])/2-mid)))
  spans.append((st,en,c));counts[c['cue_id']]=counts.get(c['cue_id'],0)+1
 missing=False
 for c in cues:
  ev=c['events']+extra.get(c['cue_id'],[])
  if counts.get(c['cue_id'],0)>len(ev): needs.append({'cue_id':c['cue_id'],'required':counts[c['cue_id']],'events':ev,'text':c['source_text']});missing=True
 if missing:continue
 seen={};shots=[]
 for i,(st,en,c) in enumerate(spans,1):
  cid=c['cue_id'];ev=c['events']+extra.get(cid,[]);k=seen.get(cid,0);seen[cid]=k+1;count=counts[cid]
  idx=round(k*(len(ev)-1)/(count-1)) if count>1 else min(len(ev)-1,int((((st+en)/2-c['start_frame'])/(c['end_frame']-c['start_frame']))*len(ev)))
  event=ev[idx]
  if eid=='EP011' and i==1:event='陈屿在外门内扶稳刚入屋的许知意，夏凛站在门内侧边，画面只呈三位完整穿衣的成年人，不画伤口、血迹或怪物攻击'
  if eid=='EP011' and i==5:event='关闭完好的普通防盗门内侧锁舌与陈屿手中的灯光控制器特写，只有门锁和完整手部，不画怪物或伤口'
  actors=list(dict.fromkeys(names[name] for name in names if name in event))
  if not actors:actors=[] if any(x in event for x in ['手爪','骨甲','金属扶手','怪物轮廓','撬棍堵','收音设备近景','种植区刚播种','门外灯罩','建筑外景','灯熄灭','灰白细长']) else c['character_ids']
  # 无在场女厨师；监视器与照片内人物不能变成同房实体。
  if '二维影像' in event or '屏内' in event:
   actors=[a for a in actors if a in c['character_ids']]
  sid=f'{eid}-S{i:03d}';img=D/'frames'/f'{sid}.png';scene=c['scene']
  if any(x in event for x in ['黑土','耕地','种植区','人工天光','西瓜','新旧连接']):scene='PARADISE' if int(eid[2:])>=19 else scene
  if '诊疗室门' in event:scene='诊疗室'
  if '金属扶手' in event or '灯架下' in event or '建筑外景' in event:scene='门外'
  ov=overrides.get(sid,{})
  event=ov.get('event',event);actors=ov.get('character_ids',actors);scene=ov.get('scene',scene)
  rr=[refs[a] for a in actors if a in refs]
  rr.extend(str((R/p).resolve()) for p in ov.get('extra_refs',[]))
  if scene in ['HOME2','工作角']:rr.append(str((R/'assets/baselines/HOME2-v1.png').resolve()))
  if scene.startswith('PARADISE') or scene=='诊疗室':
   pr=R/'assets/baselines/PARADISE-v1.png'
   if pr.exists():rr.append(str(pr.resolve()))
  txt='\n'.join(c2['source_text'] for c2 in cues if c2['end_frame']>st and c2['start_frame']<en)
  layout='本镜只画下述当前空间，不把相邻空间拼在一起。'
  if scene in ['入口','旧客厅']:
   space='101外层朴素小起居室：暖灰墙、小旧木桌、灰沙发、朝公共楼道的普通防盗门。外门与内部卧室门是两扇不同的门；除接入人的镜头，外门必须闭合。内部卧室门框在侧后方，本镜不能看见折叠空间。没有厨房、货架、耕地或大落地窗。'
  elif scene in ['楼道','门廊','门外','外檐']:
   space='本镜在101屋外的公共楼道/一楼门廊/门檐，冷暗干燥的水泥墙、楼梯扶手、外置院灯；101防盗门必须闭合，不能看见屋内，不出现厨房、沙发、库存或室内女主。'
  elif scene=='QIAO窗内':
   space='仅乔星野被困的二楼201普通房间，朴素窗框、简单书桌、拆开的便携电源；这是她入屋前的住处，没有安全屋厨房、库存和其他主角。'
  elif scene.startswith('卧室'):
   space='折叠空间内一间独立舒适卧室：干净床、木床头柜、小夜灯、暖灰墙，房门原则上闭合；没有厨房、仓储架或其他卧室同框。'
  elif scene.startswith('PARADISE') or scene=='诊疗室':
   space='Lv3折叠空间内部，原厨房前左与满货架前右仅在指定广角时可见；深处宽拱口连接40㎡黑土耕地，人工天光幕、干燥步道与新诊疗室。近景围绕当前事件，不强塞全部设施。新耕地尚未有成熟作物，外部防盗门绝不出现在这一区域。'
  elif scene=='收音特写':
   space='工程工作台局部，仅旧收音设备、控制旋钮、接收模块和桌面，不出现声音中的人物，不强加在场主角。'
  else:
   space='Lv2折叠空间内部，暖色木地板，左侧厨房、右侧整齐满货架、内走廊四卧室；近景只画当前动作，不强塞全部设施。这里没有公共楼道防盗门，没有耕地或诊疗室。'
  clothes={'XIA':'夏凛28岁，藏青修身制服、高腰长裤、短靴','XU':'许知意27岁，完整白大褂、浅蓝合体上衣、浅灰窄裙、裸腿、浅鞋，当前镜头不展示血迹伤口','QIAO':'乔星野24岁，炭灰短外套、米白合体针织上衣、高腰灰黑长裤、短靴','CHEN':'陈屿26岁，深灰夹克、灰T恤、黑裤','WANG':'王大富成年中年男性，酒红色polo衫和深裤'}
  wardrobe='；'.join(clothes[a] for a in actors if a in clothes) or '无主角实体。匿名邻居仅为普通成年男子，深色日常衣服，不长成主角的脸。'
  if eid in ['EP019','EP020'] and 'QIAO' in actors:wardrobe+='；24℃室内乔星野脱短外套，保留米白合体针织上衣。'
  if '卧室' in scene:wardrobe+='睡眠镜头穿完整舒适上衣与长裤，盖薄被，不裸露，不改变身份。'
  beauty='出镜女主自然漂亮、成年身材与合体潮流服装，姿态服务事件。' if any(a in actors for a in ['XIA','XU','QIAO']) else '严格只出现指定人数，不额外添加女主或路人。'
  weather='寒潮期，门外可有薄霜，屋内干燥温暖。' if int(eid[2:])>=19 else '非冬季，屋外常温干燥，不能有雪、冰、冰柱、霜、雨或雾。'
  prompt=f'Use case: photorealistic-natural. 真人写实电影独立静帧，单张横屏16:9，无拼贴。\n本镜唯一新事件：{event}。\n此时实际在场角色ID：{actors}，只画事件指定人数；参考人物图仅锁对应成年脸、发型与服装，不继承背景、姿势或库存。参考环境图仅锁空间、家具、库存状态，不能将其中的人物加入本镜。\n地点：{scene}；时刻：{ep["day"]}。{layout}{space}\n服装连续性：{wardrobe}\n仅按本镜唯一事件组织画面，不将对白转成画中文字\n{beauty}新构图新动作阶段，固定机位感，不能复制参考构图或裁切旧成片。选择最能看清当场动作和新信息的中景、特写或空间景，避免所有图同一远景。\n{weather}暖屋与门外暗处有清楚空间边界。真实自然肤质，清楚轮廓、适度细节、整洁干燥哑光环境；无字幕、标题、logo、水印、文字框或漂浮UI；手机、收音机和监视屏仅抽象光块或必要二维画面，不能出现可读字。无幼童、无裸露、无血腥特写、无多余人，避免过锐、鱼鳞网格、微纹理、湿反光和垃圾。'
  prompt=ov.get('prompt',prompt)
  pp=D/'image-prompts'/f'{sid}.txt'
  frozen=sid in old and (old[sid].get('image_path') or old[sid]['generation_status']=='IN_FLIGHT')
  if not frozen:pp.write_text(prompt+'\n')
  s={'shot_id':sid,'episode':eid,'anchor_cue':cid,'start_frame':st,'end_frame':en,'display_seconds':(en-st)/FPS,'unique_event':event,'scene':scene,'character_ids':actors,'reference_paths':list(dict.fromkeys(rr)),'prompt_path':str(pp.relative_to(R)),'image_path':None,'generation_status':'PLANNED','visual_review':None}
  if sid in old:
   for key in ['image_path','generation_status','visual_review','image_sha256','native_dimensions','request_path','source_path','take']:s[key]=old[sid].get(key,s.get(key))
   if frozen:
    for key in ['unique_event','scene','character_ids','reference_paths']:s[key]=old[sid][key]
  shots.append(s);queue.append(s)
 timeline={'episode':eid,'version':'paradise-v1','fps':FPS,'width':1920,'height':1080,'frames':pos,'duration_seconds':pos/FPS,'cues':cues,'shots':shots,'audio_status':'PASS_GENERATED_DECODED','post_atempo':1.3,'human_full_listening':'NOT_RUN','timing_note':'每cue最终1.3倍WAV实测；镜头按约5秒的整数帧格划分，角色对白可跨同一镜头；字幕与声轨读取同一cue边界。'}
 (D/'timeline-speed1p3.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')
 (D/'shots.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2)+'\n')
 lines=['# '+eid+' 分镜\n','|镜头|秒|对应cue|新事件|','|---|---|---|---|']+[f'|{s["shot_id"]}|{s["display_seconds"]:.2f}|{s["anchor_cue"]}|{s["unique_event"]}|' for s in shots]
 (D/'storyboard.md').write_text('\n'.join(lines)+'\n')
 summary.append({'episode':eid,'seconds':pos/FPS,'shots':len(shots)})
(P/'image-queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n')
(P/'timing-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(P/'needs-events.json').write_text(json.dumps(needs,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'planned':summary,'needs_more_events':needs},ensure_ascii=False,indent=2))
