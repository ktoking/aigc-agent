from pathlib import Path
import subprocess,json,shutil,hashlib,os,signal,time,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[3];E=P.parent.parent/'episodes/EP002_hold-yourself';O=E/'output';F=O/'hold-yourself_1920x1080_60s.mp4'
def run(a):return subprocess.run(a,check=True,capture_output=True).stdout
def probe(f):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]))
x=probe(F);v=next(s for s in x['streams'] if s['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'60/1');assert abs(float(x['format']['duration'])-60)<.05
run(['ffmpeg','-v','error','-i',str(F),'-f','null','-'])
for i,s in enumerate(sorted(E.glob('segment_*'))):
 out=s/'output/video.mp4';run(['ffmpeg','-v','error','-y','-ss',str(i*15),'-i',str(F),'-t','15','-c:v','libx264','-preset','veryfast','-crf','18','-c:a','aac','-movflags','+faststart',str(out)])
 for t,n in [(0,'first'),(14.9833,'last')]:run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(out),'-frames:v','1',str(s/f'frames/{n}-frame.png')])
run(['ffmpeg','-v','error','-y','-ss','58','-i',str(F),'-frames:v','1',str(O/'cover.jpg')])
run(['ffmpeg','-v','error','-y','-i',str(F),'-vf','fps=1/5,scale=480:270,tile=4x3','-frames:v','1',str(O/'contact-sheet.jpg')])
run(['ffmpeg','-v','error','-y','-i',str(F),'-t','10','-c','copy',str(O/'intro10.mp4')])
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>低谷中，守住自己</title><style>body{margin:0;background:#101b2b;color:#f4eee2;font-family:system-ui}main{max-width:1200px;margin:auto;padding:30px}video{width:100%;display:block;background:#101b2b}h1{font-size:36px;margin-bottom:12px}p{color:#b5c1ce;line-height:1.8}a,button{display:inline-block;color:#e8b96c;background:transparent;border:1px solid #53657b;padding:12px 20px;text-decoration:none;margin:10px 12px 0 0;font-size:16px;cursor:pointer}.small{font-size:13px}</style><main><video id="film" controls playsinline preload="metadata" poster="cover.jpg" src="hold-yourself_1920x1080_60s.mp4"></video><h1>低谷中，守住自己</h1><p>你不必买在最低点，才值得被肯定。<br>如何在投资低谷中坚持自我 · 60秒横屏 · 1080p / 60fps</p><button onclick="const v=document.getElementById('film');v.currentTime=0;v.play()">从头播放</button><a href="hold-yourself_1920x1080_60s.mp4" download>下载成片</a><a href="hold-yourself.zh-CN.srt" download>字幕 SRT</a><p class="small">BGM：we never（若如初见）· 无新增旁白<br>历史指数表现不代表个股或未来保证。临时预览链接依赖本机运行。</p></main></html>'''
(O/'index.html').write_text(page)
qa={'video':{'duration':float(x['format']['duration']),'width':1920,'height':1080,'fps':60,'frames':v.get('nb_frames'),'full_decode':'PASS','sha256':hashlib.sha256(F.read_bytes()).hexdigest()},'audio':{'present':any(s['codec_type']=='audio'for s in x['streams']),'source_range':[0,60],'speed':1},'subtitles':{'count':(O/'hold-yourself.zh-CN.srt').read_text().count(' --> ')},'hyperframes':json.load(open(P/'check.json'))['ok'],'browser_playback':'PENDING','cloudflare':'PENDING'}
(O/'delivery-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
stage=R/'stories/emotion-lines/output/cloudflare-share/conviction';stage.mkdir(parents=True,exist_ok=True)
for f in ['index.html',F.name,'cover.jpg','hold-yourself.zh-CN.srt','hold-yourself.zh-CN.vtt']:shutil.copyfile(O/f,stage/f)
old=R/'stories/emotion-lines/production';info=json.load(open(old/'cloudflare-origin.json'));script=old/'share_server.py';cmd=subprocess.run(['ps','-p',str(info['pid']),'-o','command='],capture_output=True,text=True).stdout
if str(script) in cmd:
 os.kill(info['pid'],signal.SIGTERM);time.sleep(.7)
with open(old/'share_server.log','ab') as log:subprocess.Popen(['python3',str(script)],env={**os.environ,'SHARE_ORIGIN_PORT':str(info['port'])},stdout=log,stderr=log,start_new_session=True)
time.sleep(1)
public=json.load(open(old/'cloudflare-tunnel.json'))['public_url']+'/conviction/'
for url in [public+'index.html',public+'hold-yourself.zh-CN.srt']:
 with urllib.request.urlopen(url,timeout=30)as res:assert res.status==200
with urllib.request.urlopen(urllib.request.Request(public+F.name,headers={'Range':'bytes=0-1023'}),timeout=30)as res:assert res.status==206 and len(res.read())==1024
qa['cloudflare']={'url':public+'index.html','html':200,'video_range':206};(O/'delivery-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));(P/'cloudflare-share.json').write_text(json.dumps(qa['cloudflare'],indent=2));print(public+'index.html')
