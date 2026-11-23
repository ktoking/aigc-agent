from pathlib import Path
import json,html
P=Path(__file__).resolve().parent
E=P.parent.parent/'episodes/EP002_hold-yourself';O=E/'output';O.mkdir(parents=True,exist_ok=True)
bm=json.loads((P/'beat-map.json').read_text()); cues=bm['cues']
def text(t,x,y,size=100,color='#f4eee2',id='',extra=''):
 return f'<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;font-size:{size}px;color:{color};{extra}">{t}</div>'
def scene(name,dur,body,js,bg='#101b2b'):
 (P/f'compositions/frames/{name}.html').write_text(f'''<template><div data-composition-id="{name}" data-width="1920" data-height="1080" data-duration="{dur}" style="position:absolute;inset:0;overflow:hidden;background:{bg}"><style>#{name}-world{{position:absolute;inset:0;perspective:1800px;font-family:LocalSans}} .paper{{position:absolute;background:#f4eee2;color:#101b2b;border:1px solid #93a5ba;}} </style><div id="{name}-world">{body}</div><script>{{const tl=gsap.timeline({{paused:true}});{js}window.__timelines['{name}']=tl;tl.seek(0);}}</script></div></template>''')
# pressure: phone, falling candle field, compressed future, release
body='<div id="p-phone" style="position:absolute;left:1120px;top:80px;width:600px;height:760px;border:3px solid #93a5ba;border-radius:50px;background:#18273b;padding:55px">'+text('持有的，是对未来的期待',25,60,30,'#93a5ba')+text('又跌了',55,150,100,'#d88089')
for i in range(12):
 body+=f'<div id="c{i}" style="position:absolute;left:{65+i*37}px;top:{330+i*14}px;width:22px;height:{75+(i*29)%100}px;background:#d88089"><div style="position:absolute;left:10px;top:-25px;width:2px;height:220px;background:#d88089"></div></div>'
body+='</div>'+text('跌怕了',120,170,178,id='p-h1',extra='font-family:LocalSong;')+text('吗？',120,380,178,'#e8b96c','p-h2', 'font-family:LocalSong;')+text('示意画面 · 非真实账户',1230,800,26,'#93a5ba','p-note')
body+='<div id="p-question" style="position:absolute;inset:0;background:#101b2b">'+text('我是不是',180,190,146,id='p-q1')+text('做错了？',650,410,210,'#d88089','p-q2')+'</div>'
body+='<div id="p-future" style="position:absolute;inset:0;background:#101b2b">'
for i,w in enumerate(['计划','家人','明天','生活']):body+=f'<div id="panel{i}" style="position:absolute;left:{110+i*430}px;top:170px;width:400px;height:600px;background:{["#1b2b40","#20334b","#263b51","#30475c"][i]};border-top:3px solid #e8b96c">'+text(w,80,200,100)+'</div>'
body+='</div><div id="p-free" style="position:absolute;inset:0;background:#101b2b">'+text('亏损',220,280,180,id='p-loss')+text('≠',840,275,190,'#e8b96c','p-eq')+text('你',1270,280,180,id='p-you')+text('一次结果，装不下完整的你。',520,600,48,'#93a5ba','p-sub')+'</div>'
js="tl.set(['#p-question','#p-future','#p-free'],{autoAlpha:0},0);tl.fromTo('#p-phone',{rotationY:-24,rotationZ:8,y:100},{rotationY:-10,rotationZ:3,y:0,duration:1.649,ease:'power3.out'},0);tl.fromTo('#p-h1',{y:90,opacity:0},{y:0,opacity:1,duration:.6},0);tl.fromTo('#p-h2',{x:-100,opacity:0},{x:0,opacity:1,duration:.6},1.649);"
for i in range(12):js+=f"tl.fromTo('#c{i}',{{y:-370,opacity:0}},{{y:0,opacity:1,duration:.38,ease:'power3.in'}},{.15+i*.31});"
js+="tl.to('#p-phone',{scale:1.23,x:-120,rotationY:0,duration:1.2},3.808);tl.set('#p-question',{autoAlpha:1},5.921);tl.fromTo('#p-q1',{x:-180,opacity:0},{x:0,opacity:1,duration:.45},5.921);tl.fromTo('#p-q2',{scale:1.3,opacity:0},{scale:1,opacity:1,duration:.4},6.455);tl.set('#p-future',{autoAlpha:1},8.057);"
for i in range(4):js+=f"tl.fromTo('#panel{i}',{{rotationY:80,x:{(-1 if i<2 else 1)*500}}},{{rotationY:0,x:0,duration:.8}},{8.057+i*.14});tl.to('#panel{i}',{{x:{(1.5-i)*50},scaleY:1.08,duration:2}},10.194);"
js+="tl.set('#p-free',{autoAlpha:1},12.307);tl.fromTo('#p-loss',{x:200,opacity:0},{x:0,opacity:1,duration:.6},12.307);tl.fromTo('#p-you',{x:-200,opacity:0},{x:0,opacity:1,duration:.6},12.307);tl.fromTo('#p-eq',{scale:0},{scale:1,duration:.5,ease:'back.out(1.4)'},12.7);tl.fromTo('#p-sub',{y:30,opacity:0},{y:0,opacity:1,duration:.7},14.443);"
scene('01-pressure',16.533,body,js)
# history
body='<div id="h-pages" style="position:absolute;inset:0">'
for i,(year,num,sub) in enumerate([('2008–2009','−57%','2007–2009熊市'),('2020','−34%','疫情冲击')]):
 body+=f'<div class="paper" id="h-page{i}" style="left:{100+i*875}px;top:115px;width:845px;height:685px;padding:48px;transform-origin:left center">'+text(year,48,25,100,'#101b2b')+text(num,48,185,180,'#101b2b')+text(sub,48,430,40,'#101b2b')+text('标普500峰谷跌幅 · 约数',48,505,30,'#101b2b')+'</div>'
body+=text('来源：Charles Schwab · Bull vs. Bear（2024）',120,820,26,'#101b2b')+'</div>'
body+='<div id="h-later" style="position:absolute;inset:0;background:#e8b96c">'+text('后 来',150,150,110,'#101b2b')+text('新的起点',400,360,210,'#101b2b','h-start', 'font-family:LocalSong;')+'</div>'
body+='<div id="h-then" style="position:absolute;inset:0;background:#101b2b">'+text('可站在当时',140,170,90,'#93a5ba')+text('谁也不知道',330,320,140,id='h-unknown')+text('底在哪里',750,500,140,'#e8b96c','h-bottom')+text('历史指数表现，不代表个股或未来保证。',450,800,30,'#93a5ba')+'</div>'
body+='<div id="h-worth" style="position:absolute;inset:0;background:#f4eee2">'+text('不必完美',150,180,180,'#101b2b','h-perfect')+text('也值得被肯定',420,440,148,'#101b2b','h-worthline')+'</div>'
body+='<div id="h-thanks" style="position:absolute;inset:0;background:#101b2b">'+text('认真生活的人',180,220,100,'#93a5ba')+text('辛苦了',720,380,220,'#e8b96c','h-thankstitle','font-family:LocalSong;')+'</div>'
js="tl.set(['#h-later','#h-then','#h-worth','#h-thanks'],{autoAlpha:0},0);tl.fromTo('#h-page0',{rotationY:-75,x:-150},{rotationY:0,x:0,duration:.85},0);tl.fromTo('#h-page1',{rotationY:-90,opacity:0},{rotationY:0,opacity:1,duration:.9},2.159);tl.set('#h-later',{autoAlpha:1},4.295);tl.fromTo('#h-later',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.65},4.295);tl.fromTo('#h-start',{y:180,opacity:0},{y:0,opacity:1,duration:.65},6.408);tl.set('#h-then',{autoAlpha:1},8.545);tl.fromTo('#h-then',{clipPath:'inset(0 0 100% 0)'},{clipPath:'inset(0 0 0% 0)',duration:.55},8.545);tl.fromTo('#h-bottom',{x:180,opacity:0},{x:0,opacity:1,duration:.75},10.658);tl.set('#h-worth',{autoAlpha:1},12.794);tl.fromTo('#h-perfect',{x:-150,opacity:0},{x:0,opacity:1,duration:.7},12.794);tl.fromTo('#h-worthline',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.8},14.907);tl.set('#h-thanks',{autoAlpha:1},17.043);tl.fromTo('#h-thankstitle',{scale:.85,opacity:0},{scale:1,opacity:1,duration:.7},17.043);"
scene('02-perspective',19.156,body,js,'#f4eee2')
# agency and morning
body=text('有依据的坚持',120,105,83,'#f4eee2','a-title')
for i,(w,q) in enumerate([('理由','还成立吗？'),('时间','这笔钱能等吗？'),('风险','扛得住吗？')]):
 body+=f'<div id="a-panel{i}" style="position:absolute;left:{120+i*570}px;top:290px;width:540px;height:510px;border:1px solid #93a5ba;background:#1b2b40;transform-origin:left center">'+text('0'+str(i+1),40,30,34,'#93a5ba')+text(w,50,120,115,'#e8b96c')+text(q,50,340,40)+'</div>'
body+='<div id="a-adjust" style="position:absolute;inset:0;background:#101b2b">'+text('调整',120,150,185,'#e8b96c','a-adjustword')+text('也是一种坚持',460,415,155,id='a-stay')+text('给判断，也给生活留余地',600,700,44,'#93a5ba')+'</div>'
body+='<div id="a-life" style="position:absolute;inset:0;overflow:hidden"><img id="a-morning" src="assets/morning.png" style="width:100%;height:100%;object-fit:cover"/><div id="a-living">'+text('账户之外',112,220,105)+text('还有生活',112,380,130,'#e8b96c')+'</div><div id="a-final">'+text('你的人生',112,220,110)+text('还很长',112,390,156,'#e8b96c',extra='font-family:LocalSong;')+'</div></div>'
js="tl.set(['#a-adjust','#a-life','#a-final'],{autoAlpha:0},0);tl.fromTo('#a-title',{y:50,opacity:0},{y:0,opacity:1,duration:.7},0);"
for i,t in enumerate([2.136,4.249,6.386]):js+=f"tl.fromTo('#a-panel{i}',{{rotationY:85,opacity:.08}},{{rotationY:0,opacity:1,duration:.8,ease:'power3.out'}},{t});"
js+="tl.to('#a-panel2',{backgroundColor:'#30475c',duration:.4},8.499);tl.set('#a-adjust',{autoAlpha:1},10.635);tl.fromTo('#a-adjustword',{x:-180,opacity:0},{x:0,opacity:1,duration:.6},10.635);tl.fromTo('#a-stay',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.8},12.771);tl.to('#a-adjust',{scale:1.04,duration:1.6},14.884);tl.set('#a-life',{autoAlpha:1},16.486);tl.fromTo('#a-life',{clipPath:'inset(0 0 0 100%)'},{clipPath:'inset(0 0 0 0%)',duration:.9,ease:'power3.inOut'},16.486);tl.fromTo('#a-morning',{scale:1.055},{scale:1,duration:7.825,ease:'none'},16.486);tl.set('#a-living',{autoAlpha:0},19.11);tl.set('#a-final',{autoAlpha:1},19.11);tl.fromTo('#a-final',{y:35,opacity:0},{y:0,opacity:1,duration:.9},19.11);"
scene('03-life',24.311,body,js)
# Root
hosts=''.join(f'<div class="clip" data-composition-id="{f["id"]}" data-composition-src="compositions/frames/{f["id"]}.html" data-start="{f["start"]}" data-duration="{f["end"]-f["start"]}" data-track-index="{i+1}"></div>' for i,f in enumerate(bm['frames']))
cap='';js=''
for i,c in enumerate(cues):
 cap+=f'<div class="clip captionclip" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-track-index="5"><span style="display:block" class="caption" id="cue{i}">{c["text"]}</span></div>'
 js+=f"tl.fromTo('#cue{i}',{{y:18,opacity:0}},{{y:0,opacity:1,duration:.22}},{c['start']});"
(P/'index.html').write_text(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>如何在投资低谷中坚持自我</title><script src="assets/gsap.min.js"></script><style>@font-face{{font-family:LocalSong;src:url(assets/songti.ttc)}}@font-face{{font-family:LocalSans;src:url(assets/sans.ttc)}}*{{box-sizing:border-box}}html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:#101b2b}}#root{{width:100%;height:100%;position:absolute;inset:0;font-family:LocalSans;color:#f4eee2}}.clip{{position:absolute;inset:0;width:100%;height:100%}}.captionclip{{inset:auto;left:90px;right:90px;top:910px;width:auto;height:90px}}.caption{{font-size:46px;line-height:1.5;text-align:center;background:#101b2b;padding:10px 20px;width:100%;height:90px;}}</style></head><body><div id="root" data-composition-id="hold-yourself" data-width="1920" data-height="1080" data-duration="60" data-fps="60"><div id="theater">{hosts}</div>{cap}<audio id="music" src="assets/bgm.wav" data-start="0" data-duration="60" data-track-index="9" data-volume="1"></audio></div><script>document.fonts.ready.then(()=>{{const tl=gsap.timeline({{paused:true}});{js}window.__timelines['hold-yourself']=tl;}});</script></body></html>''')
def stamp(t,sep=','):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02}{sep}{n%1000:03}'
for ext,sep in [('srt',','),('vtt','.')]:
 (O/f'hold-yourself.zh-CN.{ext}').write_text(('WEBVTT\n\n'if ext=='vtt'else'')+'\n\n'.join(f'{i+1}\n{stamp(c["start"],sep)} --> {stamp(c["end"],sep)}\n{c["text"]}'for i,c in enumerate(cues))+'\n')
for i in range(4):
 s=E/f'segment_{i+1:02}_{i*15:02}-{(i+1)*15:02}s';(s/'frames').mkdir(parents=True,exist_ok=True);(s/'output').mkdir(exist_ok=True)
 copy='\n'.join(c['text']for c in cues if c['start']<(i+1)*15 and c['end']>i*15)
 for name in ['storyboard.md','first-frame.md','last-frame.md','prompt.md','director-promt.txt','api-request.md']:
  (s/name).write_text(f'# 第{i+1}段 · {i*15}–{(i+1)*15}秒\n\n1920×1080 / 60fps，音乐原速，HyperFrames本地动画。\n\n{copy}\n\n完整运镜、卡点与素材来源见production/hold-yourself/STORYBOARD.md。首尾帧从主片精确提取。外部视频API未调用。\n')
print('built',P)

# Post-build normalization preserves final verified source.
for f in P.glob('compositions/frames/*.html'):
 s=f.read_text().replace(f'{f.stem}-world',f'world-{f.stem}').replace('<style>','<style>@font-face{font-family:LocalSans;src:url(assets/sans.ttc)}@font-face{font-family:LocalSong;src:url(assets/songti.ttc)}',1)
 f.write_text(s)
from pathlib import Path
p=P
fixes={
'01-pressure':"tl.set(['#p-phone','#p-h1','#p-h2','#p-note'],{autoAlpha:0},5.921);tl.set('#p-question',{autoAlpha:0},8.057);tl.set('#p-future',{autoAlpha:0},12.307);",
'02-perspective':"tl.set('#h-pages',{autoAlpha:0},4.295);tl.set('#h-later',{autoAlpha:0},8.545);tl.set('#h-then',{autoAlpha:0},12.794);tl.set('#h-worth',{autoAlpha:0},17.043);",
'03-life':"tl.set(['#a-title','#a-panel0','#a-panel1','#a-panel2'],{autoAlpha:0},10.635);tl.set('#a-adjust',{autoAlpha:0},16.486);"}
for name,js in fixes.items():
 f=p/f'compositions/frames/{name}.html';s=f.read_text().replace('window.__timelines',js+'window.__timelines',1)
 if name=='03-life':s=s.replace('id="a-living"','id="a-living" style="position:absolute;inset:0"').replace('id="a-final"','id="a-final" style="position:absolute;inset:0"')
 f.write_text(s)
