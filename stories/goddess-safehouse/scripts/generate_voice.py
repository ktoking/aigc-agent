from pathlib import Path
import json,subprocess,hashlib,math,concurrent.futures,threading,time
R=Path(__file__).resolve().parents[1];REPO=R.parents[1];V=R/'production/user-script-v2'
stop=threading.Event();lock=threading.Lock();results=[]
items=[]
for p in sorted((R/'episodes').glob('EP*/voice-plan.json')):
 for c in json.loads(p.read_text()):items.append((p,c))
def work(item):
 p,c=item
 if stop.is_set():return
 aid=c['cue_id'];out=R/'episodes'/p.parent.name/'audio'/f'{aid}.mp3';meta=out.with_suffix('.metadata.json')
 if not out.exists():
  cmd=['python3',str(REPO/'scripts/minimax_tts.py'),'--voice','Chinese_worker_male','--preset','documentary','--emotion','calm','--speed','1.0','--vol','1.0','--pitch','0','--text-file',str(R/c['text_path']),'--output',str(out)]
  r=subprocess.run(cmd,capture_output=True,text=True)
  if r.returncode:
   stop.set();res={'cue_id':aid,'status':'FAILED_NO_AUTO_RETRY','error':r.stderr.strip(),'returncode':r.returncode}
   with lock:results.append(res);print(json.dumps(res,ensure_ascii=False),flush=True)
   return
 m=json.loads(meta.read_text())
 if m['request']['voice_setting']['voice_id']!='Chinese_worker_male':raise ValueError('wrong voice on '+aid)
 r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(out)],capture_output=True,text=True,check=True)
 sec=float(json.loads(r.stdout)['format']['duration'])
 d=subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True,text=True)
 res={'cue_id':aid,'status':'PASS' if d.returncode==0 else 'DECODE_FAILED','audio_path':str(out.relative_to(R)),'actual_duration_seconds':sec,'audio_frames_30fps':math.ceil(sec*30),'audio_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'voice_id':'Chinese_worker_male','human_listening':'NOT_RUN'}
 with lock:
  results.append(res)
  # 一次锁内更新对应剧集，避免并发丢记录。
  cs=json.loads(p.read_text())
  for x in cs:
   if x['cue_id']==aid:x.update(res)
  p.write_text(json.dumps(cs,ensure_ascii=False,indent=2))
  (V/'voice-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
  print(json.dumps({'cue_id':aid,'seconds':sec,'decode':res['status'],'completed_this_run':len(results)},ensure_ascii=False),flush=True)
# 首轮并发触发RPM后改为单请求节流，成功文件不重做；失败请求没有音频不计成功。
last=max((p.stat().st_mtime for p in (R/'episodes').glob('EP*/audio/*.metadata.json')),default=0)
while time.time()<last+65:time.sleep(min(10,last+65-time.time()))
for item in items:
 if stop.is_set():break
 out=R/'episodes'/item[0].parent.name/'audio'/f"{item[1]['cue_id']}.mp3"
 existed=out.exists();started=time.monotonic();work(item)
 if not existed:
  remaining=8-(time.monotonic()-started)
  if remaining>0:time.sleep(remaining)
print(json.dumps({'finished':len(results),'failed':stop.is_set()},ensure_ascii=False),flush=True)
