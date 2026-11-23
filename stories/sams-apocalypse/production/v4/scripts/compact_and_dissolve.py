"""Edit supplied finished film: sentence-aware pause removal, short picture dissolves.
No speech regeneration, rate change, dynamic camera, or overlapping spoken turns.
"""
from pathlib import Path
import json,re,math,subprocess,wave,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
PROD=ROOT/'production/v4';OUT=ROOT/'output/EP001-EP008-v4';OUT.mkdir(exist_ok=True)
SOURCE=Path('/Users/kaiyi.wang/Downloads/64458d0740b90fc9c984893d2037ceb2.mp4')
FPS=30;W=960;H=544
plan=json.loads((ROOT/'production/v3/timing-plan.json').read_text())
vad=json.loads((PROD/'analysis/vad.json').read_text())
cues=[];offset=0
for ep in plan['episodes']:
 for c in ep['cues']:
  cues.append({**c,'episode':ep['episode'],'source_start':offset+c['start_frame']/30,'source_end':offset+c['end_frame_exclusive']/30})
 offset+=ep['duration_seconds']
bounds=[c['source_end'] for c in cues]
# Only remove detected non-speech spans near known sentence handoffs.
# Leave within-sentence pauses alone. Guard consonants and tails by 60ms on both sides;
# round outward from retained speech so frame alignment never removes those guards.
removals=[]
for a,b in zip(vad,vad[1:]):
 start,end=a['end'],b['start']
 nearby=[x for x in bounds if start-.20<=x<=end+.20]
 if end-start<.25 or not nearby:continue
 sf=math.ceil((start+.060)*FPS);ef=math.floor((end-.060)*FPS)
 if ef<=sf:continue
 removals.append({'start_frame':sf,'end_frame_exclusive':ef,'detected_gap':[start,end],'sentence_boundaries':nearby,'reason':'sentence_handoff_non_speech'})
first=max(0,math.floor((vad[0]['start']-.060)*FPS))
last=math.ceil((vad[-1]['end']+.080)*FPS)
keeps=[];start=first
for r in removals:
 if r['start_frame']>start:keeps.append((start,r['start_frame']))
 start=r['end_frame_exclusive']
if start<last:keeps.append((start,last))
frame_map=np.concatenate([np.arange(a,b,dtype=np.int32) for a,b in keeps])
frame_map.tofile(PROD/'analysis/output-to-source-frames.int32')
assert len(frame_map)>0 and np.all(np.diff(frame_map)>0)
source_cuts={round(float(t)*FPS) for t in re.findall(r'pts_time:([\d.]+)',(PROD/'analysis/scene-cuts.txt').read_text())}
cut_sorted=sorted(source_cuts)
# Audio uses exactly the same retained source frame ranges.
with wave.open(str(PROD/'analysis/source-fullrate.wav'),'rb') as f:
 rate=f.getframerate();assert rate==44100 and f.getnchannels()==1
 raw=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16)
chunks=[]
for a,b in keeps:
 part=raw[a*1470:b*1470].astype(np.float64)
 # 2ms edge ramp avoids clicks; no audio overlap or time added.
 ramp=min(88,len(part)//2)
 part[:ramp]*=np.linspace(0,1,ramp);part[-ramp:]*=np.linspace(1,0,ramp)
 chunks.append(np.rint(part).clip(-32768,32767).astype(np.int16))
joined=np.concatenate(chunks)
assert len(joined)==len(frame_map)*1470
with wave.open(str(PROD/'analysis/compacted.wav'),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(joined.tobytes())
# Streaming video: process actual input frames, preserve its baked captions.
# Picture dissolves occupy incoming frames (4/30s); subtitle band switches cleanly.
# The vertical feather prevents a visible horizontal edge above the caption band.
mask=np.ones((H,1,1),np.float32)
mask[400:430,0,0]=np.linspace(1,0,30);mask[430:,0,0]=0
readlog=(PROD/'logs/decode.log').open('w');writelog=(PROD/'logs/encode.log').open('w')
decoder=subprocess.Popen(['ffmpeg','-v','error','-i',str(SOURCE),'-an','-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=readlog)
video=PROD/'analysis/picture.mp4'
encoder=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-bf','0','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE,stderr=writelog)
next_index=0;previous_source=None;previous_picture=None;fade_from=None;fade_i=4;transitions=[]
try:
 for source_frame in range(last):
  buf=decoder.stdout.read(W*H*3)
  if len(buf)!=W*H*3:raise RuntimeError(f'Unexpected video EOF frame {source_frame}')
  if next_index>=len(frame_map) or source_frame!=frame_map[next_index]:continue
  picture=np.frombuffer(buf,np.uint8).reshape(H,W,3)
  crossed=previous_source is not None and any(previous_source<c<=source_frame for c in cut_sorted)
  if crossed:
   fade_from=previous_picture.copy();fade_i=0
   transitions.append({'output_frame':next_index,'source_frame':source_frame,'frames':4,'picture':'feathered_dissolve','subtitle_band':'incoming_only_no_double_text','audio_overlap':False})
  if fade_i<4:
   incoming=(fade_i+1)/4
   old_weight=mask*(1-incoming)
   rendered=np.rint(picture.astype(np.float32)*(1-old_weight)+fade_from.astype(np.float32)*old_weight).clip(0,255).astype(np.uint8)
   fade_i+=1
  else:rendered=picture
  encoder.stdin.write(rendered.tobytes());previous_picture=picture;previous_source=source_frame;next_index+=1
  if next_index%900==0:print(f'rendered {next_index}/{len(frame_map)}',flush=True)
finally:
 encoder.stdin.close();decoder.stdout.close();decoder.terminate()
encoder.wait();decoder.wait();readlog.close();writelog.close()
if encoder.returncode!=0:raise RuntimeError('Encoding failed')
assert next_index==len(frame_map)
final=OUT/'EP001-EP008_sams_apocalypse_v4.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-i',str(PROD/'analysis/compacted.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart',str(final)],check=True)
# Remap all 130 authored cues, using the SAME output-to-source frame map.
newc=[]
for c in cues:
 a=int(np.searchsorted(frame_map,round(c['source_start']*FPS)));b=int(np.searchsorted(frame_map,round(c['source_end']*FPS)))
 assert b>a,(c['text'],a,b)
 newc.append({**c,'output_start_frame':a,'output_end_frame_exclusive':b})
assert newc[0]['output_start_frame']==0 and newc[-1]['output_end_frame_exclusive']==len(frame_map)
assert all(a['output_end_frame_exclusive']==b['output_start_frame'] for a,b in zip(newc,newc[1:]))
def stamp(frame,sep=','):
 ms=round(frame*1000/FPS);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}'
srt=[];vtt=[]
for i,c in enumerate(newc,1):
 a,b=c['output_start_frame'],c['output_end_frame_exclusive'];text=c['text']
 srt.append(f'{i}\n{stamp(a)} --> {stamp(b)}\n{text}')
 vtt.append(f'{stamp(a,".")} --> {stamp(b,".")}\n{text}')
(OUT/'EP001-EP008_sams_apocalypse_v4.zh-CN.srt').write_text('\n\n'.join(srt)+'\n')
(OUT/'EP001-EP008_sams_apocalypse_v4.zh-CN.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(vtt)+'\n')
chapters=[]
for ep in plan['episodes']:
 c=[x for x in newc if x['episode']==ep['episode']]
 chapters.append({'episode':ep['episode'],'title':ep['title'],'start_seconds':c[0]['output_start_frame']/30,'end_seconds':c[-1]['output_end_frame_exclusive']/30})
(OUT/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2)+'\n')
removed_frames=11138-len(frame_map)
speed=[]
for c in newc:
 count=len(re.findall(r'[\u4e00-\u9fffA-Za-z0-9]',c['text']))
 speed.append({'episode':c['episode'],'text':c['text'],'characters':count,'source_slot_seconds':c['source_end']-c['source_start'],'new_slot_seconds':(c['output_end_frame_exclusive']-c['output_start_frame'])/FPS,'cps':count/((c['output_end_frame_exclusive']-c['output_start_frame'])/FPS)})
record={'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source_seconds':11138/FPS,'output_seconds':len(frame_map)/FPS,'output_frames':len(frame_map),'removed_seconds':removed_frames/FPS,'initial_trim_seconds':first/FPS,'tail_trim_seconds':(11138-last)/FPS,'sentence_pause_removals':removals,'keep_ranges':keeps,'transitions':transitions,'cues':newc,'speaking_rate_observations':speed,'speech_regenerated':False,'speech_rate_changed':False,'audio_overlap':False,'caption_source':'Existing burned captions retained; external authored SRT remapped to same edit; ASR does not rewrite text','width':W,'height':H,'fps':30}
(PROD/'edit-timeline.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'complete':True,'seconds':len(frame_map)/FPS,'removed_seconds':removed_frames/FPS,'sentence_pause_removals':len(removals),'dissolves':len(transitions),'output':str(final)},ensure_ascii=False),flush=True)
