"""六组会前进、回退、分叉的容错率动画；全事件锚定原曲实测拍点。"""
from pathlib import Path
import json, math, html

ROOT=Path(__file__).resolve().parent
STORY=ROOT.parent.parent
EP=STORY/'episodes/EP002_fault-tolerance-v2'
BEATS=json.loads((ROOT/'beats.json').read_text())['beats']
def B(i):return BEATS[i]['time']
SCENES=[]
EVENTS=[]
def scene(num,name,first,last,center=(0,0),zoom=1):
    s=dict(id=f'journey-{num}',name=name,start=B(first) if first else 0,end=B(last) if last<113 else 60,first=first,last=last,nodes=[],edges=[],route=[],center=center,zoom=zoom)
    SCENES.append(s);return s
def node(s,name,x,y,label='',key=False):
    n=dict(id=name,x=x,y=y,label=label,key=key);s['nodes'].append(n);return name
def edge(s,a,b,i,j,chosen=False,bend=0,fail=None,retract=None,dim=False):
    ns={n['id']:n for n in s['nodes']};p,q=ns[a],ns[b];dx=q['x']-p['x'];dy=q['y']-p['y'];length=max(1,math.hypot(dx,dy));nx=-dy/length;ny=dx/length
    d=f'M {p["x"]} {p["y"]} C {p["x"]+dx*.28+nx*bend:.2f} {p["y"]+dy*.28+ny*bend:.2f} {p["x"]+dx*.72+nx*bend:.2f} {p["y"]+dy*.72+ny*bend:.2f} {q["x"]} {q["y"]}'
    e=dict(id=f'{s["id"]}-e{len(s["edges"])}',a=a,b=b,d=d,start=B(i),end=B(j),chosen=chosen,dim=dim)
    if fail is not None:e['fail']=B(fail);EVENTS.append(dict(type='断线',time=B(fail),scene=s['id'],edge=e['id']))
    if retract:e['retract']=[B(retract[0]),B(retract[1])];EVENTS.append(dict(type='收线',time=B(retract[0]),end=B(retract[1]),scene=s['id'],edge=e['id']))
    s['edges'].append(e);EVENTS.append(dict(type='路径生长',time=B(i),end=B(j),scene=s['id'],edge=e['id']));return e
def travel(s,e,i,j,reverse=False):
    s['route'].append(dict(edge=e['id'],start=B(i),end=B(j),a=1 if reverse else 0,b=0 if reverse else 1))
    EVENTS.append(dict(type='回退' if reverse else '前进点亮',time=B(i),end=B(j),scene=s['id'],edge=e['id']))
def leaves(s,parent,at,spread=260,count=3,labelset=()):
    ns={n['id']:n for n in s['nodes']};p=ns[parent]
    for k in range(count):
        x=p['x']+(k-(count-1)/2)*spread;y=p['y']-230-((k+1)%2)*70
        name=f'option-{len(s["nodes"])}';node(s,name,x,y,labelset[k] if k<len(labelset) else '')
        edge(s,parent,name,min(at+k,111),min(at+k+3,113),bend=(k-1)*18,dim=True)

# 01：理想直线真的断掉，光点沿刚才的路返回路口，再向右改道。
s=scene(1,'单行道的错觉',0,16,center=(0,-80),zoom=1.08)
for a,x,y,label in [('a',0,420,'18岁 · 考试'),('b',0,130,'22岁 · 毕业'),('c',0,-170,'25岁 · 工作'),('d',0,-470,'原定的未来'),('l',-360,-430,'再试一次'),('r',360,-450,'换一种走法')]:node(s,a,x,y,label,True)
e0=edge(s,'a','b',0,3,True);e1=edge(s,'b','c',3,6,True);e2=edge(s,'c','d',6,10,True,fail=10,retract=(12,14))
for e,i,j in [(e0,0,3),(e1,3,6),(e2,6,10)]:travel(s,e,i,j)
travel(s,e2,12,14,True)
edge(s,'c','l',12,15,bend=-28)
er=edge(s,'c','r',14,16,True,bend=45);travel(s,er,14,16)

# 02：向前、撞墙、回退、左转，走到下一个岔口再选一次。
s=scene(2,'退回路口，重新选择',16,36,center=(-130,-220),zoom=1.1)
for a,x,y,label in [('a',0,470,'此刻'),('b',0,170,'路口'),('c',340,-80,'这条暂时不通'),('d',-330,-130,'换个方向'),('e',-240,-450,'新的选择'),('f',-530,-740,'一次尝试'),('g',70,-840,'继续向前')]:node(s,a,x,y,label,True)
ea=edge(s,'a','b',16,20,True,bend=25);eb=edge(s,'b','c',20,22,True,bend=40,fail=22,retract=(23,25));ec=edge(s,'b','d',25,28,True,bend=-40);ed=edge(s,'d','e',28,31,True,bend=-50);ee=edge(s,'e','f',31,33,True,bend=-30,fail=33,retract=(33,34));ef=edge(s,'e','g',34,36,True,bend=50)
for e,i,j,r in [(ea,16,20,0),(eb,20,22,0),(eb,23,25,1),(ec,25,28,0),(ed,28,31,0),(ee,31,33,0),(ee,33,34,1),(ef,34,36,0)]:travel(s,e,i,j,bool(r))
leaves(s,'a',17,300,3);leaves(s,'d',28,240,3);leaves(s,'g',34,180,3)

# 03：一段横向穿行的多级路网；回退后绕行，最后把两个岔路接起来。
s=scene(3,'每一步后面，仍有分支',36,56,center=(20,-190),zoom=1.08)
for a,x,y,label in [('a',-320,430,'重新出发'),('b',40,160,'一次选择'),('c',400,-100,'走不通'),('d',-40,-230,'学新本事'),('e',-390,-420,'换座城市'),('f',-700,-160,'遇见新的人'),('g',-750,-560,'连接新的可能')]:node(s,a,x,y,label,True)
ea=edge(s,'a','b',36,40,True,bend=-45);eb=edge(s,'b','c',40,43,True,bend=50,fail=43,retract=(43,45));ec=edge(s,'b','d',45,48,True,bend=-100);ed=edge(s,'d','e',48,51,True,bend=55);ee=edge(s,'e','f',51,53,True,bend=40);ef=edge(s,'f','g',53,56,True,bend=-60)
for e,i,j,r in [(ea,36,40,0),(eb,40,43,0),(eb,43,45,1),(ec,45,48,0),(ed,48,51,0),(ee,51,53,0),(ef,53,56,0)]:travel(s,e,i,j,bool(r))
leaves(s,'b',39,300,3,('重来','换个环境','去学习'));leaves(s,'d',46,240,3);leaves(s,'e',50,220,3);leaves(s,'g',53,160,3)
edge(s,'g','d',54,56,bend=-170);edge(s,'e','a',52,56,bend=170,dim=True)

# 04：先看到一条整齐的成功路线，再看见它背后的弯路和一次真正的回退。
s=scene(4,'直线背后，藏着试错',56,72,center=(60,0),zoom=.96)
for a,x,y,label in [('a',-460,160,'出发'),('b',-160,160,'尝试'),('c',140,160,'调整'),('d',440,160,'你看见的结果'),('e',440,-170,'你没看见的过程'),('f',650,-430,'走通的那一条')]:node(s,a,x,y,label,True)
ea=edge(s,'a','b',56,59,True);eb=edge(s,'b','c',59,62,True);ec=edge(s,'c','d',62,65,True,retract=(65,67));ed=edge(s,'c','e',67,70,True,bend=-60);ee=edge(s,'e','f',70,72,True,bend=40)
for e,i,j,r in [(ea,56,59,0),(eb,59,62,0),(ec,62,65,0),(ec,65,67,1),(ed,67,70,0),(ee,70,72,0)]:travel(s,e,i,j,bool(r))
for k in range(10):
    a=['a','b','c'][k%3];x=-520+k*115;y=-150-(k%3)*130;n=f'h{k}';node(s,n,x,y)
    edge(s,a,n,60+k%7,63+k%7,bend=(1 if k%2 else -1)*(110+k*3),dim=True)
    if k>2:edge(s,f'h{k-3}',n,62+k%5,66+k%5,bend=60,dim=True)

# 05：整张旧网倒退熄灭，保留光点，然后从同一光点重新分叉。
s=scene(5,'旧路熄灭，仍能重启',72,88,center=(0,-100),zoom=1)
node(s,'seed',0,230,'你还在',True)
for k in range(12):
    a=k*math.tau/12;x=math.cos(a)*470;y=230+math.sin(a)*360;n=f'old{k}';node(s,n,x,y)
    edge(s,'seed',n,64,69,bend=45,fail=73+k%3,retract=(75+k%2,79),dim=True)
    if k:edge(s,f'old{k-1}',n,65,70,bend=45,fail=74,retract=(76,79),dim=True)
for a,x,y,label in [('a',0,0,'先走一步'),('b',300,-240,'新的方向'),('c',-80,-580,'下一条路')]:node(s,a,x,y,label,True)
ea=edge(s,'seed','a',80,82,True);eb=edge(s,'a','b',82,85,True,bend=75);ec=edge(s,'b','c',85,88,True,bend=85)
travel(s,ea,80,82);travel(s,eb,82,85);travel(s,ec,85,88)
leaves(s,'a',81,240,3);leaves(s,'b',84,180,3);leaves(s,'c',86,180,3)

# 06：持续穿行，同时三代分支在拍点逐级长出；最后才拉远看到百条路。
s=scene(6,'把一条路，走成一张网',88,114,center=(0,-420),zoom=1.08)
main=[(0,380),(-150,80),(80,-180),(-150,-460),(80,-730),(360,-980)]
for k,(x,y) in enumerate(main):node(s,f'm{k}',x,y,['此刻','再试一次','改变方法','继续向前','新的路口','未来仍在展开'][k],True)
for k in range(5):
    e=edge(s,f'm{k}',f'm{k+1}',88+k*4,92+k*4,True,bend=(-1 if k%2 else 1)*65);travel(s,e,88+k*4,92+k*4)
for root in range(1,6):
    x,y=main[root]
    for arm in range(3):
        sign=-1 if arm==0 else 1
        cx=x+(arm-1)*230;cy=y-210-(arm%2)*90;n=f'r{root}a{arm}';node(s,n,cx,cy)
        i=min(88+root*3+arm,107);edge(s,f'm{root}',n,i,i+3,bend=(arm-1)*35,dim=True)
        for g in range(2):
            dx=cx+(g-.5)*180;dy=cy-200;p=f'{n}b{g}';node(s,p,dx,dy);j=min(i+3+g,109);edge(s,n,p,j,min(j+3,112),bend=(g-.5)*55,dim=True)
            for h in range(2):
                q=f'{p}c{h}';node(s,q,dx+(h-.5)*120,dy-160-(h%2)*60);z=min(j+3+h,111);edge(s,p,q,z,min(z+2,113),bend=(h-.5)*22,dim=True)
for k in range(1,5):edge(s,f'r{k}a2',f'r{k+1}a0',102+k,107+k,bend=120,dim=True)

script=[
 (0,'你以为，人生只有一条路。','每一步，都得刚好走对。'),
 (6,'选错一步，就全盘结束？','路断了，人还在。'),
 (16,'退回路口，','不等于回到起点。'),
 (24,'换一条路，','还可以继续往前。'),
 (32,'一次选择后面，','还有下一次选择。'),
 (36,'重来。换城。学一门本事。','新的路，从尝试里长出来。'),
 (44,'这一条走不通，','就退一步，试另一条。'),
 (50,'绕过的路，','也能连接新的可能。'),
 (56,'你看见别人，一路向前。','却没看见，他怎样走到这里。'),
 (62,'那些没有走通的尝试，','不一定写进最后的故事。'),
 (67,'走通的那一条，','背后也有回退和改道。'),
 (72,'有时，旧路真的全断了。','先留住那个还在的自己。'),
 (80,'从此刻，再长出一条。','先走一步，再看下一步。'),
 (88,'容错率，不是永远不跌倒。','是跌倒以后，仍有路可走。'),
 (96,'走过的路，会连成网。','下一次选择，还在前面。'),
 (104,'失败的，是一次选择。','继续走的，是你。'),
 (108,'人生，允许改道。','你不必一次，就走到答案。')]
CUES=[]
for k,(i,a,b) in enumerate(script):CUES.append(dict(start=0 if not i else B(i),end=B(script[k+1][0]) if k+1<len(script) else 60,title=a,sub=b))
DATA=dict(scenes=SCENES,beats=[b for b in BEATS if b['time']<60],cues=CUES,events=EVENTS)
(ROOT/'journey-data.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2))
headers=''.join(f'<section id="caption-{k}" class="caption"><div class="title{(" red" if k in (1,11,15) else "")}">{html.escape(c["title"])}</div><div class="subtitle">{html.escape(c["sub"])}</div></section>' for k,c in enumerate(CUES))
doc='''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920"><title>人生容错率 · 路会重新长出来</title><script src="assets/gsap.min.js"></script><style>
@font-face{font-family:SongtiLocal;src:url('assets/songti.ttc')}*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#090b08;color:#f3edd8;font-family:SongtiLocal,serif}#root{position:relative;width:100%;height:100%;overflow:hidden;background:#090b08}.clip{position:absolute;inset:0}#ground{background:radial-gradient(ellipse at 50% 58%,#242017 0%,#11130d 40%,#090b08 75%)}#journey-svg{width:100%;height:100%;position:absolute;inset:0;overflow:hidden}.caption{position:absolute;left:70px;top:248px;width:940px;text-align:center;line-height:1.6;letter-spacing:2px;opacity:0}.title{font-size:60px;font-weight:600;white-space:nowrap}.subtitle{font-size:45px;margin-top:17px;white-space:nowrap;color:#ddd6c0}.red{color:#f18b7d}.series{position:absolute;left:94px;top:1668px;letter-spacing:7px;font-size:23px;color:#b7ad91}.route-name{position:absolute;left:94px;top:1610px;letter-spacing:4px;font-size:28px;color:#d6c69d}.node-label{fill:#eee2c0;font-family:SongtiLocal,serif;font-weight:400;paint-order:stroke;stroke:#11130d;stroke-width:5;stroke-linejoin:round}.ghost{fill:#c9b888}.edge-base,.edge-glow{fill:none;stroke-linecap:round;stroke-linejoin:round}.trail-dot{fill:#fff2c4}#flash{background:radial-gradient(ellipse at 50% 56%,rgba(237,205,132,.18),transparent 64%);opacity:0;pointer-events:none}
</style></head><body><div id="root" data-composition-id="fault-tolerance-v2" data-width="1080" data-height="1920" data-duration="60" data-fps="30"><div id="ground" class="clip" data-start="0" data-duration="60" data-track-index="0"></div><div id="drawing" class="clip" data-start="0" data-duration="60" data-track-index="1"><svg id="journey-svg" viewBox="0 0 1080 1920" aria-label="六组不断生长、回退、分叉和重新点亮的人生路径" data-layout-allow-overflow><defs><filter id="bloom" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3.5"/></filter><filter id="dot-glow" x="-400%" y="-400%" width="900%" height="900%"><feGaussianBlur stdDeviation="8" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="black"/><stop offset=".12" stop-color="white"/><stop offset=".86" stop-color="white"/><stop offset="1" stop-color="black"/></linearGradient><mask id="window" maskUnits="userSpaceOnUse" x="0" y="490" width="1080" height="1100"><rect x="0" y="490" width="1080" height="1100" fill="url(#fade)"/></mask></defs><g id="journey-stage" mask="url(#window)"></g></svg></div><div id="flash" class="clip" data-start="0" data-duration="60" data-track-index="2"></div><div id="writing" class="clip" data-start="0" data-duration="60" data-track-index="3">HEADERS<div id="route-name" class="route-name"></div><div class="series">人生容错率 · 路会重新长出来</div></div><audio id="reference-music" src="assets/reference-soundtrack.m4a" data-start="0" data-media-start="0" data-duration="60" data-timeline-role="music" data-volume="1" data-track-index="4"></audio></div><script>const JOURNEY=DATA;
ENGINE
</script></body></html>'''
doc=doc.replace('HEADERS',headers).replace('DATA',json.dumps(DATA,ensure_ascii=False,separators=(',',':'))).replace('ENGINE',(ROOT/'engine.js').read_text())
(ROOT/'index.html').write_text(doc)

def tc(t,sep=','):
 m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02}{sep}{m%1000:03}'
def subs(where,cs,offset=0,name='fault-tolerance-v2.zh-CN'):
 where.mkdir(parents=True,exist_ok=True);srt=[];vtt=['WEBVTT\n']
 for n,c in enumerate(cs,1):
  a,b=tc(c['start']-offset),tc(c['end']-offset);text=c['title']+'\n'+c['sub'];srt.append(f'{n}\n{a} --> {b}\n{text}\n');vtt.append(f'{a.replace(",",".")} --> {b.replace(",",".")}\n{text}\n')
 (where/f'{name}.srt').write_text('\n'.join(srt));(where/f'{name}.vtt').write_text('\n'.join(vtt))
subs(EP/'output',CUES)
board=['# 容错率 V2：六组可逆生长路网\n','不再使用上一版固定树形图。每组均有独立节点、路径、生长计划与光点行程。路径画出、断线、回缩、回退、转向与到达时间全部来自原曲实测拍点。\n','规则：svg-path-draw / viewport-change / multi-phase-camera；检索 offset-path-traveler、svg-line-draw-loader 后，将路径进度与回退扩展为本片的确定性行程引擎。\n']
for s in SCENES:board.append(f'## {s["id"]} {s["name"]}\n\n{s["start"]:.3f}–{s["end"]:.3f} 秒，{len(s["edges"])} 条路径，{len(s["route"])} 段光点行程。'+ ('含实际回退。' if any(r['b']==0 for r in s['route']) else ''))
(ROOT/'STORYBOARD.md').write_text('\n\n'.join(board))
(ROOT/'beat-actions.csv').write_text('动作,开始秒,结束秒,场景,路径\n'+'\n'.join(f'{e["type"]},{e["time"]:.3f},{e.get("end",e["time"]):.3f},{e["scene"]},{e["edge"]}' for e in EVENTS))
chapters=[('00-15s','直线断掉，回退路口'),('15-30s','连续改道与多级分支'),('30-45s','试错显现、旧路熄灭、重新起步'),('45-60s','继续前进，生长为网')]
for k,(slug,title) in enumerate(chapters):
 seg=EP/f'segment_{k+1:02}_{slug}';(seg/'frames').mkdir(parents=True,exist_ok=True);(seg/'output').mkdir(exist_ok=True);start=k*15;end=start+15
 cs=[dict(c,start=max(c['start'],start),end=min(c['end'],end)) for c in CUES if c['end']>start and c['start']<end]
 (seg/'storyboard.md').write_text(f'# {title}\n\n参考 production/fault-tolerance-v2/STORYBOARD.md 与 beat-actions.csv。\n\n'+ '\n'.join(f'- {c["start"]:.3f}–{c["end"]:.3f}s：{c["title"]} {c["sub"]}' for c in cs))
 for name,t in [('first',start),('last',end-1/30)]: (seg/f'{name}-frame.md').write_text(f'# {name} frame\n\n使用同一可逆路径引擎在全片 {t:.3f} 秒的确定性状态，输出 frames/{name}-frame.png。首尾连续继承光点、路径进度与镜头姿态，不重新生图。')
 prompt=f'9:16，1080×1920，15秒以内，抽象矢量路径动画。{title}。深墨色底、暖金细线、宋体、真实逐笔生长与反向收回、节点扩散点亮。镜头沿光点前进并跨越多个岔路，不以固定图推拉代替路径变化。BGM为原片we never若如初见的{start}–{end}秒，不变速，无新增配音。按beat-actions.csv的实测拍点出发/到达。实际首尾帧来自本地渲染，不调用外部视频API。'
 (seg/'prompt.md').write_text(prompt);(seg/'director-promt.txt').write_text(prompt)
 (seg/'api-request.md').write_text('# 本地渲染\n\n引擎：HyperFrames 0.8.170 + 可逆SVG行程引擎。外部API：NOT_RUN。状态：待完成抽段。\n\n源工程 production/fault-tolerance-v2/index.html，输出 output/video.mp4。')
 subs(seg/'output',cs,start,'segment.zh-CN')
print(json.dumps({'scenes':len(SCENES),'edges':sum(len(s['edges']) for s in SCENES),'backtracks':sum(r['b']==0 for s in SCENES for r in s['route']),'cues':len(CUES),'events':len(EVENTS)},ensure_ascii=False))
