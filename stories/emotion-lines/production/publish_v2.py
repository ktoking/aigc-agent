"""更新现有 Cloudflare 分享页，仅复制本轮公开的媒体与播放器。"""
from pathlib import Path
import json, os, re, shutil, signal, subprocess, time, urllib.request

BASE=Path(__file__).resolve().parent
STORY=BASE.parent
SITE=STORY/'output/cloudflare-share'
EP='episodes/EP002_fault-tolerance-v2/output'
qa=json.loads((STORY/EP/'delivery-qa.json').read_text())
assert qa['status']=='PASS_LOCAL_DELIVERY'
assert qa.get('browser_playback',{}).get('played_from_start_to_end') is True

page=(STORY/'player-v2.html').read_text()
public=re.sub(r'<a[^>]*id="edit-link"[^>]*>.*?</a>','',page)
for name in ['fault-tolerance-v2_1080x1920_60s.mp4','fault-tolerance-v2.zh-CN.srt','fault-tolerance-v2.zh-CN.vtt','cover.jpg']:
    dest=SITE/EP/name;dest.parent.mkdir(parents=True,exist_ok=True)
    temp=dest.with_name(dest.name+'.next');shutil.copy2(STORY/EP/name,temp);temp.replace(dest)
for name in ['index.html','player.html']:
    p=SITE/name;tmp=p.with_suffix('.next');tmp.write_text(public);tmp.replace(p)
if not (STORY/'player-v1.html').exists():shutil.copy2(STORY/'player.html',STORY/'player-v1.html')
(STORY/'player.html').write_text(page)

# 原服务对文件做白名单快照；保持原端口重启，以沿用已有公开域名。
info=json.loads((BASE/'cloudflare-origin.json').read_text())
cmd=subprocess.run(['ps','-p',str(info['pid']),'-o','command='],capture_output=True,text=True).stdout
assert 'share_server.py' in cmd, 'Origin pid ownership could not be confirmed'
os.kill(info['pid'],signal.SIGTERM)
time.sleep(.25)
env=os.environ.copy();env['SHARE_ORIGIN_PORT']=str(info['port'])
log=open(BASE/'cloudflare-origin.log','ab')
p=subprocess.Popen(['python3',str(BASE/'share_server.py')],env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
for _ in range(50):
    try:
        current=json.loads((BASE/'cloudflare-origin.json').read_text())
        if current['pid']==p.pid:break
    except (ValueError,FileNotFoundError):pass
    time.sleep(.1)
else:raise RuntimeError('Origin restart did not complete')

tunnel=json.loads((BASE/'cloudflare-tunnel.json').read_text());url=tunnel['public_url']
results=[]
for rel,rg in [('/',None),('/'+EP+'/fault-tolerance-v2_1080x1920_60s.mp4','bytes=0-4095'),('/'+EP+'/fault-tolerance-v2.zh-CN.vtt',None)]:
    req=urllib.request.Request(url+rel,headers={'Range':rg} if rg else {})
    with urllib.request.urlopen(req,timeout=30) as response:
        data=response.read(6000);results.append({'path':rel,'status':response.status,'content_range':response.headers.get('Content-Range')})
        if rel=='/':assert '人生容错率' in data.decode()
        if rg:assert response.status==206 and len(data)==4096
report={'url':url+'/?v=2','version':'fault-tolerance-v2','verified':True,'checks':results}
(BASE/'cloudflare-v2-release.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
