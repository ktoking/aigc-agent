"""当前1.3倍版本的内置生图任务与资产登记。"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, struct, fcntl

R=Path(__file__).resolve().parents[1]
V=R/'production/user-script-v2'
ACTIVE=V/'image-queue-speed1p3.json'

def read(p): return json.loads(p.read_text())
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def plan(n,exclude='',reserve=False):
 q=read(ACTIVE);allq={s['shot_id']:s for s in read(V/'image-queue.json')};out=[]
 active_ids={s['shot_id'] for s in q}
 excluded=set(exclude.split(','))
 for s in q:
  if s['shot_id'] in excluded:continue
  if s.get('generation_status')=='IN_FLIGHT':continue
  if s.get('image_path'):continue
  refs=list(s['reference_paths']);linked=None
  if re.search(r'S\d+[BC]$',s['shot_id']) and not s.get('independent_composition'):
   parent=allq[s['shot_id'][:-1]]
   if not parent.get('image_path') and parent['shot_id'] in active_ids:continue
   if parent.get('image_path') and parent['scene_id']==s['scene_id'] and parent['character_ids']==s['character_ids']:
    linked=str(R/parent['image_path']);refs.insert(0,linked)
  refs=list(dict.fromkeys(refs));roles=[]
  for i,p in enumerate(refs):
   role=('只锁相邻主镜空间、服装、道具颜色材质与数量；本镜生成新动作新构图，不能复制旧图。' if p==linked else
         '仅锁初始无窗白色空厅，无货架库存。' if 'HALL1' in p else
         '只锁该镜头的空间、家具、货架和物资状态，忽略参考中的人物姿势和构图；本镜按指定人物和新事件生成。' if '/frames/' in p else
         '仅锁对应成年角色脸、发型和服装，不继承参考背景与姿势。')
   roles.append(f'参考{i+1}：{role}')
  prompt='\n'.join(roles)+'\n'+(R/s['prompt_path']).read_text()
  prompt+='\n出镜人物严格按本镜事件，不凭空加人。画中没有标题、字幕、水印、漂浮UI；后期另行烧录字幕。单张横屏16:9，真人电影静帧，环境干燥、简洁有序，适度细节，无过锐微纹理。所有人物均为成年人。'
  out.append(dict(id=s['shot_id'],prompt=prompt,prompt_path=s['prompt_path'],refs=refs,take=s.get('next_take') or 1,event=s['unique_event']))
  if len(out)>=n:break
 if reserve:
  ids={x['id'] for x in out}
  for s in q:
   if s['shot_id'] in ids:s['generation_status']='IN_FLIGHT'
  write(ACTIVE,q)
  for s in allq.values():
   if s['shot_id'] in ids:s['generation_status']='IN_FLIGHT'
  write(V/'image-queue.json',list(allq.values()))
 print(json.dumps(out,ensure_ascii=False))

def save(items):
 old=read(V/'image-queue.json');q=read(ACTIVE);assets=read(R/'assets/manifest.json')
 for x in items:
  src=Path(x['source']);aid=x['id'];take=x['take'];dst=R/'episodes'/aid.split('-')[0]/'frames'/f'{aid}-release-take{take:02d}.png'
  current=next(s for s in q if s['shot_id']==aid)
  if current.get('image_path'):
   assert current['image_sha256']==hashlib.sha256(src.read_bytes()).hexdigest(),'镜头已有选图，拒绝重复生成覆盖'
   continue
  dst.parent.mkdir(exist_ok=True);b=src.read_bytes();h=hashlib.sha256(b).hexdigest()
  if dst.exists():assert hashlib.sha256(dst.read_bytes()).hexdigest()==h,'保留已存在版本，不能覆盖不同图片'
  else:shutil.copy2(src,dst)
  dims=list(struct.unpack('>II',b[16:24]));rel=str(dst.relative_to(R))
  req=R/'assets/generation-requests'/f'{aid}-release-take{take:02d}.json'
  write(req,dict(prompt=x['prompt'],referenced_image_paths=x['refs'],generator='built-in image_gen',transparent_background=False,source=str(src)))
  fields=dict(image_path=rel,image_sha256=h,native_dimensions=dims,generation_status='GENERATED_REVIEW_PENDING',visual_review=None)
  for rows in [old,q]:
   for s in rows:
    if s['shot_id']==aid:s.update(fields)
  assets=[a for a in assets if a['asset_id']!=aid]+[dict(asset_id=aid,path=rel,source=str(src),sha256=h,native_dimensions=dims,generator='built-in image_gen',type='event_image',prompt_path=str(req.relative_to(R)),status='GENERATED_VISUAL_REVIEW_PENDING',selected_for_production=False)]
 write(V/'image-queue.json',old);write(ACTIVE,q);write(R/'assets/manifest.json',assets)
 status=read(V/'status.json');status.update(final_shot_images=sum(bool(s.get('image_path')) for s in q),planned_final_shots=len(q))
 status['image_progress_by_episode']={f'EP{i:03d}':{'ready':sum(bool(s.get('image_path')) for s in q if s['episode']==f'EP{i:03d}'),'total':sum(s['episode']==f'EP{i:03d}' for s in q)} for i in range(1,11)}
 write(V/'status.json',status)
 for eid in set(x['id'].split('-')[0] for x in items):
  tp=R/'episodes'/eid/'timeline-speed1p3.json';t=read(tp);byid={s['shot_id']:s for s in q}
  t['shots']=[byid[s['shot_id']] for s in t['shots']];write(tp,t)
 print(json.dumps({'saved':[x['id'] for x in items],'ready':sum(bool(s.get('image_path')) for s in q),'total':len(q)}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['plan','save']);p.add_argument('value');p.add_argument('--exclude',default='');p.add_argument('--reserve',action='store_true');a=p.parse_args()
 if a.action=='plan':
  with (V/'.image-assets.lock').open('w') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX);plan(int(a.value),a.exclude,a.reserve)
 else:
  with (V/'.image-assets.lock').open('w') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX);save(json.loads(a.value))
