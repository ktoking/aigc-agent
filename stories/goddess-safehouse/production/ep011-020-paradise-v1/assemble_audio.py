from pathlib import Path
import json,array,wave,subprocess,hashlib,math
P=Path(__file__).resolve().parent;R=P.parents[1];SR=48000;FPS=30
dest=R/'delivery/后10集_世外桃源_剧本图片多角色配音';dest.mkdir(parents=True,exist_ok=True)
out=[];total=0
for i in range(11,21):
 eid=f'EP{i:03d}';D=R/'episodes'/eid;tp=D/'timeline-speed1p3.json'
 if not tp.exists():continue
 t=json.loads(tp.read_text());pcm=array.array('h',[0])*(t['frames']*(SR//FPS))
 for c in t['cues']:
  with wave.open(str(R/c['audio_path']),'rb') as w:
   assert (w.getnchannels(),w.getsampwidth(),w.getframerate())==(1,2,SR)
   a=array.array('h');a.frombytes(w.readframes(w.getnframes()))
  start=c['start_frame']*(SR//FPS);space=(c['end_frame']-c['start_frame'])*(SR//FPS)
  assert len(a)<=space,(c['cue_id'],len(a),space)
  pcm[start:start+len(a)]=a
 f=D/'output'/f'{eid}_多角色_1.3倍.wav'
 with wave.open(str(f),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
 peak=max(abs(x) for x in pcm);clipped=sum(abs(x)>=32767 for x in pcm);assert clipped==0,(eid,clipped)
 mp3=dest/f'{eid}_多角色_1.3倍.mp3'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-c:a','libmp3lame','-b:a','192k',str(mp3)],check=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(mp3),'-f','null','-'],capture_output=True,check=True)
 item={'episode':eid,'duration_seconds':t['duration_seconds'],'frames':t['frames'],'cue_count':len(t['cues']),'clipped_samples':clipped,'peak_pcm16':peak,'wav_path':str(f.relative_to(R)),'mp3_path':str(mp3.relative_to(R)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'decode':'PASS','human_listening':'NOT_RUN'}
 out.append(item);total+=t['duration_seconds']
 print(eid,round(t['duration_seconds'],3),'decoded',flush=True)
(P/'audio-master-summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
# 四个固定女声使用相同文本，统一后期1.3倍；顺序在文件名与清单列明。
pieces=[]
for role in ['XIA','XU','QIAO','GU']:
 f=P/'voice-tests'/f'{role}.mp3'
 raw=subprocess.run(['ffmpeg','-v','error','-i',str(f),'-af','atempo=1.3','-ar',str(SR),'-ac','1','-f','s16le','-'],capture_output=True,check=True).stdout
 pieces.append(raw);pieces.append(b'\x00\x00'*(SR//2))
reel=dest/'女声试听_夏凛_许知意_乔星野_顾南枝_1.3倍.wav'
with wave.open(str(reel),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(b''.join(pieces))
print('episodes',len(out),'total_seconds',round(total,3))
