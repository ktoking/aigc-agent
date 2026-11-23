"""Structural, audio-preservation and encoded-image checks; visual review recorded separately."""
from pathlib import Path
import json, subprocess, hashlib, re, math
import numpy as np
from PIL import Image,ImageOps,ImageDraw

P=Path(__file__).resolve().parents[1];R=P.parents[1];O=R/'output/EP001-EP008-v5'
Q=P/'qa';Q.mkdir(exist_ok=True)
T=json.loads((P/'timeline.json').read_text());N='EP001-EP008_sams_apocalypse_v5'

def output(args):return subprocess.check_output(list(map(str,args)))
def ahash(path):
    return output(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).decode().strip()

def main():
    clean=O/(N+'_clean.mp4');captioned=O/(N+'.mp4')
    probe=json.loads(output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',captioned]))
    (Q/'ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n')
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert [v['width'],v['height']]==[1920,1080] and int(v['nb_read_frames'])==T['frames']
    assert v['r_frame_rate']=='30/1'
    assert len([s for s in probe['streams'] if s['codec_type']=='audio'])==1
    old=R/'output/EP001-EP008-v4'
    sound=ahash(old/'EP001-EP008_sams_apocalypse_v4.mp4')
    assert ahash(clean)==sound and ahash(captioned)==sound
    for ext in ['srt','vtt']:
        assert (O/f'{N}.zh-CN.{ext}').read_bytes()==(old/f'EP001-EP008_sams_apocalypse_v4.zh-CN.{ext}').read_bytes()
    assert len(re.findall(r' --> ',(O/f'{N}.zh-CN.srt').read_text()))==130
    # Decode every frame of clean MP4 for fixed-camera stability; no motion introduced.
    raw=output(['ffmpeg','-v','error','-i',clean,'-an','-vf','scale=96:54','-pix_fmt','gray','-f','rawvideo','-'])
    frames=np.frombuffer(raw,np.uint8).reshape(-1,54,96).astype(np.int16)
    assert len(frames)==T['frames']
    differences=np.mean(np.abs(frames[1:]-frames[:-1]),axis=(1,2))
    stable=[]
    for shot in T['shots']:
        a,b=shot['start_frame'],shot['end_frame_exclusive']
        vals=differences[a+6:b-1]
        stable.append({'shot':shot['id'],'max_mean_luma_change':float(vals.max()) if len(vals) else 0})
    max_change=max(x['max_mean_luma_change'] for x in stable)
    assert max_change<1.0,max_change
    assert float(frames.mean(axis=(1,2)).min())>2
    subprocess.run(['ffmpeg','-v','error','-i',captioned,'-f','null','-'],check=True)
    # Actual encoded shot images, reviewed as labelled pages after generation.
    folder=Q/'shots';folder.mkdir(exist_ok=True)
    mids=[(s['start_frame']+s['end_frame_exclusive'])//2 for s in T['shots']]
    select='+'.join(f'eq(n,{n})' for n in mids)
    subprocess.run(['ffmpeg','-v','error','-y','-i',captioned,'-vf',f'select={select.replace(chr(44),chr(92)+chr(44))},scale=480:270','-fps_mode','vfr',str(folder/'%03d.jpg')],check=True)
    files=sorted(folder.glob('*.jpg'));assert len(files)==len(T['shots'])
    for page in range(math.ceil(len(files)/12)):
        canvas=Image.new('RGB',(1440,4*300),'#151b25');d=ImageDraw.Draw(canvas)
        for i,impath in enumerate(files[page*12:(page+1)*12]):
            idx=page*12+i; x=(i%3)*480;y=(i//3)*300
            with Image.open(impath) as im:canvas.paste(im,(x,y))
            s=T['shots'][idx];d.text((x+8,y+275),f"{s['id']} / {s['asset']} / {mids[idx]/30:.2f}s",fill='white')
        canvas.save(Q/f'contact-{page+1:02d}.jpg')
    # Continuous frames from representative actual encoded transitions.
    for j,shot_index in enumerate([1,14,30,46,62],1):
        start=T['shots'][shot_index]['start_frame']
        data=output(['ffmpeg','-v','error','-i',captioned,'-vf',f'select=between(n\\,{start-1}\\,{start+4}),scale=480:270','-fps_mode','vfr','-pix_fmt','rgb24','-f','rawvideo','-'])
        arr=np.frombuffer(data,np.uint8).reshape(-1,270,480,3);assert len(arr)==6
        canvas=Image.new('RGB',(1440,580),'#151b25');d=ImageDraw.Draw(canvas)
        for k,frame in enumerate(arr):
            x=(k%3)*480;y=(k//3)*290;canvas.paste(Image.fromarray(frame),(x,y));d.text((x+8,y+273),f'frame {start-1+k}',fill='white')
        canvas.save(Q/f'transition-{j:02d}.jpg')
    report={'status':'automated_passed_visual_review_pending','frames':len(frames),'resolution':[1920,1080],'fps':30,'full_decode_clean':'passed','full_decode_captioned':'passed','audio_packet_hash_exact':True,'audio_packet_sha256':sound,'srt_vtt_bytes_exact_to_v4':True,'cues':130,'stable_shot_max_mean_luma_change':max_change,'stable_shots':stable,'visual_review':'pending','full_normal_speed_listening':'NOT_RUN'}
    (Q/'automated.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    manifest=json.loads((O/'delivery-manifest.json').read_text());manifest['automated_qa']=report
    manifest['sha256']=hashlib.sha256(captioned.read_bytes()).hexdigest()
    (O/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='stable_shots'},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
