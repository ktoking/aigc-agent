"""原创《跌怕了吗》：本地矢量舞台、实测音乐节拍、可寻址的六幕动画。"""
from pathlib import Path
import json, shutil, html

P=Path(__file__).resolve().parent
STORY=P.parent.parent
REPO=STORY.parent.parent
EP=STORY/'episodes/EP001_die-pa-le-ma'
OUT=EP/'output'
for d in [P/'assets',P/'compositions',STORY/'assets',STORY/'docs',OUT]:d.mkdir(parents=True,exist_ok=True)
old=REPO/'stories/emotion-lines/production/inner-noise/assets'
for name in ['gsap.min.js','reference-soundtrack.m4a','songti.ttc']:
    if not (P/'assets'/name).exists():shutil.copy2(old/name,P/'assets'/name)
if not (P/'assets/sans.ttc').exists():shutil.copyfile('/System/Library/Fonts/Hiragino Sans GB.ttc',P/'assets/sans.ttc')

CUES=[
 (0,2.185,'跌怕了吗'),
 (2.185,4.315,'明明已经很小心了，'),
 (4.315,8.535,'账户，还是一片绿。'),
 (8.535,12.785,'最沉的，可能不只是亏损。'),
 (12.785,17.035,'是开始怀疑：'),
 (17.035,19.195,'「是不是我不行？」'),
 (19.195,23.445,'如果你还在一笔笔买入，'),
 (23.445,27.695,'那份认真，我看见了。'),
 (27.695,31.945,'但你不用靠加仓，证明自己没错。'),
 (31.945,36.195,'先把行情放一放。'),
 (36.195,40.445,'允许自己，缓一口气。'),
 (40.445,42.575,'休息，也不算认输。'),
 (42.575,46.825,'再看看：买入的理由还在吗？'),
 (46.825,51.075,'留住生活的钱，给判断留点余地。'),
 (51.075,55.325,'账户的涨跌，定义不了你。'),
 (55.325,60,'愿你慢慢站稳，再决定下一步。')]
SCENES=[
 (0,8.535,'跌怕了吗','下坠的日子','跌落绿柱，微小的人仍在地面上。'),
 (8.535,19.195,'亏损之外','别把一切归咎于自己','自责石块逐拍压近，人物坐下。'),
 (19.195,31.945,'我看见了','认真，也需要被温柔对待','买入纸片入场，停住、转身，成为遮雨的屋檐。'),
 (31.945,42.575,'缓一口气','把目光，暂时还给生活','手机翻面离场，圆形空间逐层打开。'),
 (42.575,51.075,'给自己余地','理由 · 仓位 · 生活','三座基石随拍落稳，人物落脚于稳固平台。'),
 (51.075,60,'先，站稳','再决定下一步','暖色门洞升起，台阶出现，人慢慢向前。')]
BEATS=json.loads((REPO/'stories/emotion-lines/production/fault-tolerance-v2/beats.json').read_text())
# 保留原始检测文件，不把估计BPM当作人工校准结果。
(P/'beats.json').write_text(json.dumps(BEATS,ensure_ascii=False,indent=2))
(P/'beat-map.json').write_text(json.dumps({'bpm_estimate':112.9,'source':'原参考片AAC音轨实测节拍，沿用用户确认的音乐','rate':1,'scenes':[{'start':a,'end':b,'title':c}for a,b,c,_,_ in SCENES],'cues':[{'start':a,'end':b,'text':c}for a,b,c in CUES]},ensure_ascii=False,indent=2))

STYLE='''
@font-face{font-family:LocalSong;src:url(assets/songti.ttc)}
@font-face{font-family:LocalSans;src:url(assets/sans.ttc)}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#111b1c}
#root{position:absolute;inset:0;width:100%;height:100%;color:#f2ead9;font-family:LocalSans,sans-serif}
.clip{position:absolute;inset:0;width:100%;height:100%}
.bg{position:absolute;inset:0;background:#111b1c}
.topline{position:absolute;left:88px;right:88px;top:132px;display:flex;justify-content:space-between;font-size:25px;letter-spacing:4px;color:#bdc6bd}
.footer{position:absolute;left:88px;right:88px;bottom:120px;display:flex;justify-content:space-between;font-size:23px;color:#bdc6bd;letter-spacing:2px}
.captionclip{position:absolute;inset:auto;left:100px;right:100px;top:1460px;height:225px;width:auto}.caption-box{position:absolute;left:100px;right:100px;top:1460px;height:225px;display:flex;align-items:flex-start;justify-content:center}
.caption{position:absolute;inset:0;font-size:51px;line-height:1.65;text-align:center;display:flex;align-items:flex-start;justify-content:center;color:#f2ead9;font-weight:500;letter-spacing:1px}
.caption span{display:block;max-width:860px}
.meter{position:absolute;left:88px;bottom:192px;width:904px;height:3px;background:#334344}
.progress{width:100%;height:100%;background:#d8ad70;transform-origin:left center}
.headline{position:absolute;left:80px;right:80px;top:270px;text-align:center;font-family:LocalSong,serif;font-size:154px;font-weight:700;line-height:1.2;letter-spacing:-4px;margin:0}
.kicker{position:absolute;left:80px;right:80px;top:485px;text-align:center;font-size:28px;letter-spacing:5px;color:#bdc6bd}
.visual{position:absolute;left:0;top:560px;width:1080px;height:860px;overflow:hidden}
.world{transform-origin:540px 1050px}
.svg-label{font-family:LocalSans,sans-serif;font-weight:500;letter-spacing:2px}
'''

def defs(i):
 return f'''<defs>
 <linearGradient id="jade{i}" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#93b5a4"/><stop offset=".55" stop-color="#527d70"/><stop offset="1" stop-color="#254d47"/></linearGradient>
 <linearGradient id="gold{i}" x1="0" y1="0" x2=".7" y2="1"><stop stop-color="#f4dba7"/><stop offset=".55" stop-color="#d8ad70"/><stop offset="1" stop-color="#9c7646"/></linearGradient>
 <linearGradient id="stone{i}" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#83948b"/><stop offset=".55" stop-color="#4b615c"/><stop offset="1" stop-color="#2a3b3a"/></linearGradient>
 <radialGradient id="halo{i}"><stop stop-color="#d8ad70" stop-opacity=".25"/><stop offset="1" stop-color="#d8ad70" stop-opacity="0"/></radialGradient>
 <linearGradient id="portal{i}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ecd39b"/><stop offset="1" stop-color="#b1864c" stop-opacity=".02"/></linearGradient>
 </defs>'''

def person(i,x=540,y=650,scale=1,seated=False):
 # 多层圆润剪影，始终沿用同一个人物。内层局部坐标，外层只负责走位。
 body='<path d="M-27 2Q-10-10 19 2L32 76L-26 78Z" fill="url(#gold%d)"/>'%i
 if seated:body+='<path d="M-18 66L42 86L68 135M12 70L-21 105L-43 134" fill="none" stroke="#c79c64" stroke-width="18" stroke-linecap="round"/>'
 else:body+='<path d="M-15 70L-19 135M14 70L22 135" fill="none" stroke="#c79c64" stroke-width="17" stroke-linecap="round"/>'
 return f'<g id="s{i}-person"><g transform="translate({x} {y})"><g transform="scale({scale})"><ellipse cx="2" cy="142" rx="55" ry="11" fill="#071011" opacity=".7"/><circle cx="0" cy="-29" r="25" fill="#e7c995"/>{body}<path d="M-23 12L-35 62M23 12L38 59" fill="none" stroke="#cfaa76" stroke-width="13" stroke-linecap="round"/></g></g></g>'

def plinth(i,x,y,w,h):
 return f'<g><path d="M{x} {y}l55-36h{w}l-55 36Z" fill="#e4c692"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="url(#gold{i})"/><path d="M{x+w} {y}l55-36v{h}l-55 36Z" fill="#795c3d"/></g>'

def art(i):
 s=defs(i)
 s+=f'<ellipse cx="540" cy="660" rx="520" ry="370" fill="url(#halo{i})" id="s{i}-halo"/>'
 anim=[]
 if i==0:
  # 每个绿柱是物理隐喻，不是市场数据；纵向下坠由节拍逐个触发。
  for j,(x,y,h) in enumerate([(120,200,220),(294,290,275),(468,370,270),(642,450,250),(816,530,210)]):
   s+=f'<g id="s0-candle{j}"><path d="M{x+36} {y-65}v{h+120}" stroke="#74a08b" stroke-width="9"/><path d="M{x} {y}l28-18h85l-28 18Z" fill="#9cbeac"/><rect x="{x}" y="{y}" width="85" height="{h}" rx="5" fill="url(#jade0)"/><path d="M{x+85} {y}l28-18v{h}l-28 18Z" fill="#31564b"/></g>'
   at=[.045,1.115,2.185,3.255,4.315][j]
   anim.append(f'tl.fromTo("#s0-candle{j}",{{y:-700,rotation:-12,opacity:0}},{{y:0,rotation:0,opacity:1,duration:.58,ease:"power3.in"}},{at});')
   anim.append(f'tl.to("#s0-candle{j}",{{y:70,duration:.24,ease:"power2.in"}},6.445);')
  s+='<ellipse cx="540" cy="814" rx="390" ry="26" fill="#071011"/><path d="M90 802Q540 765 990 802" fill="none" stroke="#8b9c8e" stroke-width="2"/>'
  s+=person(i,540,635,.87)
  anim+=['tl.fromTo("#s0-person",{y:20,opacity:0},{y:0,opacity:1,duration:.7,ease:"power2.out"},.045);']
 elif i==1:
  for j,(x,y,r,label) in enumerate([(270,250,-13,'后悔'),(765,270,9,'怀疑'),(520,455,-5,'自责')]):
   s+=f'<g id="s1-rock{j}"><g transform="translate({x} {y})"><g transform="rotate({r})"><path d="M-145-85L-50-137L93-105L162-5L97 105L-68 127L-172 23Z" fill="url(#stone1)"/><path d="M-145-85L-50-137L93-105L-7-52Z" fill="#8a9c90" opacity=".55"/><path d="M-7-52L97 105" fill="none" stroke="#213b36" stroke-width="3"/><text class="svg-label" y="20" font-size="52" text-anchor="middle" fill="#f2ead9">{label}</text></g></g></g>'
   anim.append(f'tl.fromTo("#s1-rock{j}",{{y:-440,rotation:{-18+j*14},opacity:0}},{{y:0,rotation:0,opacity:1,duration:.75,ease:"bounce.out"}},{[.05,2.13,4.25][j]});')
   anim.append(f'tl.to("#s1-rock{j}",{{y:{35+j*10},duration:1.1,ease:"power2.inOut"}},6.38);')
  s+='<ellipse cx="540" cy="806" rx="375" ry="29" fill="#071011"/>'
  s+=person(i,540,640,.9,True)
  s+='<path id="s1-rim" d="M363 742Q540 620 718 742" fill="none" stroke="#d8ad70" stroke-width="3" opacity=".8"/>'
  anim+=['tl.fromTo("#s1-person",{opacity:0},{opacity:1,duration:.6},.05);','tl.fromTo("#s1-rim",{opacity:0},{opacity:.8,duration:1.0},8.5);']
 elif i==2:
  for j,(x,y,r) in enumerate([(250,255,-22),(425,230,-7),(605,245,12),(780,290,24)]):
   s+=f'<g id="s2-ticket{j}"><g transform="translate({x} {y})"><g transform="rotate({r})"><rect x="-115" y="-150" width="230" height="300" rx="16" fill="#e8dcc2"/><path d="M-115 72H115" stroke="#a08b67" stroke-width="2" stroke-dasharray="7 9"/><text id="s2-ticket-label{j}" class="svg-label" y="22" font-size="65" text-anchor="middle" fill="#33594d">买入</text></g></g></g>'
   anim.append(f'tl.fromTo("#s2-ticket{j}",{{y:550,x:{(-1)**j*180},rotation:{-35+j*20},opacity:0}},{{y:0,x:0,rotation:0,opacity:1,duration:.65,ease:"power3.out"}},{[0,1.06,2.12,3.19][j]});')
   anim.append(f'tl.to("#s2-ticket-label{j}",{{opacity:0,duration:.18}},8.28);')
   anim.append(f'tl.to("#s2-ticket{j}",{{x:{(540-x)*.7},y:{420-y},rotation:{[-14,-5,4,14][j]-r},scale:.83,duration:1.25,ease:"power2.inOut"}},8.5);')
  s+=person(i,540,640,.9)
  s+='<g transform="translate(540 515)"><g id="s2-shelter"><path d="M-330 0Q0-222 330 0L295 15Q0-159-295 15Z" fill="url(#gold2)"/></g></g>'
  anim+=['tl.fromTo("#s2-shelter",{scaleX:0,opacity:0},{scaleX:1,opacity:1,duration:.8,ease:"power3.out"},9.55);']
  for j in range(12):
   x=120+j*76
   s+=f'<rect id="s2-rain{j}" x="{x}" y="75" width="3" height="70" rx="2" fill="#71978a" opacity=".5"/>'
   anim.append(f'tl.fromTo("#s2-rain{j}",{{y:-70,opacity:0}},{{y:{240+(j%3)*80},opacity:.55,duration:.7,ease:"none",repeat:2}},{9.55+(j%4)*.13});')
 elif i==3:
  s+='<g id="s3-phone"><g transform="translate(540 410)"><rect x="-166" y="-310" width="332" height="620" rx="49" fill="#080f10" stroke="#677e72" stroke-width="5"/><rect x="-142" y="-270" width="284" height="515" rx="22" fill="#1d3430"/><rect x="-45" y="-292" width="90" height="8" rx="4" fill="#455b51"/>'
  for j,h in enumerate([88,125,112,166,199]):s+=f'<rect x="{-110+j*45}" y="{-180+j*44}" width="24" height="{h}" rx="3" fill="#789e8d"/>'
  s+='</g></g><g transform="translate(540 415)"><g id="s3-breath">'
  for j in range(5):s+=f'<circle id="s3-ring{j}" cx="0" cy="0" r="{115+j*57}" fill="none" stroke="#d8ad70" stroke-width="{3 if j==0 else 1.5}" opacity="{.9-j*.14}"/>'
  s+='<circle cx="0" cy="0" r="111" fill="url(#gold3)"/><text class="svg-label" x="0" y="15" text-anchor="middle" font-size="45" fill="#172322">呼吸</text></g></g>'
  s+=person(i,540,655,.9)
  anim+=['tl.fromTo("#s3-phone",{scale:.9,rotation:-8,opacity:0},{scale:1,rotation:0,opacity:1,duration:.6,ease:"power2.out"},0);','tl.to("#s3-phone",{x:650,y:-240,rotation:42,opacity:0,duration:1.1,ease:"power3.inOut"},2.12);','tl.fromTo("#s3-breath",{scale:.15,opacity:0},{scale:1,opacity:1,duration:1.15,ease:"power3.out"},3.18);']
  for j in range(5):anim.append(f'tl.to("#s3-ring{j}",{{scale:{1.09+j*.022},duration:2.125,yoyo:true,repeat:1,ease:"sine.inOut"}},4.25);')
 elif i==4:
  for j,(x,y,w,h,label) in enumerate([(145,585,220,160,'理由'),(405,510,220,235,'仓位'),(665,435,220,310,'生活')]):
   s+=f'<g id="s4-block{j}">{plinth(i,x,y,w,h)}<text class="svg-label" x="{x+w/2}" y="{y+94}" font-size="49" text-anchor="middle" fill="#172322">{label}</text></g>'
   anim.append(f'tl.fromTo("#s4-block{j}",{{y:350,opacity:0}},{{y:0,opacity:1,duration:.7,ease:"power3.out"}},{[0,1.06,2.12][j]});')
  s+=person(i,540,402,.8)
  anim+=['tl.fromTo("#s4-person",{y:-160,opacity:0},{y:0,opacity:1,duration:.7,ease:"power2.out"},3.19);']
  s+='<g id="s4-frame"><path d="M120 780V205Q120 145 180 145H900Q960 145 960 205V780" stroke="#8caf9a" stroke-width="3" fill="none"/><circle cx="540" cy="145" r="8" fill="#d8ad70"/></g>'
  anim+=['tl.fromTo("#s4-frame",{opacity:0},{opacity:.75,duration:1.0,ease:"power2.out"},4.25);']
 elif i==5:
  s+='<g transform="translate(545 585)"><g id="s5-door"><path d="M-210 0V-335Q-210-545 0-545T210-335V0Z" fill="url(#portal5)"/><path d="M-210 0V-335Q-210-545 0-545T210-335V0" fill="none" stroke="#d8ad70" stroke-width="4"/></g></g>'
  for j in range(5):
   x=155+j*120;y=730-j*58
   s+=f'<g id="s5-step{j}">{plinth(i,x,y,120,65+j*58)}</g>'
   anim.append(f'tl.fromTo("#s5-step{j}",{{y:250,opacity:0}},{{y:0,opacity:1,duration:.65,ease:"power3.out"}},{j*.53});')
  s+=person(i,215,620,.83)
  for j in range(4):anim.append(f'tl.to("#s5-person",{{x:{(j+1)*120},y:{-(j+1)*58},duration:.7,ease:"power2.inOut"}},{2.12+j*1.06});')
  anim+=['tl.fromTo("#s5-door",{scaleY:.65,opacity:0},{scaleY:1,opacity:1,duration:2.1,ease:"power2.out"},0);','tl.to("#s5-halo",{opacity:1,duration:3.0,ease:"power2.out"},4.25);']
 return s,anim

for i,(a,b,title,kicker,desc) in enumerate(SCENES):
 ident=f'scene-{i+1}'
 svg,animations=art(i)
 local_css=STYLE.replace('url(assets/','url(../assets/')
 # 声明面内独立且完整的样式和脚本，组合加载时不会掉head。
 script=f'''document.fonts.ready.then(()=>{{
 const tl=gsap.timeline({{paused:true}});
 tl.fromTo("#s{i}-title",{{y:65,opacity:0,rotation:{-2 if i%2 else 2}}},{{y:0,opacity:1,rotation:0,duration:.55,ease:"power3.out"}},0);
 tl.fromTo("#s{i}-kicker",{{y:20,opacity:0}},{{y:0,opacity:1,duration:.5}},.25);
 {''.join(animations)}
 tl.fromTo("#s{i}-world",{{scale:1.035}},{{scale:1,y:-5,duration:{b-a},ease:"none"}},0);
 window.__timelines["{ident}"]=tl;
 }});'''
 doc=f'''<!DOCTYPE html><html><head></head><body><template>
 <style>{local_css}</style>
 <div id="root" data-composition-id="{ident}" data-width="1080" data-height="1920" data-duration="{b-a}">
 <div class="bg"></div>
 <h1 class="headline" id="s{i}-title">{title}</h1><div class="kicker" id="s{i}-kicker">{kicker}</div>
 <svg class="visual" viewBox="0 0 1080 860" xmlns="http://www.w3.org/2000/svg"><g id="s{i}-world" class="world">{svg}</g></svg>
 </div><script>{script}</script></template></body></html>'''
 (P/f'compositions/{ident}.html').write_text(doc)
 (P/f'compositions/{ident}.motion.json').write_text(json.dumps({'scene_id':ident,'duration':b-a,'rules':['kinetic-beat-slam','depth-scatter-assemble','multi-phase-camera'],'objects':desc,'entry':'实测节拍上的transform入场','exit':'节拍硬切','deterministic':True},ensure_ascii=False,indent=2))

def host(duration=60):
 clips=''.join(f'<div id="mount-scene-{i+1}" class="clip" data-composition-id="scene-{i+1}" data-composition-src="compositions/scene-{i+1}.html" data-start="{a}" data-duration="{min(b,duration)-a}" data-track-index="{i+1}"></div>'for i,(a,b,*_) in enumerate(SCENES)if a<duration)
 captions=''.join(f'<div id="caption-clip-{j}" class="clip captionclip" data-start="{a}" data-duration="{min(b,duration)-a}" data-track-index="{8+j//3}"><span class="caption" id="cue{j}"><span>{html.escape(c)}</span></span></div>'for j,(a,b,c)in enumerate(CUES)if a<duration)
 script='const tl=gsap.timeline({paused:true});'
 for j,(a,b,c)in enumerate(CUES):
  if a>=duration:continue
  axis=['scale:1.06','x:-30','y:24'][j%3]
  script+=f'tl.fromTo("#cue{j}",{{{axis},opacity:0}},{{scale:1,x:0,y:0,opacity:1,duration:.28,ease:"power3.out"}},{a});'
 script+=f'tl.fromTo("#progress",{{scaleX:0}},{{scaleX:1,duration:{duration},ease:"none"}},0);window.__timelines["drawdown"]=tl;'
 return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>跌怕了吗｜炒股低谷期</title><script src="assets/gsap.min.js"></script><style>{STYLE}</style></head><body>
 <div id="root" data-composition-id="drawdown" data-width="1080" data-height="1920" data-duration="{duration}" data-fps="30"><div class="bg"></div><div id="theater" style="position:absolute;inset:0">{clips}</div>{captions}
 <div class="topline"><span>写给投资低谷中的你</span><span>慢 慢 站 稳</span></div>
 <div class="meter"><div class="progress" id="progress"></div></div>
 <div class="footer"><span>跌怕了吗</span><span>让生活，先回到自己手里</span></div>
 <audio id="original-music" src="assets/reference-soundtrack.m4a" data-start="0" data-duration="{duration}" data-media-start="0" data-track-index="20" data-volume="1"></audio>
 </div><script>document.fonts.ready.then(()=>{{{script}}});</script></body></html>'''
(P/'index.html').write_text(host())
INTRO=P.parent/'die-pa-le-ma-intro10'
INTRO.mkdir(exist_ok=True)
for sub in ['assets','compositions']:
    shutil.copytree(P/sub,INTRO/sub,dirs_exist_ok=True,copy_function=shutil.copyfile)
shutil.copyfile(P/'hyperframes.json',INTRO/'hyperframes.json')
(INTRO/'index.html').write_text(host(10))
(P/'index.motion.json').write_text(json.dumps({'duration':60,'assertions':[{'kind':'appearsBy','selector':'#cue0','bySec':0.8},{'kind':'staysInFrame','selector':'#cue0'},{'kind':'staysInFrame','selector':'#cue15'},{'kind':'keepsMoving','withinSelector':'#theater','maxStaticSec':3.0}]},ensure_ascii=False,indent=2))

def stamp(t,sep=','):
 ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}{sep}{ms%1000:03d}'
(OUT/'die-pa-le-ma.zh-CN.srt').write_text('\n\n'.join(f'{j+1}\n{stamp(a)} --> {stamp(b)}\n{c}'for j,(a,b,c)in enumerate(CUES))+'\n')
(OUT/'die-pa-le-ma.zh-CN.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(a,".")} --> {stamp(b,".")}\n{c}'for a,b,c in CUES)+'\n')

(STORY/'AGENTS.md').write_text('''# 《跌怕了吗》原创故事包

本包是炒股低谷期的情绪鼓励短片，遵循仓库60秒、4段规范。主视觉是深青背景、玉绿下坠物、暖金人物的矢量立体剧场。人物为原创抽象剪影，不锁真人脸。

不使用分支连线，不复制Nico构图；不换成容错率主题。音乐沿用用户确认的《we never（若如初见）》参考音轨，原速；无新增旁白。屏幕文案和独立SRT/VTT同时交付。

不捏造行情/账户数据，不把台阶上升解释为股价必然回升，不鼓励无限补仓。安慰人的情绪，允许休息和调整。

素材和输出仅在本故事包内。保持可寻址动画和本地资源，不使用Skynet、Git hooks或上传凭证。
''')
docs={
'story-memory.md':'# 内容锁定\n\n标题《跌怕了吗》，写给炒股低谷期的人。用户请求原创、卡点音乐和变化丰富的新风格。沿用既有音乐偏好；不沿用旧片分支连线。\n',
'production-rules.md':'# 生产约束\n\n60秒1080×1920、30fps、四段15秒。六个节拍场景，16条文案。所有画面为原创SVG物体隐喻，无真实行情。原音轨0—60秒、无变速、无新增配音。\n',
'workflow.md':'# 本次流程\n\n按Winhao学AI教程：查来源 → 分幕文案 → 准备素材并记来源 → 三案比选与avoid → 分镜审查 → 10秒试片 → 全片导出和真实媒体检查。源文件在production/die-pa-le-ma，主片和字幕在episodes/EP001_die-pa-le-ma/output。\n',
'season-arc.md':'# 单集情绪弧\n\n看见下跌恐惧 → 放下自我否定 → 接住认真 → 允许暂停 → 回到判断与生活 → 站稳再决定。\n',
'audience-strategy.md':'# 受众\n\n经历投资回撤、仍在按自己的计划投入而感到孤独的人。前2秒提问，3—5秒一次物体/文字变化。不用收益承诺或羞辱卖出者制造共鸣。\n'}
for k,v in docs.items():(STORY/'docs'/k).write_text(v)
(P/'BRIEF.md').write_text('''---
workflow: general-video
flow: automation
storyboard: no
---
# 跌怕了吗

用户已授权制作完整原创视频。60秒竖屏，音乐卡点，无新增旁白；复用已确认的we never参考音轨。主题为炒股低谷期的情绪安慰。

## 参考与方法
Winhao学AI：Vibe知识大赏｜6步做出爆火的知识科普视频。已在抖音页面核对六步及03:03明确提到的Hyperframes；这不是另一个待安装的vibe技能。

## 创作角度
让下坠、重压、纸片、呼吸和台阶替观众说出心情；结尾站稳的人，代表找回判断力。

## Assets
原创SVG舞台；复用本地GSAP、Songti与Hiragino字体、用户确认音轨。详细见sources.md。
''')
(P/'frame.md').write_text('''# 画风设计与三案比选

1. **立体情绪剧场（采用）**：深青空间、玉绿物体、暖金人物。绿柱下坠、石块压近、纸片变屋檐、手机离场、基石落稳、台阶前进。视觉变化由物体动作推动。
2. 黑白粗笔纸漫画：易读，但线描与先前图解过于接近。
3. 实拍夜行与城市窗灯：有温度，但与抽象投资情绪的动作对应较弱，需要更多合适的实拍资产。

## 设计系统
背景#111b1c，前景#f2ead9，主强调暖金#d8ad70；玉绿只服务下跌/重压语义。标题LocalSong，正文LocalSans，均打包本地字体。标题154px，正文51px。主焦点是560—1420px区域中的立体物体。顶部标题，底部独立文案区，边角仅放轻量锚点。

## avoid
禁止分支连线、树状图、股票收益截图、虚构涨跌数字、满屏金融终端UI、霓虹紫蓝、静态照片反复缩放、廉价震屏、闪白、过锐细纹理、许诺回本、把加仓塑造成勇敢的唯一证明。

## 动效依据
kinetic-beat-slam、depth-scatter-assemble、multi-phase-camera；仅呼吸一幕使用sine-wave-loop，内容上就是允许呼吸。原创物体采用SVG二维投影的立体明暗，不宣称物理3D渲染。
''')
sb='# 分镜与检查\n\nmusic: 用户确认的we never（若如初见）原参考AAC，0—60秒、原速。\n\n'
for i,(a,b,t,k,d)in enumerate(SCENES):
 sb+=f'## Frame {i+1}\n\nstatus: animated\nsrc: compositions/scene-{i+1}.html\n时间：{a}—{b}秒\n标题：{t}\n视觉：{d}\n规则：kinetic-beat-slam + depth-scatter-assemble + multi-phase-camera'+(' + sine-wave-loop'if i==3 else '')+'\n节拍：场景起点、文案起点和物体主要落点均使用同一实测节拍表。\n\n'
sb+='## 文案时序\n\n'+'\n'.join(f'- {a:.3f}—{b:.3f}：{c}'for a,b,c in CUES)+'\n\n## 分镜审查\n\n文案均为原创情绪表达；无年份、业绩数字或历史收益论断。最长文案15字，展示4.25秒，约4字/秒。画面是隐喻，无真实行情。无来源的必然回升/坚持就能赢等句子未使用。先导出10秒并检查，再全片渲染。\n'
(P/'STORYBOARD.md').write_text(sb)
(P/'sources.md').write_text('''# 来源与素材台账

## 方法来源（本次浏览核对）
- 用户分享：https://v.douyin.com/zULJ4A2K-tg/
- 解析页：https://www.douyin.com/video/7692352215482240296
- Winhao学AI，时长05:50，标题Vibe知识大赏｜6步做出爆火的知识科普视频。
- 页面完整描述与章节核对：搜集、编排、找图、定样式写分镜、检查分镜、直出；03:03章节明确Hyperframes；04:25先做开头10秒。

## 内容依据
- FINRA Understanding Risk：https://www.finra.org/investors/investing/investing-basics/risk ，2026-10-18抓取正文成功。核对：投资有亏损风险；风险承受能力包括愿意和能够承受的程度；长期持有不消除风险；生活支出会影响承受长期波动的能力。仅据此约束文案，不照搬文章、历史收益或数字。
- Investor.gov股票页本次访问被拒，未作为已核验引用。
- 片中所有安慰语为原创文案，不伪装成名人语录或心理学实验结论。

## 视觉素材
- 六幕所有物体、人物和SVG路径：本项目原创代码绘制，来源build.py；没有借用教程/参考作者画面，没有外部图片可截图的环节。找图步骤因此转为原创资产清单。
- 绿柱仅表示下跌感受；石头表示自责；纸片表示认真；台阶表示恢复自主判断。均不是真实账户、真实股价或预测。
- 字体：本机Songti、Hiragino Sans GB，仅随本地可编辑项目使用；公开分享仅包含已栅格化视频，不分发字体文件。
- GSAP：复用本地3.14.2脚本。

## 音乐
用户先前确认《we never（若如初见）》；复用原参考片下载的AAC音轨assets/reference-soundtrack.m4a。曲名来自用户确认，未做全曲版权/指纹鉴定。原速、0—60秒。技术波形比对单独记录在交付QA，不将其当成授权鉴定。

## 工具
使用已安装HyperFrames技能及0.8.171 CLI。catalog查询falling blocks kinetic typography paper theater，words tier。候选falling-lines是WebGPU背景、caption-kinetic-slam是单词全屏字幕，均不足以承载六幕语义物体；按已读规则原创绘制物体，未引入额外生成API。
''')

for j in range(4):
 seg=EP/f'segment_{j+1:02d}_{j*15:02d}-{(j+1)*15:02d}s'
 for d in ['frames','output']:(seg/d).mkdir(parents=True,exist_ok=True)
 selected=[(a,b,c)for a,b,c in CUES if a<(j+1)*15 and b>j*15]
 text='\n'.join(f'- {max(a,j*15)-j*15:.3f}—{min(b,(j+1)*15)-j*15:.3f}秒：{c}'for a,b,c in selected)
 storyboard=f'# 第{j+1}段分镜\n\n全片{j*15}—{(j+1)*15}秒。\n\n{text}\n\n镜头/对象以production/die-pa-le-ma/STORYBOARD.md中重叠场景为准，固定版心内物体运动，节拍硬切。\n'
 (seg/'storyboard.md').write_text(storyboard)
 for which,tt in [('first',j*15),('last',(j+1)*15-1/30)]:
  scene=next(s for s in SCENES if s[0]<=tt<s[1])
  (seg/f'{which}-frame.md').write_text(f'# {"首"if which=="first"else"尾"}帧\n\n取主片{tt:.6f}秒的实际渲染帧，存frames/{which}-frame.png。场景：{scene[2]}。{scene[4]} 深青背景、暖金人物、玉绿物体；人物和首尾帧由同一确定性时间线继承。\n')
 prompt=f'9:16、15秒、1080×1920，明显非真人的原创矢量立体剧场。角色固定为圆头暖金剪影。首帧frames/first-frame.png锁定本段起点，尾帧frames/last-frame.png锁定本段终点，与相邻段连续。场景为深青抽象空间，灯光左上暖金。\n\n动作链：\n{text}\n\n运镜：围绕主体轻微拉近/拉远，物体逐拍落下、拼合、打开或走位；具体动作来自对应场景代码，不用静态图片代替动画。声音为用户确认we never原速卡点，无新增配音。台词为屏幕文案，不做口型。禁止分支连线、收益承诺、真行情数字、抖动闪白。\n'
 (seg/'prompt.md').write_text('# 视频导演提示词\n\n'+prompt)
 (seg/'director-promt.txt').write_text(prompt)
 (seg/'api-request.md').write_text(f'# 第{j+1}段生成记录\n\n平台：本地HyperFrames0.8.171；外部视频API：NOT_RUN。\n\n参数：1080×1920、30fps、15秒、原音轨对应{j*15}—{(j+1)*15}秒；确定性SVG/GSAP。首尾帧为实际成片抽帧。状态：等待主片渲染后抽段验证。\n\n不需要视频生成API；若重试，仅修改本段重叠场景并重新渲染。\n')
(EP/'publish-package.md').write_text('# 发布文案候选\n\n- 跌怕了吗？写给还在低谷里认真生活的你\n- 账户在下跌，也别把自己判成失败者\n- 炒股最难熬的时候，先接住自己\n\n封面大字：跌怕了吗\n\n评论引导：低谷时，什么能让你重新站稳？\n\n标签：#投资心态 #低谷期 #情绪自救\n\n视频是情绪支持；没有个股建议或收益承诺。未向社交平台发布。\n')
print(json.dumps({'project':str(P),'episode':str(EP),'scenes':len(SCENES),'cues':len(CUES)},ensure_ascii=False))
