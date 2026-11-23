from pathlib import Path
import json,math,copy,re
R=Path(__file__).resolve().parents[1];V=R/'production/user-script-v2';qpath=V/'image-queue.json'
queue=json.loads(qpath.read_text());byid={s['shot_id']:s for s in queue};extra=json.loads((V/'extra-events.json').read_text());FPS=30
extra['EP010-C10'].append('陈屿把灯控制器留在手里，夏凛看着他认出提前准备的灯具，隔门救援成功后两人短暂交谈，室内旧客厅，外门仍闭合')
overrides={('EP010-C02',0):('HOME2',['CHEN']),('EP002-C05',0):('SIM',['CHEN']),('EP003-C07',0):('MALL',['MA','CHEN']),('EP004-C09',0):('OLDHOME',['WANG']),('EP004-C13',0):('OLDHOME',['CHEN']),('EP004-C13',1):('WAREHOUSE',['CHEN']),('EP006-C02',0):('PARKOFFICE',['XIA']),('EP008-C02',0):('PHARMACY',['CHEN','CLERK','XU']),('EP010-C10',0):('CORRIDOR',[]),('EP010-C10',1):('OLDHOME',['CHEN','XIA']),('EP010-C15',0):('CORRIDOR',['XU'])}
assets=json.loads((R/'assets/manifest.json').read_text());refs={}
for aid in ['CHEN','WANG','MA','XIA','XU']:
 version='v3' if aid in ['XIA','XU'] else 'v1';p=R/f'assets/baselines/{aid}-{version}.png'
 if p.exists():refs[aid]=str(p)
complete=[]
for vp in sorted((R/'episodes').glob('EP*/voice-plan.json')):
 eid=vp.parent.name;cues=json.loads(vp.read_text());assert all(c['status']=='PASS' for c in cues),eid
 cursor=0;voice=[];timed=[]
 for ci,c in enumerate(cues):
  cid=c['cue_id'];bid=cid.replace('-C','-S');base=byid[bid]
  gap=3 if ci else 0;frames=math.ceil(c['actual_duration_seconds']*FPS);total=frames+gap
  audio_start=cursor+gap;audio_end=audio_start+frames
  voice.append({'cue_id':cid,'text':c['source_text'],'audio_path':c['audio_path'],'audio_sha256':c['audio_sha256'],'actual_duration_seconds':c['actual_duration_seconds'],'start_frame':audio_start,'end_frame':audio_end,'external_gap_before_frames':gap})
  n=math.ceil(total/180) if total>=240 else 1
  assert len(extra.get(cid,[]))>=n-1,('need extra event',cid,n,extra.get(cid))
  parts=[base]
  for k in range(n-1):
   sid=bid+chr(ord('B')+k)
   if sid not in byid:
    s=copy.deepcopy(base);s.update(shot_id=sid,image_path=None,image_sha256=None,generation_status='PLANNED',next_take=None,prior_image_path=None,unique_event=extra[cid][k],visual_review=None)
    scene,ids=overrides.get((cid,k),(base['scene_id'],base['character_ids']));s['scene_id']=scene;s['character_ids']=ids;s['reference_paths']=[refs[a] for a in ids if a in refs]
    if scene in ['HALL1','SIM']:s['reference_paths'].insert(0,str(R/'assets/baselines/HALL1-v1.png'))
    p=R/'episodes'/eid/'image-prompts'/f'{sid}.txt'
    # 正文仍是原句；新增的只是同一段中的另一可见事件。
    desc=';'.join((R/f'assets/characters/{a}/00-character-card.md').read_text().split('\n\n')[1] for a in ids)
    location=(R/f'assets/scenes/{scene}/scene-card.md').read_text().split('\n\n')[1]
    prompt=f'真人写实电影独立静帧，横向16:9，单张全画幅，没有拼贴、字幕、水印或漂浮UI。\n本镜唯一事件：{extra[cid][k]}。\n角色身份：{desc or "本镜不出现主角实体，仅事件指定的物件或远景轮廓"}。\n本镜地点：{location}\n原段落语境（只作理解，不生成画中文字）：{c["source_text"].strip()}\n这是相邻镜头的独立新事件图，不能只裁切旧镜头；使用新构图、当前事件的动作阶段和新信息，镜内保持固定画面。参考人像仅取脸与服装，不继承背景；自然皮肤、适度细节、清楚大形、干燥哑光地墙，背景有秩序，避免过锐、微纹理、脏乱、湿反光。\n手机信息只能在手机玻璃内部用抽象光块表达，没有手机外的气泡、笑脸贴图或字幕。\n'
    if scene in ['HALL1','SIM'] and eid in ['EP001','EP002']:prompt+='当前初始白色空厅无窗、无货架、无纸箱、无床、无厨房，只有本镜明确的试验物件或展示窗；怪物仅在隔离窗外。\n'
    p.write_text(prompt);s['prompt_path']=str(p.relative_to(R));byid[sid]=s;queue.append(s)
   parts.append(byid[sid])
  if cid in ['EP001-C13','EP004-C13'] and n>1:parts=parts[1:]+parts[:1]
  for k,s in enumerate(parts):
   start=cursor+total*k//n;end=cursor+total*(k+1)//n
   s.update(start_frame=start,end_frame=end,timing_status='MEASURED_AUDIO_INTEGER_FRAMES',final_timing_locked=True,display_seconds=(end-start)/FPS,transition_frames=gap if k==0 else 0)
   s['duration_exception_reason']='确认稿该长句群在此可见状态下完整表达；连续声音不截词，单图时长略超主范围' if (end-start)/FPS>6 else ('短揭示/短回应，保持当前事件边界和下一场切换；连续声音完整' if (end-start)/FPS<4 else None)
   timed.append(s)
  cursor+=total
 timeline={'episode':eid,'version':'user-script-v2','fps':FPS,'width':1920,'height':1080,'frames':cursor,'duration_seconds':cursor/FPS,'cues':voice,'shots':timed,'audio_status':'PASS_GENERATED_AND_DECODED','subtitle_files':False,'human_listening':'NOT_RUN','timing_note':'每段音频实测；较长段落多图沿同一语义事件切换，内部图切点均匀预排，正常速度播放时仍需复核。'}
 (R/'episodes'/eid/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2))
 complete.append({'episode':eid,'duration_seconds':cursor/FPS,'frames':cursor,'cues':len(cues),'shots':len(timed),'range_4_6':sum(4<=s['display_seconds']<=6 for s in timed)})
queue.sort(key=lambda s:(s['episode'],s['shot_id']));qpath.write_text(json.dumps(queue,ensure_ascii=False,indent=2))
for eid in set(s['episode'] for s in queue):(R/'episodes'/eid/'shots.json').write_text(json.dumps([s for s in queue if s['episode']==eid],ensure_ascii=False,indent=2))
(V/'timing-summary.json').write_text(json.dumps(complete,ensure_ascii=False,indent=2));print(json.dumps(complete,ensure_ascii=False,indent=2))
