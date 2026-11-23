"""基于现有Pillow→FFmpeg静帧链路，只输出确认稿的有声无字版本。"""
from pathlib import Path
import argparse,subprocess,json,hashlib,math,wave,array
from PIL import Image,ImageOps,ImageDraw,ImageFont
from bisect import bisect_right
R=Path(__file__).resolve().parents[1];FPS=30;W=1920;H=1080;SR=48000
def run(a,**kw):return subprocess.run(list(map(str,a)),check=True,**kw)
def main(eid,variant=None,captions=False):
 d=R/'episodes'/eid;tp=d/(f'timeline-{variant}.json' if variant else 'timeline.json');t=json.loads(tp.read_text());cues=t['cues'];shots=t['shots'];nframes=t['frames']
 assert shots[0]['start_frame']==0 and shots[-1]['end_frame']==nframes
 assert all(a['end_frame']==b['start_frame'] for a,b in zip(shots,shots[1:]))
 assert len({s['image_sha256'] for s in shots})==len(shots),'成片镜头复用图'
 assert all((R/s['image_path']).exists() for s in shots)
 o=d/'output';o.mkdir(exist_ok=True);work=d/'render'
 if variant:work=work/(variant+('_subtitled' if captions else ''))
 work.mkdir(parents=True,exist_ok=True)
 caption_data=json.loads((d/'captions/captions-speed1p3.json').read_text())['entries'] if captions else []
 caption_starts=[c['start_frame'] for c in caption_data]
 font=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',54) if captions else None
 def caption_at(frame):
  if not caption_data:return ''
  j=bisect_right(caption_starts,frame)-1
  return caption_data[j].get('display_text',caption_data[j]['text']) if j>=0 and frame<caption_data[j]['end_frame'] else ''
 def paint(im,text):
  if not text:return im.tobytes()
  base=im.copy();draw=ImageDraw.Draw(base)
  draw.text((W//2,H-102),text,font=font,anchor='mm',fill='white',stroke_width=4,stroke_fill=(8,8,8))
  return base.tobytes()
 wavpath=work/'narration.wav';total_samples=nframes*(SR//FPS);pcm=array.array('h',[0])*total_samples
 for c in cues:
  raw=run(['ffmpeg','-v','error','-i',R/c['audio_path'],'-ac','1','-ar',SR,'-f','s16le','-'],capture_output=True).stdout
  a=array.array('h');a.frombytes(raw);start=c['start_frame']*(SR//FPS)
  assert start+len(a)<=total_samples,'音频未覆盖'
  pcm[start:start+len(a)]=a
 with wave.open(str(wavpath),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
 picture=work/'picture.mp4';log=(work/'render.log').open('w')
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','19','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',picture]
 enc=subprocess.Popen(list(map(str,cmd)),stdin=subprocess.PIPE,stderr=log);previous=None;count=0
 for i,s in enumerate(shots):
  with Image.open(R/s['image_path']) as im:image=ImageOps.fit(im.convert('RGB'),(W,H),method=Image.Resampling.LANCZOS)
  raw=image.tobytes();duration=s['end_frame']-s['start_frame'];trans=s.get('transition_frames',0);caption_cache={'':raw}
  for k in range(duration):
   # 仅在时间线已有无声空档内设置叠化；其他事件切点为硬切，不额外添加时长。
   text=caption_at(count)
   if previous is not None and k<trans:frame=paint(Image.blend(previous,image,(k+1)/trans),text)
   else:
    if text not in caption_cache:caption_cache[text]=paint(image,text)
    frame=caption_cache[text]
   enc.stdin.write(frame);count+=1
  previous=image;print(eid,s['shot_id'],count,flush=True)
 enc.stdin.close();assert enc.wait()==0;log.close();assert count==nframes
 suffix=(f'_{variant}' if variant else '')+('_subtitled' if captions else '')
 out=o/f'{eid}_user-script-v2_Chinese_worker_male{suffix}.mp4'
 run(['ffmpeg','-v','error','-y','-i',picture,'-i',wavpath,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar',SR,'-af','apad','-t',f'{nframes/FPS:.9f}','-movflags','+faststart',out])
 # 音频仅补尾静音，不截断；时间线末帧>=最后cue实际时长。
 assert cues[-1]['end_frame']<=nframes
 run(['ffmpeg','-v','error','-i',out,'-f','null','-'],capture_output=True)
 probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',out],capture_output=True,text=True).stdout)
 vs=[s for s in probe['streams'] if s['codec_type']=='video'];aus=[s for s in probe['streams'] if s['codec_type']=='audio'];subs=[s for s in probe['streams'] if s['codec_type']=='subtitle']
 assert len(vs)==1 and len(aus)==1 and not subs
 assert int(vs[0]['nb_read_frames'])==nframes and vs[0]['width']==W and vs[0]['height']==H
 manifest={'episode':eid,'script_version':'user-script-v2','script_sha256':hashlib.sha256((d/'narration.txt').read_bytes()).hexdigest(),'video':str(out.relative_to(R)),'video_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'frames':nframes,'fps':FPS,'duration_seconds':nframes/FPS,'resolution':[W,H],'native_image_dimensions':'see shots/asset manifests; exported 1080p can include upscale','image_count':len(shots),'unique_hashes':len(set(s['image_sha256'] for s in shots)),'audio_streams':len(aus),'subtitle_streams':0,'burned_in_text':'REQUIRES_FRAME_REVIEW','full_decode':'PASS','normal_speed_playback':'NOT_RUN','human_full_watch':'NOT_RUN','human_audio_listen':'NOT_RUN'}
 manifest.update(variant=variant,tempo_multiplier=t.get('tempo_multiplier',1.0),provider_speed=t.get('provider_speed',1.0),timeline=str(tp.relative_to(R)))
 if captions:manifest.update(burned_in_text='CHINESE_CAPTIONS_RENDERED',caption_count=len(caption_data),caption_source='confirmed text unchanged; ASR alignment to accelerated audio',caption_font='STHeiti Medium',caption_font_size=54)
 (o/f'delivery-manifest{suffix}.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(o/f'probe{suffix}.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2))
 print('RENDERED',out,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('episode');p.add_argument('--variant',choices=['speed1p3']);p.add_argument('--captions',action='store_true');a=p.parse_args();main(a.episode,a.variant,a.captions)
