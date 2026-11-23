"""Assemble exact episode order, offset detached cues, inspect actual encoded compilation."""
from pathlib import Path
import json,re,subprocess,hashlib
from continue_series import ROOT,HERE,episode,captions,stamp,run,PLAN
OUT=ROOT/'output/EP001-EP008';OUT.mkdir(parents=True,exist_ok=True)
QA=OUT/'qa';QA.mkdir(exist_ok=True)
MOVIE='EP001-EP008_sams_apocalypse_1080p.mp4'
def parse(path):
 result=[]
 def sec(t):
  h,m,s,ms=map(int,re.split('[:,]',t));return h*3600+m*60+s+ms/1000
 for i,b in enumerate(path.read_text(encoding='utf8').strip().split('\n\n'),1):
  ls=b.splitlines();assert ls[0]==str(i)
  a,z=ls[1].split(' --> ');result.append([sec(a),sec(z),'\n'.join(ls[2:])])
 return result
files=[];allc=[];chapters=[]
for n in range(1,9):
 ep=ROOT/'episodes/EP001_own-the-store' if n==1 else episode(n)
 f=ep/'output'/f'EP{n:03d}_sams_apocalypse_1080p.mp4';assert f.exists(),f
 c=parse(ep/'output'/f'EP{n:03d}_sams_apocalypse.zh-CN.srt')
 assert c[0][0]==0 and c[-1][1]==60
 expected=json.loads((HERE/'timeline.json').read_text())['subtitles'] if n==1 else captions(n)
 assert c==[[round(a,3),round(b,3),t] for a,b,t in expected],(n,'subtitle mismatch')
 files.append(f);allc.extend([[a+(n-1)*60,b+(n-1)*60,t] for a,b,t in c])
 draft=(ROOT/f'drafts/EP{n:03d}-script-v1.md').read_text();m=re.search(f'EP{n:03d}《(.*?)》',draft)
 chapters.append(dict(episode=n,start=(n-1)*60,end=n*60,title=m[1] if m else '整个超市都是我的',file=str(f.relative_to(ROOT))))
assert all(a[1]<=b[0] for a,b in zip(allc,allc[1:]));assert allc[-1][1]==480
srt=OUT/'EP001-EP008_sams_apocalypse.zh-CN.srt'
srt.write_text('\n\n'.join(f'{i}\n{stamp(a)} --> {stamp(b)}\n{t}' for i,(a,b,t) in enumerate(allc,1))+'\n',encoding='utf8')
vtt='WEBVTT\n\n'+'\n\n'.join(f'{stamp(a,".")} --> {stamp(b,".")}\n{t}' for a,b,t in allc)+'\n'
(OUT/'EP001-EP008_sams_apocalypse.zh-CN.vtt').write_text(vtt,encoding='utf8')
(QA/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2)+'\n')
concat=HERE/'compilation.ffconcat';concat.write_text('ffconcat version 1.0\n'+'\n'.join("file '"+str(p)+"'" for p in files)+'\n')
final=OUT/MOVIE
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat,'-map','0:v:0','-c:v','copy','-an','-sn','-dn','-movflags','+faststart',final])
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(final)]))
assert len(info['streams'])==1
v=info['streams'][0];assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',14400)
assert abs(float(info['format']['duration'])-480)<1/30
(QA/'ffprobe.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
assert parse(srt)==[[round(a,3),round(b,3),t] for a,b,t in allc]
# Decode full 8 minutes, detect unintended full-frame black intervals.
with (QA/'full-decode-blackdetect.log').open('w') as log:
 run(['ffmpeg','-hide_banner','-nostats','-i',final,'-vf','blackdetect=d=0.1:pix_th=0.05:pic_th=0.99','-an','-f','null','-'],stdout=log,stderr=subprocess.STDOUT)
black=re.findall(r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)',(QA/'full-decode-blackdetect.log').read_text())
assert not black,black
# Actual encoded samples from each image and all seven episode joins.
indices=sorted(set([0,14399]+[n*1800+s*225+60 for n in range(8) for s in range(8)]+[n*1800-1 for n in range(1,8)]+[n*1800 for n in range(1,8)]))
expr='+'.join(f'eq(n,{n})' for n in indices)
run(['ffmpeg','-v','error','-y','-i',final,'-vf',f"select='{expr}',scale=640:360",'-fps_mode','vfr',QA/'sample-%03d.jpg'])
(QA/'sample-frames.json').write_text(json.dumps([{'frame':n,'time':n/30,'file':f'sample-{i:03d}.jpg'} for i,n in enumerate(indices,1)],indent=2)+'\n')
run(['ffmpeg','-v','error','-y','-framerate','1','-i',QA/'sample-%03d.jpg','-vf','scale=320:180,tile=4x4:padding=2:margin=2','-frames:v','5',QA/'contact-%02d.jpg'])
# Native HTML video plays exact deliverable; Blob VTT also works when opened from filesystem.
buttons=''.join(f'<button data-time="{c["start"]}">第{c["episode"]}集 · {c["title"]}</button>' for c in chapters)
player='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>山姆末日 · 第1—8集</title><style>body{margin:0;background:#101925;color:#edf3fa;font-family:system-ui,sans-serif}main{max-width:1280px;margin:22px auto;padding:0 18px}h1{font-size:23px}video{width:100%;background:#000;display:block;border-radius:8px}p{color:#b8c6d4;font-size:14px}nav{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}button{border:1px solid #42556c;border-radius:6px;background:#1c2b3c;color:#edf3fa;padding:9px;cursor:pointer}video::cue{font-size:26px;background:rgba(0,0,0,.76);color:white}a{color:#86c8ff}</style><main><h1>丧尸爆发后，我拥有整个山姆超市 · 第1—8集合集</h1><video id="film" controls playsinline preload="metadata" src="MOVIE"><track id="captions" kind="subtitles" srclang="zh-CN" label="第一人称中文字幕" default></video><p>8分钟 · 1080p · 图片运镜漫剧 · 无音轨。字幕为独立外挂，可在播放器切换。</p><nav>BUTTONS</nav><a href="EP001-EP008_sams_apocalypse.zh-CN.srt" download>下载独立SRT字幕</a></main><script>const vtt=CAPTIONS;document.getElementById('captions').src=URL.createObjectURL(new Blob([vtt],{type:'text/vtt'}));const film=document.getElementById('film');document.querySelectorAll('button[data-time]').forEach(b=>b.addEventListener('click',()=>{film.currentTime=Number(b.dataset.time);film.play()}));</script></html>'''.replace('MOVIE',MOVIE).replace('BUTTONS',buttons).replace('CAPTIONS',json.dumps(vtt,ensure_ascii=False))
(OUT/'player.html').write_text(player,encoding='utf8')
report={'episodes':8,'episode_order':[f'EP{n:03d}' for n in range(1,9)],'duration_seconds':480,'resolution':[1920,1080],'fps':30,'frame_count':14400,'video_codec':v['codec_name'],'audio_stream_count':0,'subtitle_stream_count':0,'burned_subtitles':False,'external_srt_cues':len(allc),'subtitle_text_exact':True,'subtitle_timing':'人工阅读节奏，无配音','full_decode':'passed','black_intervals':black,'encoded_samples':len(indices),'gpt_images_in_film':67,'shots':125,'bytes':final.stat().st_size,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'browser_playback':'pending','visual_review':'pending'}
(QA/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text('# 第1—8集合集\n\n- 视频：'+MOVIE+'\n- 字幕：EP001-EP008_sams_apocalypse.zh-CN.srt（UTF-8）\n- 预览：player.html，可切换外挂字幕、按集跳转。\n- 规格：480秒、1920×1080、30fps，只有H.264视频流；无音轨、无烧录或内嵌字幕。\n- 由GPT内置生图、Hypit本地图片运镜生成；保留第一集既有成片。\n- 字幕按阅读节奏排时；没有生成配音。\n- 来源与完整提示词：../../production/hypit/continuation-sources.json。\n- 质量报告：qa/validation.json。\n')
print(json.dumps(report,ensure_ascii=False),flush=True)
