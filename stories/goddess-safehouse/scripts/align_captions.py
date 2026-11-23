"""ASR仅提供时间，字幕文字逐字取自确认稿；在1.3倍实际音轨上对齐。"""
from pathlib import Path
import argparse, difflib, hashlib, json, math, re, unicodedata, subprocess
import numpy as np
from faster_whisper import WhisperModel
from opencc import OpenCC

R=Path(__file__).resolve().parents[1]
FPS=30
CC=OpenCC('t2s')

def norm(c):
 c=CC.convert(unicodedata.normalize('NFKC',c))
 return c.lower() if any(x.isalnum() for x in c) else ''

def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def display(text):
 return re.sub(r'\s+',' ',''.join(' ' if unicodedata.category(c).startswith('P') else c for c in text)).strip()

def split(text):
 parts=re.findall(r'[^，。！？；、\n]+[，。！？；、]*',text)
 out=[]
 for p in parts:
  while len(p)>18:
   out.append(p[:16]);p=p[16:]
  if p:out.append(p)
 # 过短意群接到前一条，保留原句全部标点，不把字幕变成残缺文字。
 packed=[]
 for p in out:
  if packed and len(p)<=5 and len(packed[-1])+len(p)<=18:packed[-1]+=p
  else:packed.append(p)
 assert ''.join(packed)==text.strip().replace('\n','')
 return packed

def stamp(frame):
 ms=round(frame*1000/FPS);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'

def episode(model,eid):
 d=R/'episodes'/eid;t=json.loads((d/'timeline-speed1p3.json').read_text());audio=R/t['audio_master_path'];out=d/'captions';out.mkdir(exist_ok=True)
 ap=out/'asr-speed1p3.json';key=hashlib.sha256(audio.read_bytes()).hexdigest()
 old=json.loads(ap.read_text()) if ap.exists() else {}
 if old.get('audio_sha256')==key:words=old['words']
 else:
  raw=subprocess.run(['ffmpeg','-v','error','-i',str(audio),'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True,check=True).stdout
  waveform=np.frombuffer(raw,dtype=np.float32)
  segments,info=model.transcribe(waveform,language='zh',beam_size=3,word_timestamps=True,
   condition_on_previous_text=False,vad_filter=False,
   initial_prompt='陈屿、王大富、夏凛、许知意、梧桐里、方舟安全屋、血月、毛肚、物资点、安心值。')
  words=[]
  for s in segments:
   for w in s.words or []:words.append(dict(word=w.word,start=w.start,end=w.end,probability=w.probability))
  save(ap,dict(audio_sha256=key,model='faster-whisper-small-local-int8',language='zh',words=words))
 captions=[];quality=[]
 for cue in t['cues']:
  text=cue['text'].strip().replace('\n','');clean='';source_indices=[]
  for i,c in enumerate(text):
   n=norm(c)
   if n:clean+=n;source_indices.append(i)
  asr='';times=[]
  for w in words:
   if w['end']<cue['start_frame']/FPS or w['start']>=cue['end_frame']/FPS:continue
   n=''.join(norm(c) for c in w['word'])
   for k,c in enumerate(n):
    asr+=c;times.append((w['start']+(w['end']-w['start'])*k/max(1,len(n)),w['start']+(w['end']-w['start'])*(k+1)/max(1,len(n))))
  matcher=difflib.SequenceMatcher(None,clean,asr,autojunk=False);aligned={}
  for a,b,n in matcher.get_matching_blocks():
   for k in range(n):aligned[a+k]=times[b+k]
  ratio=len(aligned)/max(1,len(clean));quality.append(dict(cue_id=cue['cue_id'],matched_characters=len(aligned),source_characters=len(clean),coverage=ratio,source_text=text,recognized_text=asr))
  assert ratio>=.55,(eid,cue['cue_id'],'ASR alignment too uncertain',ratio)
  # 未匹配字只在相邻已匹配字间插值；实际句群边界始终来自实测音频。
  starts=[]
  for i in range(len(clean)):
   if i in aligned:starts.append(aligned[i][0]);continue
   left=max((k for k in aligned if k<i),default=-1);right=min((k for k in aligned if k>i),default=len(clean))
   lt=aligned[left][1] if left>=0 else cue['start_frame']/FPS
   rt=aligned[right][0] if right<len(clean) else cue['end_frame']/FPS
   starts.append(lt+(rt-lt)*(i-left)/(right-left))
  for i in range(1,len(starts)):starts[i]=max(starts[i],starts[i-1])
  offset=0;parts=split(text);local=[]
  for p in parts:
   first=next((j for j,idx in enumerate(source_indices) if idx>=offset),len(starts)-1)
   sf=max(cue['start_frame'],min(cue['end_frame']-1,math.floor(starts[first]*FPS)-1))
   local.append(dict(text=p,display_text=display(p),start_frame=sf,cue_id=cue['cue_id'],source_start_char=offset,source_end_char=offset+len(p)))
   offset+=len(p)
  for i,x in enumerate(local):
   x['end_frame']=local[i+1]['start_frame'] if i+1<len(local) else cue['end_frame']
   assert x['end_frame']>x['start_frame'],(eid,x)
   assert x['end_frame']-x['start_frame']>=10,(eid,'caption too short',x)
  captions+=local
 assert ''.join(c['text'] for c in captions)==''.join(c['text'].strip().replace('\n','') for c in t['cues'])
 assert all(a['end_frame']<=b['start_frame'] for a,b in zip(captions,captions[1:]))
 save(out/'captions-speed1p3.json',dict(episode=eid,fps=FPS,frames=t['frames'],source='confirmed text unchanged',timing='ASR matched characters with interpolation for unmatched characters; measured accelerated audio',entries=captions,alignment=quality,human_audio_listen='NOT_RUN'))
 (out/f'{eid}-speed1p3.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start_frame"])} --> {stamp(c["end_frame"])}\n{c["display_text"]}' for i,c in enumerate(captions))+'\n')
 print(eid,len(captions),'captions, coverage',round(sum(x['matched_characters'] for x in quality)/sum(x['source_characters'] for x in quality),3),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('episodes',nargs='*');a=p.parse_args();model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,num_workers=1,local_files_only=True)
 for eid in a.episodes or [f'EP{i:03d}' for i in range(1,11)]:episode(model,eid)
