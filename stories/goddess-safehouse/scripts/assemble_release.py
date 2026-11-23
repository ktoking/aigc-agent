"""无额外片头时长：10集整数帧连续拼接，连续PCM音轨一次AAC编码。"""
from pathlib import Path
import array, hashlib, json, subprocess, wave

R=Path(__file__).resolve().parents[1]
V=R/'production/user-script-v2'
O=V/'release-speed1p3'
FPS,SR=30,48000

def run(args,**kw):return subprocess.run(list(map(str,args)),check=True,**kw)
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def stamp(f):
 ms=round(f*1000/FPS);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'

def main():
 sm=json.loads((V/'script-manifest.json').read_text());frames=0;chapters=[];entries=[];pictures=[];hashes=[];pcm=array.array('h');proof=[]
 for e in sm['episodes']:
  eid=e['episode'];d=R/'episodes'/eid;t=json.loads((d/'timeline-speed1p3.json').read_text())
  p=d/'render/speed1p3_subtitled/picture.mp4';assert p.exists(),p;pictures.append(p)
  m=json.loads((d/'output/delivery-manifest_speed1p3_subtitled.json').read_text());assert m['frames']==t['frames'] and m['burned_in_text']=='CHINESE_CAPTIONS_RENDERED'
  assert hashlib.sha256((d/'narration.txt').read_bytes()).hexdigest()==e['narration_sha256']
  captions=json.loads((d/'captions/captions-speed1p3.json').read_text())['entries']
  assert ''.join(c['text'] for c in captions)==''.join(c['text'].strip().replace('\n','') for c in t['cues'])
  for c in captions:entries.append({**c,'episode':eid,'start_frame':c['start_frame']+frames,'end_frame':c['end_frame']+frames})
  with wave.open(str(d/'render/speed1p3_subtitled/narration.wav'),'rb') as w:
   assert w.getframerate()==SR and w.getnchannels()==1 and w.getnframes()==t['frames']*(SR//FPS)
   a=array.array('h');a.frombytes(w.readframes(w.getnframes()));pcm.extend(a)
  hashes.extend(s['image_sha256'] for s in t['shots'])
  chapters.append(dict(episode=eid,title=e['title'],start_frame=frames,end_frame=frames+t['frames']))
  frames+=t['frames'];proof.append(m)
 assert len(set(hashes))==len(hashes),'合集有图像复用'
 master=O/'前10集连续配音_1.3倍.wav'
 with wave.open(str(master),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
 concat=O/'concat-pictures.txt';concat.write_text('\n'.join("file '"+str(p).replace("'","'\\''")+"'" for p in pictures)+'\n')
 md=[';FFMETADATA1','title=末世囤货：我的安全屋住满了女神 · 前10集合集']
 for c in chapters:md+=['[CHAPTER]','TIMEBASE=1/30',f'START={c["start_frame"]}',f'END={c["end_frame"]}',f'title=第{int(c["episode"][2:])}集《{c["title"]}》']
 metadata=O/'chapters.ffmeta';metadata.write_text('\n'.join(md)+'\n')
 out=O/'末世囤货_前10集合集_1.3倍速_字幕版.mp4'
 run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat,'-i',master,'-i',metadata,'-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-c:v','copy','-c:a','aac','-b:a','192k','-ar',SR,'-af','apad','-t',f'{frames/FPS:.9f}','-movflags','+faststart',out])
 run(['ffmpeg','-v','error','-i',out,'-f','null','-'],capture_output=True)
 probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-show_chapters','-of','json',out],capture_output=True,text=True).stdout)
 vs=[s for s in probe['streams'] if s['codec_type']=='video'];aus=[s for s in probe['streams'] if s['codec_type']=='audio'];subs=[s for s in probe['streams'] if s['codec_type']=='subtitle']
 assert len(vs)==1 and len(aus)==1 and not subs and vs[0]['width']==1920 and vs[0]['height']==1080
 assert int(vs[0]['nb_read_frames'])==frames and len(probe['chapters'])==10
 assert abs(float(vs[0]['duration'])-frames/FPS)<1/FPS
 save(O/'probe.json',probe);save(O/'chapters.json',chapters);save(O/'captions.json',entries)
 (O/'前10集_1.3倍速.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start_frame"])} --> {stamp(c["end_frame"])}\n{c["display_text"]}' for i,c in enumerate(entries))+'\n')
 save(O/'delivery-manifest.json',dict(video=str(out.relative_to(R)),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),episodes=10,frames=frames,duration_seconds=frames/FPS,resolution=[1920,1080],fps=FPS,images=len(hashes),unique_image_hashes=len(set(hashes)),voice_id='Chinese_worker_male',provider_speed=1.0,postprocess_tempo=1.3,subtitles='BURNED_IN_CHINESE',caption_count=len(entries),text_changes=0,chapters=chapters,full_decode='PASS',normal_speed_playback='NOT_RUN',human_audio_listen='NOT_RUN',human_full_watch='NOT_RUN',source_episode_proof=proof))
 print('RELEASE_COMPLETE',out,frames/FPS,'seconds',frames,'frames',len(hashes),'independent images',flush=True)

if __name__=='__main__':main()
