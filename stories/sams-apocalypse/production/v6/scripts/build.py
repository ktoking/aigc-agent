"""Silent clean compilation: 3-frame cue gaps, 3-frame dissolves inside those gaps."""
from pathlib import Path
import json,subprocess,hashlib,zipfile,html
from PIL import Image,ImageOps

P=Path(__file__).resolve().parents[1];R=P.parents[1];SOURCE=R/'production/v5'
O=R/'output/EP001-EP008-v6';O.mkdir(parents=True,exist_ok=True)
T=json.loads((SOURCE/'timeline.json').read_text());FPS=30;GAP=3;W,H=1920,1080
NAME='EP001-EP008_sams_apocalypse_v6_silent'

def stamp(frame,sep=','):
    ms=round(frame*1000/FPS);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}'

def main():
    (P/'logs').mkdir(parents=True,exist_ok=True);(P/'qa').mkdir(exist_ok=True)
    jobs={j['id']:j for j in T['jobs']};cues=[]
    for i,c in enumerate(T['cues']):
        a,b=c['output_start_frame'],c['output_end_frame_exclusive']
        matching=[s for s in T['shots'] if s['start_frame']<=a and s['end_frame_exclusive']>=b]
        assert len(matching)==1,(i,matching)
        cues.append({'index':i+1,'episode':c['episode'],'segment':c['segment'],'text':c['text'],'source_start_frame':a,'source_end_frame_exclusive':b,'start_frame':a+i*GAP,'end_frame_exclusive':b+i*GAP,'asset':matching[0]['asset'],'gap_after_frames':GAP if i<len(T['cues'])-1 else 0})
    total=T['frames']+(len(cues)-1)*GAP
    assert total==7730 and cues[0]['start_frame']==0 and cues[-1]['end_frame_exclusive']==total
    assert all(b['start_frame']-a['end_frame_exclusive']==GAP for a,b in zip(cues,cues[1:]))
    cache={}
    def picture(key):
        if key not in cache:
            with Image.open(SOURCE/jobs[key]['path']) as im:cache[key]=ImageOps.fit(im.convert('RGB'),(W,H),method=Image.Resampling.LANCZOS)
        return cache[key]
    target=O/f'{NAME}.mp4'
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-map','0:v:0','-an','-sn','-dn','-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','18','-bf','0','-threads','4','-pix_fmt','yuv420p','-movflags','+faststart',str(target)]
    transitions=[];count=0;last_key=None;raw=None
    with (P/'logs/encode.log').open('w') as log:
        enc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
        try:
            for i,c in enumerate(cues):
                assert count==c['start_frame']
                im=picture(c['asset'])
                if last_key!=c['asset']:raw=im.tobytes();last_key=c['asset']
                for _ in range(c['end_frame_exclusive']-c['start_frame']):enc.stdin.write(raw);count+=1
                assert count==c['end_frame_exclusive']
                if i+1<len(cues):
                    nxt=cues[i+1];changed=nxt['asset']!=c['asset']
                    if changed:transitions.append({'start_frame':count,'end_frame_exclusive':count+GAP,'frames':GAP,'old_asset':c['asset'],'new_asset':nxt['asset'],'in_subtitle_gap':True})
                    next_im=picture(nxt['asset']) if changed else None
                    for k in range(GAP):
                        frame=Image.blend(im,next_im,(k+1)/GAP).tobytes() if changed else raw
                        enc.stdin.write(frame);count+=1
                if (i+1)%20==0:print(f'rendered {i+1}/{len(cues)} cues; {count}/{total} frames',flush=True)
        finally:enc.stdin.close()
        assert enc.wait()==0
    assert count==total and len(transitions)==68
    srt=[];vtt=[]
    for c in cues:
        srt.append(f"{c['index']}\n{stamp(c['start_frame'])} --> {stamp(c['end_frame_exclusive'])}\n{c['text']}")
        vtt.append(f"{stamp(c['start_frame'],'.')} --> {stamp(c['end_frame_exclusive'],'.')}\n{c['text']}")
    (O/f'{NAME}.zh-CN.srt').write_text('\n\n'.join(srt)+'\n')
    (O/f'{NAME}.zh-CN.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(vtt)+'\n')
    oldchap=json.loads((R/'output/EP001-EP008-v5/chapters.json').read_text());chapters=[]
    for chapter in oldchap:
        cc=[c for c in cues if c['episode']==chapter['episode']]
        chapters.append({**chapter,'start_seconds':cc[0]['start_frame']/FPS,'end_seconds':(cc[-1]['end_frame_exclusive']+cc[-1]['gap_after_frames'])/FPS})
    (O/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2)+'\n')
    plan={'version':6,'source_version':5,'fps':FPS,'width':W,'height':H,'frames':total,'duration_seconds':total/FPS,'cue_gap_frames':GAP,'cue_gap_seconds':0.1,'transition_frames':GAP,'transition_seconds':0.1,'transition_policy':'inside existing 3-frame inter-cue gap; no additional transition padding','audio':False,'subtitles_burned':False,'subtitles_embedded':False,'camera':'locked_static','cues':cues,'transitions':transitions,'assets':jobs}
    (P/'timeline.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(O/'EP001-EP008_v6_subtitles.zip','w',zipfile.ZIP_DEFLATED) as z:
        for suffix in ['srt','vtt']:z.write(O/f'{NAME}.zh-CN.{suffix}',f'{NAME}.zh-CN.{suffix}')
        z.write(O/'chapters.json','chapters.json')
    manifest={k:plan[k] for k in ['version','source_version','fps','width','height','frames','duration_seconds','cue_gap_frames','cue_gap_seconds','transition_frames','transition_seconds','transition_policy','audio','subtitles_burned','subtitles_embedded','camera']}
    manifest.update({'status':'rendered_pending_qa','cue_count':len(cues),'gap_count':len(cues)-1,'dissolve_count':len(transitions),'added_seconds':(total-T['frames'])/FPS,'cue_durations_preserved':True,'subtitle_text_preserved':True,'video':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    (O/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    buttons=''.join(f'<button data-seek="{c["start_seconds"]}">EP{c["episode"]:03d} · {html.escape(c["title"])}</button>' for c in chapters)
    page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>山姆八集合集 · 无声无字 v6</title><style>body{background:#111923;color:#f2f5f9;font:16px system-ui,"PingFang SC",sans-serif;margin:0}main{max-width:1100px;margin:28px auto;padding:0 18px}h1{font-size:26px}p{line-height:1.8;color:#b6c5d6}video{width:100%;background:black;border-radius:10px}a{color:#9bd7ff}button{background:#23384d;color:white;border:1px solid #4c647c;border-radius:7px;padding:10px 13px;margin:5px 7px 5px 0}.links{display:flex;gap:20px;flex-wrap:wrap;margin:24px 0}</style><main><h1>丧尸爆发后，我拥有整个山姆超市</h1><p>八集合集 · 无声音、无画内字幕 · 4分17.67秒<br>每句间隔0.1秒，换图叠化0.1秒；叠化位于句间间隔内。</p><video controls playsinline preload="metadata" src="NAME.mp4"></video><p id="status">点击播放</p><button id="play">从头播放</button><button id="speed">播放速度 1×</button><nav>CHAPTERS</nav><div class="links"><a href="NAME.mp4" download>下载无声无字视频</a><a href="NAME.zh-CN.srt" download>下载对应SRT</a><a href="NAME.zh-CN.vtt" download>下载对应VTT</a><a href="EP001-EP008_v6_subtitles.zip" download>下载字幕包</a></div><p>字幕文件单独交付，播放器不叠加字幕。Cloudflare临时分享需本机保持在线。</p></main><script>const v=document.querySelector('video'),s=document.querySelector('#status');document.querySelector('#play').onclick=()=>{v.currentTime=0;v.play().catch(()=>{})};document.querySelector('#speed').onclick=()=>{const r=[1,1.25,1.5,2,4,8];v.playbackRate=r[(r.indexOf(v.playbackRate)+1)%r.length];document.querySelector('#speed').textContent='播放速度 '+v.playbackRate+'×'};document.querySelectorAll('[data-seek]').forEach(b=>b.onclick=()=>{v.currentTime=+b.dataset.seek;v.play().catch(()=>{})});v.ontimeupdate=()=>s.textContent=v.currentTime.toFixed(2)+' / '+v.duration.toFixed(2)+' 秒';v.onended=()=>s.textContent='播放完毕';v.onerror=()=>s.textContent='播放错误：'+v.error?.message;</script></html>'''.replace('NAME',NAME).replace('CHAPTERS',buttons)
    (O/'index.html').write_text(page)
    print(json.dumps(manifest,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
