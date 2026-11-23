"""Create an eight-chapter player and a separate temporary Cloudflare tunnel."""
from pathlib import Path
import json,html,subprocess,sys,socket,re,time,urllib.request,zipfile
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=R/'output/EP001-EP008-v5';S=P/'share';S.mkdir(exist_ok=True)
N='EP001-EP008_sams_apocalypse_v5'

def main():
    chapters=json.loads((O/'chapters.json').read_text())
    buttons=''.join(f'<button data-seek="{c["start_seconds"]}">EP{c["episode"]:03d} · {html.escape(c["title"])}</button>' for c in chapters)
    page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>山姆八集合集 · 真人末日电影风 v5</title><style>body{background:#111923;color:#f2f5f9;font:16px system-ui,"PingFang SC",sans-serif;margin:0}main{max-width:1100px;margin:28px auto;padding:0 18px}h1{font-size:27px}p{line-height:1.8;color:#b6c5d6}video{width:100%;background:black;border-radius:10px}a{color:#9bd7ff}button{background:#23384d;color:white;border:1px solid #4c647c;border-radius:7px;padding:10px 13px;margin:5px 7px 5px 0;cursor:pointer}.links{display:flex;gap:20px;flex-wrap:wrap;margin:24px 0}</style><main><h1>丧尸爆发后，我拥有整个山姆超市</h1><p>八集完整合集 · 4分04.77秒 · 真人末日电影风 v5<br>干燥整洁的灾难初期超市，沿用原配音、BGM和台词；固定镜头，短叠化，无额外等待。</p><video controls playsinline preload="metadata" src="NAME.mp4"></video><p id="status">点击播放</p><div><button id="play">从头播放</button><button id="speed">播放速度 1×</button></div><nav>CHAPTERS</nav><div class="links"><a href="NAME.mp4" download>下载带字幕MP4</a><a href="NAME_clean.mp4" download>下载无字MP4（含原声音）</a><a href="NAME.zh-CN.srt" download>下载SRT</a><a href="NAME.zh-CN.vtt" download>下载VTT</a><a href="EP001-EP008_v5_subtitles.zip" download>下载字幕包</a></div><p>本版画面由新绘电影风格静帧及短叠化组成。Cloudflare为临时分享，需要本机在线。</p></main><script>const v=document.querySelector('video'),s=document.querySelector('#status');document.querySelector('#play').onclick=()=>{v.currentTime=0;v.play().catch(()=>{})};document.querySelector('#speed').onclick=()=>{const r=[1,1.25,1.5,2,4,8];v.playbackRate=r[(r.indexOf(v.playbackRate)+1)%r.length];document.querySelector('#speed').textContent='播放速度 '+v.playbackRate+'×'};document.querySelectorAll('[data-seek]').forEach(b=>b.onclick=()=>{v.currentTime=+b.dataset.seek;v.play().catch(()=>{})});v.ontimeupdate=()=>s.textContent=v.currentTime.toFixed(2)+' / '+v.duration.toFixed(2)+' 秒';v.onended=()=>s.textContent='播放完毕';v.onerror=()=>s.textContent='播放错误：'+v.error?.message;</script></html>'''.replace('NAME',N).replace('CHAPTERS',buttons)
    (O/'index.html').write_text(page)
    with zipfile.ZipFile(O/'EP001-EP008_v5_subtitles.zip','w',zipfile.ZIP_DEFLATED) as z:
        for suffix in ['zh-CN.srt','zh-CN.vtt']:
            f=O/f'{N}.{suffix}';z.write(f,f.name)
        z.write(O/'chapters.json','chapters.json')
    port=5196
    s=socket.socket();available=s.connect_ex(('127.0.0.1',port))!=0;s.close()
    if available:
        with (S/'http.log').open('ab') as log:
            proc=subprocess.Popen([sys.executable,str(R/'production/v2/scripts/share_server.py'),'--directory',str(O.resolve()),'--port',str(port)],stdout=log,stderr=log,start_new_session=True)
        (S/'http.pid').write_text(str(proc.pid))
    tunnel_log=S/'cloudflared.log'
    if not (S/'cloudflared.pid').exists():
        with tunnel_log.open('ab') as log:
            proc=subprocess.Popen(['/opt/homebrew/bin/cloudflared','tunnel','--url',f'http://127.0.0.1:{port}','--no-autoupdate'],stdout=log,stderr=log,start_new_session=True)
        (S/'cloudflared.pid').write_text(str(proc.pid))
    for attempt in range(25):
        urls=re.findall(r'https://[a-z0-9-]+\.trycloudflare\.com',tunnel_log.read_text() if tunnel_log.exists() else '')
        if urls:break
        time.sleep(1)
    assert urls,'Tunnel did not provide a URL'
    url=urls[-1];(S/'url.txt').write_text(url+'\n')
    print(json.dumps({'local':f'http://127.0.0.1:{port}/','cloudflare':url,'mode':'temporary; local machine must remain online'},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
