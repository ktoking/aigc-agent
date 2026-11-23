"""Approved EP002–008 -> reusable Hypit sources, detached captions, local output QA."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, struct, subprocess, textwrap
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PLAN=json.loads((HERE/'continuation-plan.json').read_text())
SLUGS={2:'keep-the-door-closed',3:'first-inventory',4:'cold-chain-technician',5:'first-night-apart',6:'dinner-for-two',7:'a-place-to-live',8:'power-outage'}
def episode(n): return ROOT/'episodes'/f'EP{n:03d}_{SLUGS[n]}'
def segdir(ep,s):return ep/f'segment_{s:02d}_{(s-1)*15:02d}-{s*15:02d}s'
def run(args,**kw):return subprocess.run(list(map(str,args)),cwd=ROOT,check=True,**kw)
def stamp(t,sep=','):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}'
def read_script(n):
 text=(ROOT/f'drafts/EP{n:03d}-script-v1.md').read_text()
 blocks=re.findall(r'第一人称正文：\s*\n(.*?)(?=\n### |\Z)',text,re.S)
 assert len(blocks)==4,(n,len(blocks))
 return text,[[line.strip() for line in b.strip().splitlines() if line.strip()] for b in blocks]
def captions(n):
 text,blocks=read_script(n);cues=[]
 for s,lines in enumerate(blocks):
  weights=[len(x)+4 for x in lines];total=sum(weights);elapsed=0
  for i,(line,w) in enumerate(zip(lines,weights)):
   start=s*450+round(elapsed/total*450);elapsed+=w;end=s*450+round(elapsed/total*450)
   # Break long subtitle lines only at punctuation when possible. Text is unchanged.
   if len(line)>23:
    target=len(line)//2;breaks=[m.end() for m in re.finditer('[，。！？、；]',line)]
    candidates=[x for x in breaks if 8<=x<len(line)-7]
    split=min(candidates,key=lambda x:abs(x-target)) if candidates else target
    line=line[:split]+'\n'+line[split:]
   cues.append([start/30,end/30,line])
 assert ''.join(''.join(x.split()) for b in blocks for x in b)==''.join(''.join(c[2].split()) for c in cues)
 return cues
def prepare(n):
 ep=episode(n);out=ep/'output';out.mkdir(parents=True,exist_ok=True)
 assets={}
 for j in [x for x in PLAN if x['episode']==n]:
  p=segdir(ep,j['segment'])/'frames'/f'{j["id"]}.png'
  if not p.exists():raise FileNotFoundError(p)
  w,h=struct.unpack('>II',p.read_bytes()[16:24]);assets[j['id']]={**j,'path':str(p.relative_to(ROOT)),'width':w,'height':h}
 cues=captions(n)
 (out/f'EP{n:03d}_sams_apocalypse.zh-CN.srt').write_text('\n\n'.join(f'{i}\n{stamp(a)} --> {stamp(b)}\n{t}' for i,(a,b,t) in enumerate(cues,1))+'\n')
 (out/f'EP{n:03d}_sams_apocalypse.zh-CN.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(a,".")} --> {stamp(b,".")}\n{t}' for a,b,t in cues)+'\n')
 shots=[]
 for s in range(4):
  # Two full-frame story images per segment; deliberate tighter views change attention.
  for k,(a,b,which) in enumerate([(0,4,1),(4,7.5,1),(7.5,11.5,2),(11.5,15,2)]):
   asset=f'e{n}-{s*2+which:02d}';tight=k%2==1
   scale=[1.105,1.14] if tight else [1.025,1.065]
   if (s+k)%3==1:scale=scale[::-1]
   shots.append(dict(id=f'shot-{len(shots)+1:02d}',asset=asset,start=s*15+a,end=s*15+b,scale=scale,x=[-10,10] if k%2 else [8,-8],y=[0,-4],transition=0.1 if tight else 0.2))
 data={'episode':n,'duration':60,'fps':30,'assets':assets,'shots':shots,'subtitles':cues}
 (HERE/f'EP{n:03d}-timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (ep/'image-manifest.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
 lines=['<?svml using="@hypit/markup@1"?>','<svml>']
 for alias,pkg in [('time','timeline-author'),('space','spatial'),('media','media'),('visual','visual-track'),('film','film'),('html','html-video')]:lines.append(f'<import as="{alias}" from="@hypit/{pkg}@1"/>')
 lines+=['<import as="look" source="./look.svs"/>','<time:Clock id="clock" frame-rate="30"/>','<time:Timeline id="program" clock={clock} end="60s">']
 for i,s in enumerate(shots):lines.append(f'<time:Window id="{s["id"]}" from="{s["start"]}s" until="{min(60,s["end"]+0.2)}s"/>')
 lines+=['</time:Timeline>','<space:Canvas id="canvas" width="1920" height="1080"/>']
 for key,a in assets.items():lines += [f'<space:Extent id="extent-{key}" width="{a["width"]}" height="{a["height"]}"/>',f'<media:Image id="asset-{key}" src="../../{escape(a["path"])}"/>']
 for i,s in enumerate(shots):
  lines.append(f'<visual:Motion id="motion-{s["id"]}">')
  duration=min(60,s['end']+.2)-s['start']
  for at,ratio,opacity in [('start',0,1 if i==0 else 0),('6f',.2/duration,1),('end',1,1)]:
   scale=s['scale'][0]+(s['scale'][1]-s['scale'][0])*ratio;x=s['x'][0]+(s['x'][1]-s['x'][0])*ratio;y=s['y'][0]+(s['y'][1]-s['y'][0])*ratio
   lines.append(f'<visual:Pose at="{at}" scale="{scale:.6f}" x="{x:.4f}" y="{y:.4f}" origin-x="0.5" origin-y="0.5" opacity="{opacity}" easing="linear"/>')
  lines.append('</visual:Motion>')
 lines.append('<visual:Track id="picture" timeline={program.timeline}>')
 for i,s in enumerate(shots):lines.append(f'<visual:Clip id="{s["id"]}" image={{asset-{s["asset"]}}} extent={{extent-{s["asset"]}}} during={{program.{s["id"]}}} frame={{canvas.bounds}} z="{i+1}" fit="cover" motion={{motion-{s["id"]}}}/>')
 lines+=['</visual:Track>','<film:Film id="main" canvas={canvas.canvas} timeline={program.timeline} appearance={look.film.main}>','<film:Track source={picture.visual}/>','</film:Film>','<html:Video id="final" composition={main.composition} timeline={program.timeline}/>','</svml>']
 (HERE/f'EP{n:03d}.svml').write_text('\n'.join(lines)+'\n')
 (HERE/f'EP{n:03d}.svrun').write_text(f'<?svml using="@hypit/markup/run@1"?>\n<svrun version="1"><author source="./EP{n:03d}.svml"/><target output="final.video"/></svrun>\n')
 draft,blocks=read_script(n)
 (ep/'episode.md').write_text(draft.replace('状态：后续剧本第一稿，约60秒、四段；未生成图片或视频。','状态：用户已通过，按已通过正文制作，60秒四段，无配音，独立字幕。'))
 overview=['# 镜头表','','16:9 / 1920×1080 / 30fps / 60秒。每段2张GPT故事图，使用局部重构图和缓推/横移。无音轨、无烧录字幕。','','| 镜头 | 时间 | 图像 | 画面 |','| --- | --- | --- | --- |']
 for s in shots:overview.append(f'| {s["id"]} | {s["start"]}–{s["end"]}s | {s["asset"]} | {assets[s["asset"]]["description"]} |')
 (ep/'overview-storyboard.md').write_text('\n'.join(overview)+'\n')
 (ep/'image-manifest.md').write_text('# GPT 图片清单\n\n来源与完整提示词：`../../production/hypit/continuation-sources.json`。\n\n'+'\n'.join(f'- `{k}`：`{a["path"]}`，{a["width"]}×{a["height"]}，{a["title"]}。' for k,a in assets.items())+'\n')
 for s in range(1,5):
  d=segdir(ep,s);(d/'output').mkdir(exist_ok=True);a=(s-1)*15;b=s*15
  ss=[x for x in shots if a<=x['start']<b]
  (d/'storyboard.md').write_text('# 分段故事板\n\n全片 '+f'{a}–{b}秒。\n\n'+'\n'.join(f'- {x["start"]}–{x["end"]}秒：{assets[x["asset"]]["title"]}；素材 frames/{x["asset"]}.png；缩放{x["scale"]}，位移{x["x"]}。' for x in ss)+'\n\n第一人称独立字幕：\n\n'+'\n'.join(blocks[s-1])+'\n')
  for label,sh in [('first',ss[0]),('last',ss[-1])]:
   (d/f'{label}-frame.md').write_text(f'# {"首" if label=="first" else "尾"}帧\n\n素材 `frames/{sh["asset"]}.png`；{assets[sh["asset"]]["description"]}。\n保留人物衣帽、道具和门状态；实际视频提取为 `frames/{label}-frame.png`。\n')
  instruction=f'16:9，15秒，1920×1080，30fps，干净彩色二维漫画。\n使用本地Hypit缓推、缓拉、横移与6帧叠化；按storyboard.md顺序构图。\n角色：男主圆白头黑点眼，青绿帽、黄帽衫、蓝马甲；许棠低马尾、橘维修外套、灰裤蓝灰工具包。店长棕短发黑框眼镜红挂绳，始终在门外。\n全片时间{a}–{b}秒，首尾图继承见first-frame.md和last-frame.md；局部重构图由EP{n:03d}.svml精确给出。\n不调用视频API。无人声、无音乐、无音效，独立SRT，不烧录字幕。\n无人物肢体动画，仅静帧运镜。禁止黑边、水印、文字叠加、人物换装、门状态混乱和无限资源。\n'
  (d/'prompt.md').write_text('# 本地合成指令\n\n'+instruction);(d/'director-promt.txt').write_text(instruction)
  (d/'api-request.md').write_text(f'# 执行记录\n\n- 本地Hypit 0.3.1 + FFmpeg；16:9，15秒，1080p，30fps。\n- 运行：production/hypit/EP{n:03d}.svrun。\n- GPT 内置imagegen生成图片，无外部图片API。\n- 视频API：未提交，无API任务ID。\n- Build结果见本段output/render-record.json；失败保留图片，只修编排。\n')
 print(json.dumps({'prepared':n,'images':len(assets),'shots':len(shots),'cues':len(cues)},ensure_ascii=False),flush=True)
def finish(n):
 ep=episode(n);out=ep/'output';qa=out/'qa';qa.mkdir(exist_ok=True)
 build=json.loads((HERE/f'EP{n:03d}-build.json').read_text())['build']
 assert build['work']['outcome']=='complete' and build['result']['state']=='complete',build
 raw=HERE/'output'/f'EP{n:03d}-{build["id"]}.mp4';raw.parent.mkdir(exist_ok=True)
 if not raw.exists():run(['hypit','get',build['id'],'--output','final.video','--to',raw])
 final=out/f'EP{n:03d}_sams_apocalypse_1080p.mp4'
 run(['ffmpeg','-v','error','-y','-i',raw,'-map','0:v:0','-c:v','copy','-an','-sn','-dn','-movflags','+faststart',final])
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(final)]))
 assert len(info['streams'])==1
 v=info['streams'][0];assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',1800)
 assert abs(float(info['format']['duration'])-60)<1/30
 (qa/'ffprobe.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
 times=sorted(set([0,449,450,899,900,1349,1350,1799]+[round(s*30) for s in [2,9,17,24,32,39,47,54]]))
 expr='+'.join(f'eq(n,{t})' for t in times)
 run(['ffmpeg','-v','error','-y','-i',final,'-vf',f"select='{expr}'",'-fps_mode','vfr',qa/'frame-%02d.png'])
 lookup={t:qa/f'frame-{i:02d}.png' for i,t in enumerate(times,1)}
 for s in range(1,5):
  d=segdir(ep,s)
  for label,t in [('first',(s-1)*450),('last',s*450-1)]:shutil.copy2(lookup[t],d/f'frames/{label}-frame.png')
  (d/'output/render-record.json').write_text(json.dumps({'build_id':build['id'],'episode':n,'first_frame':(s-1)*450,'end_frame_exclusive':s*450,'fps':30,'video_api_submitted':False},indent=2)+'\n')
 run(['ffmpeg','-v','error','-y','-framerate','1','-i',qa/'frame-%02d.png','-vf','scale=384:216,tile=4x4:padding=2:margin=2','-frames:v','1',qa/'contact-sheet.jpg'])
 report={'episode':n,'build_id':build['id'],'outcome':'complete','duration':60,'resolution':[1920,1080],'fps':30,'frames':1800,'audio_streams':0,'subtitle_streams':0,'srt_cues':len(captions(n)),'approved_script_exact_match':True,'gpt_images':8,'shots':16,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'bytes':final.stat().st_size,'visual_review':'pending'}
 (qa/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 (ep/'qa-checklist.md').write_text(f'# 第{n}集验收\n\n- Hypit Build `{build["id"]}`：complete。\n- 1080p，30fps，1800帧，60秒，无音轨或内嵌字幕流。\n- 独立SRT与已通过正文一致。\n- 8张GPT图片，16个本地运镜镜头；实际编码抽帧16张，含四段首尾。\n- 目视与整片解码结果见 output/qa/validation.json。\n- 未发布，未提交视频生成API。\n')
 print(json.dumps(report,ensure_ascii=False),flush=True)
def build(n):
 prepare(n)
 with (HERE/f'EP{n:03d}-check.log').open('w') as f:run(['hypit','check',f'production/hypit/EP{n:03d}.svml'],stdout=f,stderr=subprocess.STDOUT)
 with (HERE/f'EP{n:03d}-plan.json').open('w') as f:run(['hypit','plan',f'production/hypit/EP{n:03d}.svrun','--json'],stdout=f)
 with (HERE/f'EP{n:03d}-build.json').open('w') as f:run(['hypit','build',f'production/hypit/EP{n:03d}.svrun','--follow','--json'],stdout=f)
 finish(n)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','build','finish']);p.add_argument('episodes',nargs='+',type=int);a=p.parse_args()
 for n in a.episodes:globals()[a.action](n)
