from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,hashlib,shutil,zipfile,html
ROOT=Path(__file__).resolve().parents[3];PROD=ROOT/'production/v2';OUT=ROOT/'output/EP001-EP008-v2';QA=OUT/'qa';QA.mkdir(exist_ok=True)
plan=json.loads((PROD/'timing-plan.json').read_text())
source=json.loads((ROOT/'handoff/cloud-codex-20261018-v2/scripts-and-shots.json').read_text())

def run(args):return subprocess.run(list(map(str,args)),check=True,capture_output=True,text=True)
def verify(ep):
 n=ep['episode'];path=OUT/f'EP{n:03d}_sams_apocalypse_v2.mp4'
 probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',path]).stdout)
 v=probe['streams'][0];assert len(probe['streams'])==1
 assert(v['codec_type'],v['codec_name'],v['width'],v['height'],v['r_frame_rate'],v['pix_fmt'])==('video','h264',1920,1080,'30/1','yuv420p')
 assert int(v['nb_read_frames'])==ep['frame_count']
 assert abs(float(probe['format']['duration'])-ep['duration_seconds'])<.001
 run(['ffmpeg','-v','error','-i',path,'-f','null','-'])
 auth=json.loads((PROD/f'EP{n:03d}-timeline.json').read_text())
 sample_frames=sorted(set([s['start_frame'] for s in auth['shots']]+[s['end_frame_exclusive']-1 for s in auth['shots']]+[s['start_frame'] for s in ep['segments']]+[s['end_frame_exclusive']-1 for s in ep['segments']]))
 q=QA/f'EP{n:03d}';q.mkdir(exist_ok=True)
 expr='+'.join(f'eq(n,{f})' for f in sample_frames)
 run(['ffmpeg','-v','error','-y','-i',path,'-vf',f"select='{expr}'",'-fps_mode','vfr',q/'frame-%03d.png'])
 lookup={f:q/f'frame-{i:03d}.png' for i,f in enumerate(sample_frames,1)}
 epdir=ROOT/'episodes'/f"EP{n:03d}_{source['episodes'][n-1]['slug']}"/'v2'
 for s in ep['segments']:
  d=epdir/s['directory']
  for label,frame in [('first',s['start_frame']),('last',s['end_frame_exclusive']-1)]:
   shutil.copy2(lookup[frame],d/f'frames/{label}-frame.png')
   (d/f'{label}-frame.md').write_text(f'# {label} frame\n\n从本轮编码MP4实际第{frame}帧提取，30fps。源：{path.name}。\n')
  instruction=f"16:9，1920×1080，30fps，干净彩色二维漫画；实际时间{s['start_frame']/30:.2f}—{s['end_frame_exclusive']/30:.2f}秒。\n采用本地FFmpeg静帧缓推/缓拉/轻横移，按本轮EP{n:03d}-timeline.json执行。干净跳切，不加转场等待。\n约5字/秒，字幕句间0帧空档；配音由用户后期制作，本次无音轨，不烧录字幕，外挂SRT/VTT。\n保持已有角色衣帽、空间、门、伤口、道具和光线，不重复生图，不生成视频API任务。\n"
  (d/'prompt.md').write_text(instruction);(d/'director-promt.txt').write_text(instruction)
  (d/'api-request.md').write_text('# 执行记录\n\nFFmpeg libx264本地渲染，未提交视频生成API，无API任务ID。源时间线位于production/v2/，命令和日志已保留。\n')
  (d/'output/render-record.json').write_text(json.dumps({'episode':n,'frame_range':[s['start_frame'],s['end_frame_exclusive']],'engine':'FFmpeg','video_api_submitted':False},indent=2)+'\n')
 run(['ffmpeg','-v','error','-y','-framerate','1','-i',q/'frame-%03d.png','-vf','scale=384:216,tile=6x6:padding=2:margin=2','-frames:v','1',q/'contact-sheet.jpg'])
 record={'episode':n,'frames':ep['frame_count'],'seconds':ep['duration_seconds'],'audio_streams':0,'subtitle_streams':0,'cue_count':len(ep['cues']),'full_decode':'passed','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'visual_review':'pending','audio_alignment':'NOT_RUN'}
 (q/'ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n');(q/'validation.json').write_text(json.dumps(record,indent=2)+'\n')
 (epdir/'qa-checklist.md').write_text('# v2验收\n\n'+json.dumps(record,ensure_ascii=False,indent=2)+'\n')
 (epdir/'image-manifest.json').write_text(json.dumps(auth['assets'],ensure_ascii=False,indent=2)+'\n')
 print(f"verified EP{n:03d}: {ep['duration_seconds']}s, {ep['frame_count']} frames",flush=True)
 return record

records=list(ThreadPoolExecutor(max_workers=3).map(verify,plan['episodes']))
comp=OUT/'EP001-EP008_sams_apocalypse_v2.mp4'
probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',comp]).stdout)
assert len(probe['streams'])==1 and int(probe['streams'][0]['nb_read_frames'])==plan['frame_count']
assert abs(float(probe['format']['duration'])-plan['duration_seconds'])<.001
full=run(['ffmpeg','-hide_banner','-i',comp,'-vf','blackdetect=d=0.1:pix_th=0.01','-an','-f','null','-'])
assert 'black_start:' not in full.stderr
(QA/'full-decode-blackdetect.log').write_text(full.stderr)
(QA/'compilation-ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n')
chapters=[];offset=0
for e in plan['episodes']:
 chapters.append({'episode':e['episode'],'title':e['title'],'start_seconds':offset/30,'duration_seconds':e['duration_seconds'],'video':f"EP{e['episode']:03d}_sams_apocalypse_v2.mp4",'srt':f"EP{e['episode']:03d}_sams_apocalypse_v2.zh-CN.srt"});offset+=e['frame_count']
(OUT/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(OUT/'EP001-EP008_v2_subtitles.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.glob('*.srt')):z.write(p,p.name)
manifest={'status':'rendered_technical_checks_passed','cps':5,'duration_seconds':plan['duration_seconds'],'frame_count':plan['frame_count'],'resolution':[1920,1080],'fps':30,'audio_streams':0,'subtitle_streams':0,'subtitles_burned':False,'subtitle_timing':'text estimate, not audio aligned','cue_gap_frames':0,'cue_overlap_frames':0,'episodes':records,'compilation_sha256':hashlib.sha256(comp.read_bytes()).hexdigest(),'compilation_bytes':comp.stat().st_size,'full_decode':'passed','unexpected_black_intervals':[],'visual_review':'pending','browser_playback':'pending'}
(OUT/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.txt').write_text('山姆末日漫画 EP001—EP008 v2\n按5字/秒重排；总时长343.6秒。无音轨，不烧录字幕，独立SRT/VTT。\n字幕为文字估算稿，配音由用户后期制作。\n单集和合集均重新渲染，原版保留。\n')
buttons=''.join(f'<button data-seek="{c["start_seconds"]}">EP{c["episode"]:03d} · {html.escape(c["title"])}</button>' for c in chapters)
rows=''.join(f'<tr><td>EP{c["episode"]:03d}</td><td>{html.escape(c["title"])}</td><td>{c["duration_seconds"]:.1f}秒</td><td><a href="{c["video"]}" download>视频</a> · <a href="{c["srt"]}" download>字幕</a></td></tr>' for c in chapters)
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>山姆末日漫画 · 1—8集 v2</title><style>body{margin:0;background:#10131b;color:#eef0f8;font:16px system-ui,"PingFang SC",sans-serif}main{max-width:1120px;margin:32px auto;padding:0 20px}h1{font-size:28px}p{color:#b8c3d7;line-height:1.8}video{width:100%;background:#000;aspect-ratio:16/9;border-radius:12px}video::cue{font-size:26px;color:#fff;background:rgba(0,0,0,.65)}a{color:#8fcbff}button{background:#253349;border:1px solid #455878;color:#fff;padding:10px 14px;border-radius:8px;margin:6px 6px 6px 0;cursor:pointer}.downloads{display:flex;gap:22px;flex-wrap:wrap;margin:22px 0}table{width:100%;border-collapse:collapse}td{padding:12px 8px;border-bottom:1px solid #2d3544}#status{font-size:14px}</style><main><h1>丧尸爆发后，我拥有整个山姆超市</h1><p>第1—8集 · 紧凑版 v2 · 5分43.6秒<br>无音轨视频 · 外挂字幕可开关 · 配音由你后期制作</p><video id="film" controls preload="metadata" playsinline><source src="EP001-EP008_sams_apocalypse_v2.mp4" type="video/mp4"><track kind="subtitles" src="EP001-EP008_sams_apocalypse_v2.zh-CN.vtt" srclang="zh-CN" label="简体中文" default></video><p id="status">字幕按约5字/秒连续排时；尚未与后期配音对齐。</p><div><button id="captions">开关字幕</button><button id="rate">切换播放速度</button></div><nav>CHAPTERS</nav><div class="downloads"><a href="EP001-EP008_sams_apocalypse_v2.mp4" download>下载合集 MP4</a><a href="EP001-EP008_sams_apocalypse_v2.zh-CN.srt" download>下载合集 SRT</a><a href="EP001-EP008_v2_subtitles.zip" download>下载全部字幕 ZIP</a></div><table><tbody>ROWS</tbody></table><p>视频与字幕均为v2新版，请配套使用。</p></main><script>const v=document.querySelector('video');document.querySelectorAll('[data-seek]').forEach(b=>b.onclick=()=>{v.currentTime=Number(b.dataset.seek);v.play().catch(()=>{})});document.querySelector('#captions').onclick=()=>{const t=v.textTracks[0];t.mode=t.mode==='showing'?'hidden':'showing'};document.querySelector('#rate').onclick=()=>{const rates=[1,1.25,1.5,2,4,8];v.playbackRate=rates[(rates.indexOf(v.playbackRate)+1)%rates.length];document.querySelector('#rate').textContent='播放速度 '+v.playbackRate+'×'};</script></html>'''.replace('CHAPTERS',buttons).replace('ROWS',rows)
(OUT/'index.html').write_text(page);shutil.copy2(OUT/'index.html',OUT/'player.html')
print(json.dumps({'complete':True,'seconds':plan['duration_seconds'],'frames':plan['frame_count'],'bytes':comp.stat().st_size,'output':str(OUT)},ensure_ascii=False),flush=True)
