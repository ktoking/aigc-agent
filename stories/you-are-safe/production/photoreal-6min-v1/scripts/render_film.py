#!/usr/bin/env python3
"""固定图像、三帧（0.1秒）短叠化；从同一帧时间线导出无音轨视频。"""
from pathlib import Path
import json,subprocess,concurrent.futures,shutil
P=Path(__file__).resolve().parents[1]
R=P.parents[1]
O=R/'output/photoreal-6min-v1'
PLAN=json.loads((P/'timeline.json').read_text())
FPS=PLAN['fps'];W=PLAN['width'];H=PLAN['height']

def run(args,log):
 with log.open('w') as f:
  subprocess.run([str(x) for x in args],stdout=f,stderr=subprocess.STDOUT,check=True)

def render(index):
 shot=PLAN['shots'][index];source=P/shot['asset'];dest=P/'clips'/(shot['id']+'.mp4')
 frames=shot['end_frame_exclusive']-shot['start_frame']
 scale=f'scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1,fps={FPS},settb=1/{FPS},setpts=N'
 cmd=['ffmpeg','-v','error','-y','-filter_complex_threads','1']
 if index:
  previous=P/PLAN['shots'][index-1]['asset']
  cmd+=['-loop','1','-framerate',str(FPS),'-i',previous,'-loop','1','-framerate',str(FPS),'-i',source]
  filt=f'[0:v]{scale},format=yuv444p[a];[1:v]{scale},format=yuv444p[b];[a][b]xfade=transition=fade:duration={PLAN["transition_frames"]/FPS:.9f}:offset=0,format=yuv420p[out]'
 else:
  cmd+=['-loop','1','-framerate',str(FPS),'-i',source]
  filt=f'[0:v]{scale},format=yuv420p[out]'
 cmd+=['-filter_complex',filt,'-map','[out]','-frames:v',str(frames),'-an','-sn','-dn','-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','18','-tune','stillimage','-bf','0','-threads','2','-pix_fmt','yuv420p','-video_track_timescale','15360','-movflags','+faststart',dest]
 run(cmd,P/'logs'/(shot['id']+'.log'))
 return {'id':shot['id'],'frames':frames,'file':str(dest.relative_to(P))}

def main():
 assert W==1920 and H==1080 and FPS==30
 missing=[s['asset'] for s in PLAN['shots'] if not (P/s['asset']).is_file()]
 if missing:raise SystemExit('缺图，未开始渲染：'+','.join(missing))
 for folder in [P/'clips',P/'logs',O]:folder.mkdir(parents=True,exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  done=[]
  for result in pool.map(render,range(len(PLAN['shots']))):
   done.append(result);print('rendered',result['id'],result['frames'],flush=True)
 paths=[(P/'clips'/(s['id']+'.mp4')).resolve() for s in PLAN['shots']]
 concat=P/'clips.ffconcat'
 concat.write_text('ffconcat version 1.0\n'+'\n'.join("file '"+str(p).replace("'","'\\''")+"'" for p in paths)+'\n')
 run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat,'-map','0:v:0','-c:v','copy','-an','-sn','-dn','-movflags','+faststart',O/'you-are-safe-photoreal-6min-v1.mp4'],P/'logs/concat.log')
 (P/'render-manifest.json').write_text(json.dumps({'engine':'FFmpeg libx264','camera':'locked_static','transition_frames':PLAN['transition_frames'],'transition_inside_incoming_clip':True,'frames':PLAN['frames'],'audio':False,'subtitles_burned':False,'rendered_clips':done},ensure_ascii=False,indent=2)+'\n')
 shutil.copy2(P/'narration.txt',O/'narration.txt')
 print('COMPLETE',PLAN['frames'],'frames',PLAN['duration_seconds'],'seconds',flush=True)
if __name__=='__main__':main()
