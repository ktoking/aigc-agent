"""沿用故事已验证的Pillow→FFmpeg链路：离线字幕对齐、静帧烧字、连续PCM与章节。"""
from pathlib import Path
import argparse,array,difflib,hashlib,json,math,re,subprocess,time,unicodedata,wave

P=Path(__file__).resolve().parent;R=P.parents[1]
O=P/'release-speed1p3';O.mkdir(exist_ok=True)
D=R/'delivery/后10集_世外桃源_剧本图片多角色配音'
FPS,SR,W,H=30,48000,1920,1080

def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def run(a,**kw):return subprocess.run(list(map(str,a)),check=True,**kw)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def display(text):return re.sub(r'\s+',' ',''.join(' ' if unicodedata.category(c).startswith('P') else c for c in text)).strip()
def split(text):
 parts=re.findall(r'[^，。！？；、\n]+[，。！？；、]*',text);out=[]
 for p in parts:
  while len(p)>18:out.append(p[:16]);p=p[16:]
  if p:
   if out and len(p)<=5 and len(out[-1])+len(p)<=18:out[-1]+=p
   else:out.append(p)
 assert ''.join(out)==text.strip().replace('\n','')
 return out

def align():
 import numpy as np
 from faster_whisper import WhisperModel
 from opencc import OpenCC
 cc=OpenCC('t2s')
 def norm(c):
  c=cc.convert(unicodedata.normalize('NFKC',c));return c.lower() if any(x.isalnum() for x in c) else ''
 model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,num_workers=1,local_files_only=True)
 for e in json.loads((P/'episode-source.json').read_text()):
  eid=e['episode'];ep=R/'episodes'/eid;t=json.loads((ep/'timeline-speed1p3.json').read_text());audio=ep/'output'/f'{eid}_多角色_1.3倍.wav'
  ap=O/f'{eid}-asr.json';cache=json.loads(ap.read_text()) if ap.exists() else {};key=sha(audio)
  if cache.get('audio_sha256')==key:words=cache['words']
  else:
   raw=run(['ffmpeg','-v','error','-i',audio,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout
   segments,info=model.transcribe(np.frombuffer(raw,dtype=np.float32),language='zh',beam_size=3,word_timestamps=True,condition_on_previous_text=False,vad_filter=False,initial_prompt='陈屿、夏凛、许知意、乔星野、顾南枝、王大富、方舟安全屋、血月、安心值、物资点、B七、恒温耕地。')
   words=[{'word':w.word,'start':w.start,'end':w.end,'probability':w.probability} for s in segments for w in s.words or []]
   save(ap,{'audio_sha256':key,'model':'faster-whisper-small-local-int8','words':words})
  caps=[];quality=[]
  for c in t['cues']:
   text=c['source_text'].strip().replace('\n','');parts=split(text)
   if len(parts)==1 or (len(display(text))<=26 and c['end_frame']-c['start_frame']<=210):
    caps.append({'cue_id':c['cue_id'],'text':text,'display_text':display(text),'start_frame':c['start_frame'],'end_frame':c['end_frame'],'timing':'EXACT_MEASURED_CUE','speaker':c['speaker']});continue
   clean='';indices=[]
   for i,ch in enumerate(text):
    n=norm(ch)
    if n:clean+=n;indices.extend([i]*len(n))
   recognized='';times=[]
   for w in words:
    if w['end']<c['start_frame']/FPS or w['start']>=c['end_frame']/FPS:continue
    n=''.join(norm(ch) for ch in w['word'])
    for k,ch in enumerate(n):recognized+=ch;times.append((w['start']+(w['end']-w['start'])*k/max(1,len(n)),w['start']+(w['end']-w['start'])*(k+1)/max(1,len(n))))
   matches={}
   for a,b,n in difflib.SequenceMatcher(None,clean,recognized,autojunk=False).get_matching_blocks():
    for k in range(n):matches[a+k]=times[b+k]
   coverage=len(matches)/max(1,len(clean))
   route='EPISODE_ASR'
   if coverage<.5:
    # 整集识别漏段或漂移时只重识别当前实际音频，不改台词、不重新配音。
    raw=run(['ffmpeg','-v','error','-i',R/c['audio_path'],'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout
    segs,_=model.transcribe(np.frombuffer(raw,dtype=np.float32),language='zh',beam_size=5,word_timestamps=True,condition_on_previous_text=False,vad_filter=False,initial_prompt='陈屿、夏凛、许知意、乔星野、顾南枝、血月、安全屋。')
    recognized='';times=[]
    for seg in segs:
     for w in seg.words or []:
      n=''.join(norm(ch) for ch in w.word)
      for k,ch in enumerate(n):
       recognized+=ch;times.append((c['start_frame']/FPS+w.start+(w.end-w.start)*k/max(1,len(n)),c['start_frame']/FPS+w.start+(w.end-w.start)*(k+1)/max(1,len(n))))
    matches={}
    for a,b,n in difflib.SequenceMatcher(None,clean,recognized,autojunk=False).get_matching_blocks():
     for k in range(n):matches[a+k]=times[b+k]
    coverage=len(matches)/max(1,len(clean));route='CUE_LOCAL_ASR'
   quality.append({'cue_id':c['cue_id'],'coverage':coverage,'recognized_text':recognized,'source_text':text,'route':route})
   assert coverage>=.5,(eid,c['cue_id'],'字幕对齐需修复',coverage)
   starts=[]
   for i in range(len(clean)):
    if i in matches:starts.append(matches[i][0]);continue
    left=max((k for k in matches if k<i),default=-1);right=min((k for k in matches if k>i),default=len(clean));lt=matches[left][1] if left>=0 else c['start_frame']/FPS;rt=matches[right][0] if right<len(clean) else c['end_frame']/FPS
    starts.append(lt+(rt-lt)*(i-left)/(right-left))
   for i in range(1,len(starts)):starts[i]=max(starts[i],starts[i-1])
   local=[];offset=0
   for part in parts:
    ix=next((j for j,k in enumerate(indices) if k>=offset),len(starts)-1)
    sf=max(c['start_frame'],min(c['end_frame']-1,math.floor(starts[ix]*FPS)-1))
    local.append({'cue_id':c['cue_id'],'speaker':c['speaker'],'text':part,'display_text':display(part),'start_frame':sf,'timing':'ASR_MATCHED_WITH_INTERPOLATION'});offset+=len(part)
   # 极短尾段并回前一条，仍逐字保留原文，不造出闪烁字幕。
   for i in range(len(local)-1,0,-1):
    end=local[i+1]['start_frame'] if i+1<len(local) else c['end_frame']
    if end-local[i]['start_frame']<10 or local[i]['start_frame']-local[i-1]['start_frame']<10:
     local[i-1]['text']+=local[i]['text'];local[i-1]['display_text']=display(local[i-1]['text']);local.pop(i)
   for i,x in enumerate(local):
    x['end_frame']=local[i+1]['start_frame'] if i+1<len(local) else c['end_frame'];assert x['end_frame']>x['start_frame']
   caps.extend(local)
  assert ''.join(x['text'] for x in caps)==''.join(c['source_text'].strip().replace('\n','') for c in t['cues'])
  assert all(a['end_frame']<=b['start_frame'] for a,b in zip(caps,caps[1:]))
  assert not any(unicodedata.category(ch).startswith('P') for x in caps for ch in x['display_text'])
  save(O/f'{eid}-captions.json',{'episode':eid,'audio_sha256':key,'frames':t['frames'],'entries':caps,'alignment':quality,'text_changes':0,'human_listening':'NOT_RUN'})
  print('CAPTIONS_READY',eid,len(caps),'min long-cue coverage',round(min((x['coverage'] for x in quality),default=1),3),flush=True)
 save(O/'caption-status.json',{'status':'PASS','episodes':10})

def render():
 from PIL import Image,ImageOps,ImageDraw,ImageFont
 from bisect import bisect_right
 src=json.loads((P/'episode-source.json').read_text());chapters=[];shots=[];caps=[];pcm=array.array('h');offset=0
 for e in src:
  eid=e['episode'];cp=O/f'{eid}-captions.json'
  while not cp.exists():
   if (O/'alignment-failure.json').exists():raise RuntimeError('字幕对齐失败，停止合成，详见记录')
   time.sleep(2)
  ep=R/'episodes'/eid;t=json.loads((ep/'timeline-speed1p3.json').read_text());c=json.loads(cp.read_text());assert c['frames']==t['frames']
  for s in t['shots']:
   assert s['visual_review']=='PASS_MODEL_VISUAL_REVIEW';assert sha(R/s['image_path'])==s['image_sha256']
   shots.append({**s,'start_frame':s['start_frame']+offset,'end_frame':s['end_frame']+offset})
  caps.extend({**x,'episode':eid,'start_frame':x['start_frame']+offset,'end_frame':x['end_frame']+offset} for x in c['entries'])
  with wave.open(str(ep/'output'/f'{eid}_多角色_1.3倍.wav'),'rb') as w:
   assert (w.getframerate(),w.getnchannels(),w.getsampwidth())==(SR,1,2);assert w.getnframes()==t['frames']*(SR//FPS)
   chunk=array.array('h');chunk.frombytes(w.readframes(w.getnframes()));pcm.extend(chunk)
  chapters.append({'episode':eid,'title':e['title'],'start_frame':offset,'end_frame':offset+t['frames']});offset+=t['frames']
 assert len(set(s['image_sha256'] for s in shots))==len(shots)==132
 assert shots[0]['start_frame']==0 and shots[-1]['end_frame']==offset and all(a['end_frame']==b['start_frame'] for a,b in zip(shots,shots[1:]))
 master=O/'后10集连续配音_1.3倍.wav'
 with wave.open(str(master),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
 del pcm
 meta=[';FFMETADATA1','title=末世囤货：我的安全屋住满了女神 · 第11—20集合集']
 for c in chapters:meta+=['[CHAPTER]','TIMEBASE=1/30',f'START={c["start_frame"]}',f'END={c["end_frame"]}',f'title=第{int(c["episode"][2:])}集《{c["title"]}》']
 (O/'chapters.ffmeta').write_text('\n'.join(meta)+'\n');save(O/'chapters.json',chapters);save(O/'captions.json',caps)
 font=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',54);caption_starts=[c['start_frame'] for c in caps]
 def caption_at(f):
  j=bisect_right(caption_starts,f)-1
  return caps[j]['display_text'] if j>=0 and f<caps[j]['end_frame'] else ''
 picture=O/'picture_subtitled.mp4';count=0
 with (O/'render-ffmpeg.log').open('w') as log:
  enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','19','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(picture)],stdin=subprocess.PIPE,stderr=log)
  for s in shots:
   with Image.open(R/s['image_path']) as im:frame=ImageOps.fit(im.convert('RGB'),(W,H),method=Image.Resampling.LANCZOS)
   cache={'':frame.tobytes()}
   for k in range(s['end_frame']-s['start_frame']):
    text=caption_at(count)
    if text not in cache:
     f=frame.copy();draw=ImageDraw.Draw(f);draw.text((W//2,H-102),text,font=font,anchor='mm',fill='white',stroke_width=4,stroke_fill=(8,8,8));cache[text]=f.tobytes()
    enc.stdin.write(cache[text]);count+=1
   print('SHOT_RENDERED',s['shot_id'],count,'/',offset,flush=True)
  enc.stdin.close();assert enc.wait()==0
 assert count==offset
 out=D/'末世囤货_第11-20集合集_1.3倍速_多角色_字幕版.mp4'
 assert not out.exists(),'保留既有成片，请换版本名'
 run(['ffmpeg','-v','error','-y','-i',picture,'-i',master,'-i',O/'chapters.ffmeta','-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-c:v','copy','-c:a','aac','-b:a','192k','-ar',SR,'-af','apad','-t',f'{offset/FPS:.9f}','-movflags','+faststart',out])
 run(['ffmpeg','-v','error','-i',out,'-f','null','-'],capture_output=True)
 probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-show_chapters','-of','json',out],capture_output=True,text=True).stdout)
 v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(W,H,'30/1',offset)
 assert len(probe['chapters'])==10 and abs(float(v['duration'])-offset/FPS)<1/FPS
 save(O/'probe.json',probe)
 report={'video':str(out.relative_to(R)),'sha256':sha(out),'frames':offset,'duration_seconds':offset/FPS,'width':W,'height':H,'fps':FPS,'episodes':10,'chapters':chapters,'images':132,'unique_image_hashes':132,'voice_cues':95,'voice_cast':json.loads((P/'voice-cast.json').read_text()),'provider_speed':1.0,'post_atempo':1.3,'burned_in_subtitles':True,'punctuation_display':'REPLACED_BY_SPACES','caption_count':len(caps),'caption_text_changes':0,'full_decode':'PASS','normal_speed_playback':'NOT_RUN','human_full_watch':'NOT_RUN','human_full_listening':'NOT_RUN','image_native_dimensions':'see source manifests; 1080p export includes upscale'}
 save(O/'video-manifest.json',report);save(D/'合集视频清单.json',report)
 s=json.loads((P/'status.json').read_text());s.update(videos='PASS_RENDERED_SUBTITLED_DECODED',collection_video=str(out.relative_to(R)),production_status='COLLECTION_RENDERED_AWAITING_PLAYBACK_CHECK');save(P/'status.json',s)
 print('COLLECTION_COMPLETE',out,offset/FPS,'seconds',len(caps),'captions',flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['align','render']);a=p.parse_args()
 try:align() if a.mode=='align' else render()
 except Exception as e:
  if a.mode=='align':save(O/'alignment-failure.json',{'error':str(e)})
  raise
