"""Rebuild the 8-episode compilation using new stills and the exact v4 audio stream."""
from pathlib import Path
import json, subprocess, shutil, hashlib
from PIL import Image, ImageOps, ImageDraw, ImageFont

P=Path(__file__).resolve().parents[1]
R=P.parents[1]
O=R/'output/EP001-EP008-v5'
T=json.loads((P/'timeline.json').read_text())
W,H,FPS=T['width'],T['height'],T['fps']
NAME='EP001-EP008_sams_apocalypse_v5'

def run(args):
    subprocess.run(list(map(str,args)),check=True)

def fit(path):
    with Image.open(path) as im:
        return ImageOps.fit(im.convert('RGB'),(W,H),method=Image.Resampling.LANCZOS)

def main():
    O.mkdir(parents=True,exist_ok=True)
    jobs={j['id']:j for j in T['jobs']}
    missing=[j['path'] for j in jobs.values() if not (P/j['path']).exists()]
    assert not missing,missing
    assert T['shots'][0]['start_frame']==0 and T['shots'][-1]['end_frame_exclusive']==T['frames']
    assert all(a['end_frame_exclusive']==b['start_frame'] for a,b in zip(T['shots'],T['shots'][1:]))
    silent=P/'picture.mp4'
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','18','-bf','0','-threads','4','-pix_fmt','yuv420p','-movflags','+faststart',silent]
    caption_picture=P/'caption-picture.mp4'
    caplog=(P/'logs/caption-encode.log').open('w')
    capcmd=cmd[:-1]+[caption_picture]
    capenc=subprocess.Popen(list(map(str,capcmd)),stdin=subprocess.PIPE,stderr=caplog)
    font_path=Path('/System/Library/Fonts/PingFang.ttc')
    if not font_path.exists():font_path=Path('/System/Library/Fonts/STHeiti Light.ttc')
    font=ImageFont.truetype(str(font_path),48)
    cue_index=0;cached_key=None;cached_caption=None
    def caption_bytes(im,text):
        rendered=im.copy();draw=ImageDraw.Draw(rendered)
        draw.text((W//2,H-74),text,font=font,anchor='mm',fill='white',stroke_width=3,stroke_fill='#101010')
        return rendered.tobytes()
    with (P/'logs/encode.log').open('w') as log:
        enc=subprocess.Popen(list(map(str,cmd)),stdin=subprocess.PIPE,stderr=log)
        previous=None;count=0
        for i,s in enumerate(T['shots']):
            im=fit(P/jobs[s['asset']]['path']);n=s['end_frame_exclusive']-s['start_frame']
            raw=im.tobytes()
            for k in range(n):
                blended=Image.blend(previous,im,(k+1)/T['transition_frames']) if previous is not None and k<T['transition_frames'] else None
                frame=blended.tobytes() if blended is not None else raw
                while cue_index+1<len(T['cues']) and count>=T['cues'][cue_index+1]['output_start_frame']:cue_index+=1
                key=(i,cue_index)
                if blended is not None:
                    capframe=caption_bytes(blended,T['cues'][cue_index]['text'])
                else:
                    if cached_key!=key:
                        cached_caption=caption_bytes(im,T['cues'][cue_index]['text']);cached_key=key
                    capframe=cached_caption
                enc.stdin.write(frame);capenc.stdin.write(capframe);count+=1
            previous=im
            print(f"render {i+1}/{len(T['shots'])}: {s['id']} frames={count}",flush=True)
        enc.stdin.close();capenc.stdin.close();assert enc.wait()==0 and capenc.wait()==0
    caplog.close()
    assert count==T['frames']
    old=R/'output/EP001-EP008-v4'
    for ext in ['srt','vtt']:
        shutil.copy2(old/f'EP001-EP008_sams_apocalypse_v4.zh-CN.{ext}',O/f'{NAME}.zh-CN.{ext}')
    shutil.copy2(old/'chapters.json',O/'chapters.json')
    clean=O/f'{NAME}_clean.mp4'
    run(['ffmpeg','-v','error','-y','-i',silent,'-i',old/'EP001-EP008_sams_apocalypse_v4.mp4','-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',clean])
    run(['ffmpeg','-v','error','-y','-i',caption_picture,'-i',old/'EP001-EP008_sams_apocalypse_v4.mp4','-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',O/f'{NAME}.mp4'])
    manifest={'version':5,'status':'rendered_pending_qa','duration_seconds':T['duration_seconds'],'frames':T['frames'],'fps':FPS,'resolution':[W,H],'images':len(jobs),'shots':len(T['shots']),'transition_frames':4,'camera':'locked','audio':'v4 original complete narration/music mix copied without reencoding','speech_regenerated':False,'speech_rate_changed':False,'cues':len(T['cues']),'text_and_timing':'exact v4 SRT/VTT copy','clean_video':clean.name,'captioned_video':NAME+'.mp4','style':'realistic disaster cinema, intact dry clean supermarket','generation':'GPT built-in imagegen; stills plus local dissolves, not generated live action','assets':[{'id':j['id'],'file':j['path'],'sha256':hashlib.sha256((P/j['path']).read_bytes()).hexdigest()} for j in jobs.values()]}
    (O/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('RENDER COMPLETE',flush=True)

if __name__=='__main__':main()
