from pathlib import Path
import json,sys,hashlib,struct,shutil,fcntl
P=Path(__file__).resolve().parent;R=P.parents[1];Q=P/'image-queue.json'
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
with (P/'.image.lock').open('w') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX);q=json.loads(Q.read_text())
 if sys.argv[1]=='next':
  n=int(sys.argv[2]);selected=[]
  for s in q:
   if s.get('image_path') or s['generation_status']=='IN_FLIGHT':continue
   s['generation_status']='IN_FLIGHT';task={'id':s['shot_id'],'prompt':(R/s['prompt_path']).read_text(),'refs':s['reference_paths'],'take':s.get('take') or 1};selected.append(task)
   submitted=P/'submitted';submitted.mkdir(exist_ok=True);write(submitted/f'{s["shot_id"]}-take{task["take"]:02d}.json',task)
   if len(selected)>=n:break
  write(Q,q);print(json.dumps(selected,ensure_ascii=False))
 elif sys.argv[1]=='save':
  sid=sys.argv[2];src=Path(sys.argv[3]);s=next(x for x in q if x['shot_id']==sid);take=s.get('take') or 1;stem=sid if take==1 else f'{sid}-take{take:02d}';dst=R/'episodes'/s['episode']/'frames'/f'{stem}.png'
  b=src.read_bytes();h=hashlib.sha256(b).hexdigest()
  if dst.exists():assert hashlib.sha256(dst.read_bytes()).hexdigest()==h
  else:shutil.copy2(src,dst)
  rp=P/'image-requests'/f'{stem}.json';rp.parent.mkdir(exist_ok=True)
  sf=P/'submitted'/f'{sid}-take{take:02d}.json';submitted=json.loads(sf.read_text()) if sf.exists() else {'prompt':(R/s['prompt_path']).read_text(),'refs':s['reference_paths']}
  write(rp,{'shot_id':sid,'take':take,'generator':'built-in image_gen','prompt':submitted['prompt'],'referenced_image_paths':submitted['refs'],'source_path':str(src),'transparent_background':False})
  s.update(image_path=str(dst.relative_to(R)),image_sha256=h,native_dimensions=list(struct.unpack('>II',b[16:24])),generation_status='GENERATED_REVIEW_PENDING',source_path=str(src),request_path=str(rp.relative_to(R)))
  write(Q,q)
  tp=R/'episodes'/s['episode']/'timeline-speed1p3.json';t=json.loads(tp.read_text())
  t['shots']=[next((z for z in q if z['shot_id']==x['shot_id']),x) for x in t['shots']];write(tp,t)
  write(P/'image-progress.json',{'ready':sum(bool(x.get('image_path')) for x in q),'planned':len(q),'by_episode':{e:{'ready':sum(bool(x.get('image_path')) for x in q if x['episode']==e),'planned':sum(x['episode']==e for x in q)} for e in sorted(set(x['episode'] for x in q))}})
  print(json.dumps({'saved':sid,'ready':sum(bool(x.get('image_path')) for x in q),'planned':len(q)},ensure_ascii=False))
