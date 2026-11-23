"""Rebuild EP001-008 from accepted stills with per-sentence continuous timing."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json, subprocess, shutil, hashlib, argparse
ROOT=Path(__file__).resolve().parents[3]
PROD=ROOT/'production/v2'
OUT=ROOT/'output/EP001-EP008-v2'
HANDOFF=ROOT/'handoff/cloud-codex-20261018-v2'
PLAN=json.loads((HANDOFF/'estimated-timing/timing-plan.json').read_text())
SCRIPTS=json.loads((HANDOFF/'scripts-and-shots.json').read_text())

def run(args,log=None):
    if log:
        with log.open('w') as f:subprocess.run(list(map(str,args)),check=True,stdout=f,stderr=subprocess.STDOUT)
    else:subprocess.run(list(map(str,args)),check=True)

def make_shots(ep):
    n=ep['episode'];old=json.loads((ROOT/'production/hypit'/('timeline.json' if n==1 else f'EP{n:03d}-timeline.json')).read_text())
    assets=old['assets']
    if n==1:
        for a in assets.values():
            a['path']=str(Path('episodes/EP001_own-the-store')/f"segment_{a['segment']:02d}_{(a['segment']-1)*15:02d}-{a['segment']*15:02d}s"/'frames'/a['file'])
        cue_groups=[('cart',1,1),('work',2,2),('cart',3,3),('flee',4,5),('monitor',6,6),('shutter',7,7),('night',8,8),('resources',9,10),('cold',11,11),('cart',12,13),('bed',14,14),('manager',15,17),('keys',18,18)]
        shots=[]
        for i,((key,a,b),style) in enumerate(zip(cue_groups,old['shots'])):
            shots.append({'id':f'shot-{i+1:02d}','asset':key,'start_frame':ep['cues'][a-1]['start_frame'],'end_frame_exclusive':ep['cues'][b-1]['end_frame_exclusive'],'scale':style['scale'],'x':style['x'],'y':style['y'],'cues':[a,b]})
    else:
        shots=[]
        for i,c in enumerate(ep['cues']):
            seg=c['segment'];j=i%4;key=f'e{n}-{(seg-1)*2+(1 if j<2 else 2):02d}'
            tight=j%2==1;scale=[1.105,1.14] if tight else [1.025,1.065]
            if (seg+j)%3==1:scale=scale[::-1]
            shots.append({'id':f'shot-{i+1:02d}','asset':key,'start_frame':c['start_frame'],'end_frame_exclusive':c['end_frame_exclusive'],'scale':scale,'x':[-10,10] if j%2 else [8,-8],'y':[0,-4],'cues':[i+1,i+1]})
    assert shots[0]['start_frame']==0 and shots[-1]['end_frame_exclusive']==ep['frame_count']
    assert all(a['end_frame_exclusive']==b['start_frame'] for a,b in zip(shots,shots[1:]))
    for a in assets.values():assert (ROOT/a['path']).is_file(),a['path']
    return assets,shots

def render_shot(job):
    n,shot,asset=job
    folder=PROD/'shots'/f'EP{n:03d}';folder.mkdir(parents=True,exist_ok=True)
    dest=folder/f"{shot['id']}.mp4"
    frames=shot['end_frame_exclusive']-shot['start_frame'];den=max(1,frames-1)
    z0,z1=shot['scale'];x0,x1=shot['x'];y0,y1=shot['y']
    z=f'{z0}+({z1-z0})*on/{den}'
    x=f'iw/2-iw/zoom/2-({x0}+({x1-x0})*on/{den})'
    y=f'ih/2-ih/zoom/2-({y0}+({y1-y0})*on/{den})'
    vf=f'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z={z}:x={x}:y={y}:d={frames}:s=1920x1080:fps=30,format=yuv420p'
    cmd=['ffmpeg','-v','error','-y','-i',ROOT/asset['path'],'-vf',vf,'-frames:v',frames,'-an','-sn','-dn','-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-r','30','-pix_fmt','yuv420p','-video_track_timescale','15360','-movflags','+faststart',dest]
    run(cmd,PROD/'logs'/f'EP{n:03d}-{shot["id"]}.log')
    return n,shot['id'],str(dest)

def main():
    PROD.mkdir(parents=True,exist_ok=True);(PROD/'logs').mkdir(exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    shutil.copy2(HANDOFF/'estimated-timing/timing-plan.json',PROD/'timing-plan.json')
    jobs=[];episodes=[]
    for ep in PLAN['episodes']:
        n=ep['episode'];assets,shots=make_shots(ep)
        draft=next(x for x in SCRIPTS['episodes'] if x['episode']==n)
        epdir=ROOT/'episodes'/f"EP{n:03d}_{draft['slug']}"/'v2';epout=epdir/'output';epout.mkdir(parents=True,exist_ok=True)
        authored={**ep,'assets':assets,'shots':shots,'transition':'direct_cuts_no_added_frames','engine':'FFmpeg libx264','audio':False,'subtitles_burned':False}
        (PROD/f'EP{n:03d}-timeline.json').write_text(json.dumps(authored,ensure_ascii=False,indent=2)+'\n')
        (epdir/'overview-storyboard.md').write_text(f"# EP{n:03d} v2镜头表\n\n5个非标点字/秒；{ep['duration_seconds']}秒，30fps，无音轨，外挂字幕。\n\n| 镜头 | 帧区间(尾不含) | 素材 | 对应台词 |\n| --- | --- | --- | --- |\n"+'\n'.join(f"| {s['id']} | {s['start_frame']}—{s['end_frame_exclusive']} | {s['asset']} | {s['cues']} |" for s in shots)+'\n')
        for ext in ['srt','vtt']:
            shutil.copy2(HANDOFF/f'estimated-timing/EP{n:03d}_text-estimate.{ext}',epout/f'EP{n:03d}_sams_apocalypse_v2.zh-CN.{ext}')
            shutil.copy2(epout/f'EP{n:03d}_sams_apocalypse_v2.zh-CN.{ext}',OUT/f'EP{n:03d}_sams_apocalypse_v2.zh-CN.{ext}')
        shutil.copy2(HANDOFF/f'estimated-timing/EP{n:03d}_narration.txt',epout/'narration.txt')
        for seg in ep['segments']:
            segdir=epdir/seg['directory'];(segdir/'frames').mkdir(parents=True,exist_ok=True);(segdir/'output').mkdir(exist_ok=True)
            selected=[s for s in shots if s['start_frame']<seg['end_frame_exclusive'] and s['end_frame_exclusive']>seg['start_frame']]
            (segdir/'storyboard.md').write_text('# 本段镜头\n\n'+ '\n'.join(f"- {s['id']}：{s['start_frame']/30:.2f}—{s['end_frame_exclusive']/30:.2f}s；{s['asset']}" for s in selected)+'\n')
        jobs +=[(n,s,assets[s['asset']]) for s in shots]
        episodes.append((ep,epdir))
    print(json.dumps({'stage':'rendering','shots':len(jobs),'frames':PLAN['frame_count'],'seconds':PLAN['duration_seconds']},ensure_ascii=False),flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures=[pool.submit(render_shot,j) for j in jobs]
        for i,f in enumerate(as_completed(futures),1):
            n,s,_=f.result()
            if i%10==0 or i==len(jobs):print(f'rendered {i}/{len(jobs)} EP{n:03d} {s}',flush=True)
    final_files=[]
    for ep,epdir in episodes:
        n=ep['episode'];auth=json.loads((PROD/f'EP{n:03d}-timeline.json').read_text());concat=PROD/f'EP{n:03d}.ffconcat'
        paths=[PROD/'shots'/f'EP{n:03d}'/f"{s['id']}.mp4" for s in auth['shots']]
        concat.write_text('ffconcat version 1.0\n'+'\n'.join("file '"+str(x.resolve()).replace("'","'\\''")+"'" for x in paths)+'\n')
        target=OUT/f'EP{n:03d}_sams_apocalypse_v2.mp4'
        run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat,'-map','0:v:0','-c:v','copy','-an','-sn','-dn','-movflags','+faststart',target])
        shutil.copy2(target,epdir/'output'/target.name);final_files.append(target)
        print(f'assembled EP{n:03d}: {target.stat().st_size} bytes',flush=True)
    concat=PROD/'compilation.ffconcat';concat.write_text('ffconcat version 1.0\n'+'\n'.join("file '"+str(x.resolve())+"'" for x in final_files)+'\n')
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat,'-map','0:v:0','-c:v','copy','-an','-sn','-dn','-movflags','+faststart',OUT/'EP001-EP008_sams_apocalypse_v2.mp4'])
    for ext in ['srt','vtt']:shutil.copy2(HANDOFF/f'estimated-timing/EP001-EP008_text-estimate.{ext}',OUT/f'EP001-EP008_sams_apocalypse_v2.zh-CN.{ext}')
    print('RENDER COMPLETE',flush=True)

if __name__=='__main__':main()
