"""仅共享已验收的成片、封面和字幕，复用既有Cloudflare临时隧道。"""
from pathlib import Path
import subprocess,os,signal,time,json,shutil,sys,urllib.request
P=Path(__file__).resolve().parent
REPO=P.parents[3]
OUT=P.parent.parent/'episodes/EP001_die-pa-le-ma/output'
FILM='die-pa-le-ma_1080x1920_60s.mp4'
PAGE='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>跌怕了吗｜写给投资低谷中的你</title><style>
*{box-sizing:border-box}body{margin:0;background:#111b1c;color:#f2ead9;font-family:system-ui,-apple-system,sans-serif}main{max-width:1160px;margin:auto;padding:30px 28px;display:grid;grid-template-columns:minmax(260px,460px) 1fr;gap:52px;align-items:center;min-height:100vh}video{display:block;width:100%;max-height:90vh;background:#111b1c;border-radius:14px;box-shadow:0 20px 80px #060d0d}h1{font-family:serif;font-size:clamp(44px,7vw,76px);line-height:1.2;margin:18px 0}p{font-size:17px;line-height:1.9;color:#bdc6bd}.tag{font-size:13px;letter-spacing:3px;color:#d8ad70}.quote{font-family:serif;font-size:25px;color:#f2ead9}button,a{display:inline-flex;align-items:center;justify-content:center;padding:12px 20px;border-radius:7px;border:1px solid #66766b;background:transparent;color:#f2ead9;text-decoration:none;font-size:14px;cursor:pointer;margin:0 8px 12px 0}button{background:#d8ad70;color:#142120;border-color:#d8ad70;font-weight:600}.meta{font-size:13px;color:#9cad9f}.links{margin-top:22px}@media(max-width:720px){main{display:flex;flex-direction:column;padding:22px 18px;gap:24px;align-items:stretch}video{max-height:76vh;width:auto;max-width:100%;margin:auto}h1{font-size:48px}section{padding:0 7px 25px}}
</style></head><body><main><video id="film" controls playsinline preload="metadata" poster="cover.jpg" src="die-pa-le-ma_1080x1920_60s.mp4"></video><section><div class="tag">写给投资低谷中的你</div><h1>跌怕了吗</h1><p class="quote">账户的涨跌，定义不了你。</p><p>下坠、重压、认真、呼吸、余地、站稳。<br>愿这六十秒，接住疲惫的你。</p><button id="play" onclick="const v=document.getElementById('film');v.currentTime=0;v.play()">从头播放</button><div class="links"><a href="die-pa-le-ma_1080x1920_60s.mp4" download>下载成片</a><a href="die-pa-le-ma.zh-CN.srt" download>SRT 字幕</a><a href="die-pa-le-ma.zh-CN.vtt" download>VTT 字幕</a></div><p class="meta">60秒 · 1080×1920 · 音乐卡点 · 无新增配音</p></section></main></body></html>'''

def restart(script,info,env=None):
 if info.exists():
  prior=json.loads(info.read_text());pid=prior['pid']
  cmd=subprocess.run(['ps','-p',str(pid),'-o','command='],capture_output=True,text=True).stdout
  if str(script)in cmd:
   os.kill(pid,signal.SIGTERM)
   for _ in range(30):
    if not subprocess.run(['ps','-p',str(pid),'-o','command='],capture_output=True,text=True).stdout:break
    time.sleep(.1)
 with open(script.parent/(script.stem+'.log'),'ab')as log:
  proc=subprocess.Popen(['python3',str(script)],env={**os.environ,**(env or {})},stdout=log,stderr=log,start_new_session=True)
 return proc.pid

if '--prepare-local' in sys.argv:
 assert (OUT/FILM).exists()
 (OUT/'index.html').write_text(PAGE)
 restart(P/'preview_server.py',P/'preview-origin.json')
 print('http://127.0.0.1:5206/index.html')
 sys.exit()

qa=json.loads((OUT/'delivery-qa.json').read_text())
assert qa['status']=='PASS_LOCAL_DELIVERY'
assert qa['browser_playback']['played_from_start_to_end']
old=REPO/'stories/emotion-lines/production'
tunnel=json.loads((old/'cloudflare-tunnel.json').read_text())
public=tunnel['public_url'].rstrip('/')
stage=REPO/'stories/emotion-lines/output/cloudflare-share/drawdown'
stage.mkdir(parents=True,exist_ok=True)
for name in [FILM,'cover.jpg','die-pa-le-ma.zh-CN.srt','die-pa-le-ma.zh-CN.vtt']:
 temp=stage/(name+'.tmp');shutil.copyfile(OUT/name,temp);temp.replace(stage/name)
temp=stage/'index.html.tmp';temp.write_text(PAGE);temp.replace(stage/'index.html')
origin=json.loads((old/'cloudflare-origin.json').read_text())
restart(old/'share_server.py',old/'cloudflare-origin.json',{'SHARE_ORIGIN_PORT':str(origin['port'])})
for _ in range(40):
 try:
  urllib.request.urlopen(f'http://127.0.0.1:{origin["port"]}/drawdown/index.html',timeout=2).read();break
 except Exception:time.sleep(.2)
url=public+'/drawdown/index.html'
page=urllib.request.urlopen(url,timeout=30)
assert page.status==200 and '跌怕了吗' in page.read().decode()
req=urllib.request.Request(public+'/drawdown/'+FILM,headers={'Range':'bytes=0-1023'})
with urllib.request.urlopen(req,timeout=30)as r:
 assert r.status==206 and len(r.read())==1024
 assert r.headers['Content-Range'].startswith('bytes 0-1023/')
with urllib.request.urlopen(public+'/drawdown/die-pa-le-ma.zh-CN.srt',timeout=30)as r:assert r.status==200
qa['boundaries']['cloudflare']={'status':'VERIFIED_HTTP','url':url,'html':200,'video_range':206,'subtitle':200,'note':'临时隧道依赖本机服务，未发布到抖音等平台'}
(OUT/'delivery-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
(P/'cloudflare-share.json').write_text(json.dumps({'url':url,'origin':tunnel['origin'],'stage':str(stage),'verified':True},ensure_ascii=False,indent=2))
print(url)
