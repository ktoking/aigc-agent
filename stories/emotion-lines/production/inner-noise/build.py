"""离线生成本片的可编辑 HTML、节拍映射、字幕与四段制作包。"""
from pathlib import Path
import json, math, html, shutil

ROOT = Path(__file__).resolve().parent
STORY = ROOT.parent.parent
EP = STORY / 'episodes/EP001_inner-noise'
beats = json.loads((ROOT/'beats/assets/reference-soundtrack.m4a.json').read_text())['beats']
def snap(t):
    return round(min(beats, key=lambda b: abs(b['time']-t))['time'], 3)

phrases = [
 (0, '一次失误，能有多大？', '那个被放大的瞬间'),
 (3.2, '一句话说错了。', '一场面试没发挥好。'),
 (6.4, '你开始反复回放。', '每想一次，它就大一点。'),
 (9.6, '把一个瞬间，', '放大成了全部。'),
 (12.3, '最后，对自己说：', '“我就是不行。”'),
 (15.5, '可你也许只是——', '靠得太近。'),
 (18.7, '试着退后一点。', '看看它之外，还有什么。'),
 (22, '那只是一个节点，', '不是你的全部。'),
 (25.3, '你做成过的事，', '没有因此消失。'),
 (28.4, '先别急着定义自己。', '把目光，放回这件事。'),
 (31.6, '把「我不行」，', '换成一个具体问题。'),
 (34.8, '是准备不足？', '还是方法不合适？'),
 (38, '能补的，去补。', '能改的，去改。'),
 (41.2, '暂时改不了的，', '也可以先放一放。'),
 (44.5, '一次失误，', '不需要用整个人来偿还。'),
 (47.8, '今天可以有遗憾。', '明天仍然可以有下一步。'),
 (51, '别把一次失误，', '判成整个人失败。'),
 (54.4, '你可以犯一次错。', '也可以继续往前走。'),
 (57.5, '给自己，', '留一条继续走的路。'),
]
cues = []
for i,(t,a,b) in enumerate(phrases):
    start=0 if i==0 else snap(t)
    end=snap(phrases[i+1][0]) if i+1<len(phrases) else 60
    cues.append(dict(start=start,end=end,title=a,sub=b))
(ROOT/'beat-map.json').write_text(json.dumps(dict(source='原片原始 AAC 音轨；BGM 名称由用户确认：we never（若如初见）',bpm_estimate=112.9,source_in=0,source_out=60,playback_rate=1,cues=cues,beats=[b for b in beats if b['time']<60]),ensure_ascii=False,indent=2))
def tc(t,sep=','):
    ms=round(t*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}{sep}{ms%1000:03}'

def subtitles(where,items,offset=0,name='inner-noise.zh-CN'):
    where.mkdir(parents=True,exist_ok=True)
    srt=[];vtt=['WEBVTT\n']
    for n,c in enumerate(items,1):
        a,b=c['start']-offset,c['end']-offset
        text=c['title']+'\n'+c['sub']
        srt.append(f'{n}\n{tc(a)} --> {tc(b)}\n{text}\n')
        vtt.append(f'{tc(a,".")} --> {tc(b,".")}\n{text}\n')
    (where/f'{name}.srt').write_text('\n'.join(srt))
    (where/f'{name}.vtt').write_text('\n'.join(vtt))
subtitles(EP/'output',cues)

text_html=[]
for i,c in enumerate(cues):
    color=' accent' if i in (3,4,10,16) else ''
    text_html.append(f'<section class="phrase" id="phrase-{i}"><div class="headline{color}">{html.escape(c["title"])}</div><div class="subline">{html.escape(c["sub"])}</div></section>')

# 主路径和分支所有几何均为新作；不会拼贴参考作者画面。
main='M540 1450 C500 1340 590 1250 540 1080 C488 930 640 800 575 620'
branches=[];leaves=[]
for j,(x,y,label) in enumerate([(210,1330,'照顾自己'),(860,1340,'按时完成'),(160,1070,'愿意尝试'),(920,1050,'认真生活'),(240,760,'重新学习'),(860,730,'帮过别人')]):
    sy=[1310,1310,1090,1090,850,850][j]
    d=f'M540 {sy} C{540+(x-540)*.22:.1f} {sy-80} {x} {y+100} {x} {y}'
    branches.append(f'<path class="branch" id="branch-{j}" d="{d}"/>')
    leaves.append(f'<g class="leaf" id="leaf-{j}"><circle class="node" cx="{x}" cy="{y}" r="5"/><text x="{x}" y="{y-28}" text-anchor="middle">{label}</text></g>')
    for k in range(4):
        dx=(k-1.5)*57; ey=y-70-k%2*65
        branches.append(f'<path class="twig" id="twig-{j}-{k}" d="M{x} {y+40} Q{x+dx*.3} {y-25} {x+dx:.1f} {ey}"/>')

# 次级联结让“生活网络”真正互相连通，避免只画成六根树枝。
web=[]
for side in (-1,1):
    for n in range(7):
        x=540+side*(130+n*38)
        y=690+n*106
        web.append(f'<path class="web" d="M{x:.1f} {y:.1f} C{x-side*70:.1f} {y+68:.1f} {x-side*115:.1f} {y+92:.1f} {x-side*150:.1f} {y+208:.1f}"/>')
        web.append(f'<path class="web" d="M{x:.1f} {y:.1f} Q{x+side*105:.1f} {y+80:.1f} {x+side*95:.1f} {y+185:.1f}"/>')
for n in range(5):
    y=730+n*130
    web.append(f'<path class="web" d="M{240+n%2*25} {y} C420 {y+130} 660 {y-45} {850-n%2*30} {y+90}"/>')

loops=[]
for i in range(5):
    rx=90+i*29;ry=50+i*18
    loops.append(f'<ellipse id="loop-{i}" class="rumination" cx="540" cy="1080" rx="{rx}" ry="{ry}"/>')

html_doc='''<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920">
<title>内耗｜别把一次失误，判成整个人失败</title><script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:SongtiLocal;src:url('assets/songti.ttc')}*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#0b0c08;color:#f3edd8;font-family:SongtiLocal,serif}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:#0b0c08}.clip{position:absolute;inset:0}.atmosphere{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 55%,#242116 0%,#12120c 35%,#0b0c08 72%)}
.grain{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 60%,rgba(182,149,83,.04),transparent 64%)}
.phrase{position:absolute;left:90px;top:285px;width:900px;text-align:center;opacity:0;line-height:1.55;letter-spacing:2px}.headline{font-size:62px;font-weight:600;white-space:nowrap}.subline{font-size:52px;margin-top:18px;font-weight:400;white-space:nowrap}.accent{color:#e67470}
#graph{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}path{fill:none;stroke-linecap:round;stroke-linejoin:round}.main{stroke:#f3edd8;stroke-width:3.4;filter:url(#soft-glow)}.branch{stroke:#c4bda7;stroke-width:1.9}.twig{stroke:#8f8978;stroke-width:1.05}.web{stroke:#a79d81;stroke-width:1;opacity:.38}.leaf{fill:#d6cdb6;opacity:0}.leaf text{font-family:SongtiLocal,serif;font-size:34px;fill:#e4dcc6}.node{fill:#fff6ce;filter:url(#soft-glow)}.rumination{fill:none;stroke:#e67470;stroke-width:1;opacity:0}.error-dot{fill:#e67470;filter:url(#red-glow)}
#red-wash{position:absolute;left:160px;top:700px;width:760px;height:760px;border-radius:50%;background:radial-gradient(ellipse,rgba(167,61,49,.2),rgba(120,36,31,.04) 50%,transparent 70%);opacity:0;pointer-events:none}
#judgment{position:absolute;left:140px;top:1150px;width:800px;text-align:center;color:#e67470;font-size:87px;letter-spacing:8px;opacity:0}
.action{stroke:#fff6ce;stroke-width:3;filter:url(#soft-glow)}.action-label{fill:#f3edd8;font-size:38px;font-family:SongtiLocal,serif;opacity:0}.quiet-label{fill:#c4bda7;font-size:32px;font-family:SongtiLocal,serif;opacity:0}.breath{fill:none;stroke:#c8b88d;stroke-width:.8;opacity:0}.star{fill:#a89973;opacity:.13}
.note{position:absolute;top:1565px;left:140px;width:800px;font-size:32px;text-align:center;line-height:1.9;letter-spacing:3px;color:#c4bda7;opacity:0}.series{position:absolute;left:100px;top:1640px;font-size:25px;letter-spacing:6px;color:#9f9987}.series-line{position:absolute;left:100px;top:1610px;width:44px;height:1px;background:#8e846c}
</style></head><body>
<div id="root" data-composition-id="inner-noise" data-width="1080" data-height="1920" data-duration="60" data-fps="30">
 <div id="background-layer" class="clip" data-start="0" data-duration="60" data-track-index="0"><div class="atmosphere"></div><div class="grain"></div></div>
 <div id="drawing-layer" class="clip" data-start="0" data-duration="60" data-track-index="1"><div id="red-wash"></div>
 <svg id="graph" viewBox="0 0 1080 1920" aria-label="一次失误被放大，又被还原为生活网络中的一个节点" data-layout-allow-overflow>
 <defs><filter id="soft-glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter><filter id="red-glow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="10" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
 <defs><linearGradient id="edge-fade" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="black"/><stop offset="12%" stop-color="white"/><stop offset="90%" stop-color="white"/><stop offset="100%" stop-color="black"/></linearGradient><mask id="graph-window" maskUnits="userSpaceOnUse" x="50" y="550" width="980" height="990"><rect x="50" y="550" width="980" height="990" fill="url(#edge-fade)"/></mask></defs>
 <g mask="url(#graph-window)"><g id="world"><g id="network">WEB BRANCHES LEAVES</g><path id="life-path" class="main" d="MAIN"/>
 <g id="loop-field">LOOPS</g><circle id="failure" class="error-dot" cx="540" cy="1080" r="8" opacity="0"/>
 <g id="actions"><path class="action" id="prepare" d="M540 1080 C520 1010 320 980 270 815"/><path class="action" id="method" d="M540 1080 C575 995 760 950 805 815"/><path class="action" id="forward" d="M540 1080 C490 940 650 800 575 620"/>
 <text class="action-label" id="label-prepare" x="270" y="770" text-anchor="middle">补一点准备</text><text class="action-label" id="label-method" x="805" y="770" text-anchor="middle">换一个方法</text>
 <text class="quiet-label" id="label-wait" x="540" y="1160" text-anchor="middle">暂时搁置，也是一种选择</text></g>
 <circle id="traveler" class="node" r="8"/><circle id="breath" class="breath" cx="540" cy="1080" r="70"/>
 </g></g></svg><div id="judgment">我就是不行</div></div>
 <div id="type-layer" class="clip" data-start="0" data-duration="60" data-track-index="2">PHRASES<div class="note" id="note">把自责，变成一个可以处理的小问题。</div><div class="series-line"></div><div class="series">把心事画成线 · 01</div></div>
 <audio id="reference-music" src="assets/reference-soundtrack.m4a" data-start="0" data-media-start="0" data-duration="60" data-timeline-role="music" data-track-index="3" data-volume="1"></audio>
</div>
<script>
document.fonts.ready.then(()=>{
const tl=gsap.timeline({paused:true});
const cues=CUES, beats=BEATS;
function draw(selector,start,duration){document.querySelectorAll(selector).forEach((p,i)=>{const len=p.getTotalLength();gsap.set(p,{strokeDasharray:len,strokeDashoffset:len});tl.to(p,{strokeDashoffset:0,duration,ease:'power2.inOut'},start+i*.055);});}
function show(selector,start,duration=.65){tl.fromTo(selector,{opacity:0},{opacity:1,duration,ease:'power1.out'},start);}
const at=t=>beats.reduce((a,b)=>Math.abs(b.time-t)<Math.abs(a.time-t)?b:a).time;
draw('#life-path',.045,3.1);
const path=document.getElementById('life-path'), length=path.getTotalLength();
const motion={p:0};const dot=document.getElementById('traveler');
const placeDot=()=>{const p=path.getPointAtLength(motion.p*length);dot.setAttribute('cx',p.x);dot.setAttribute('cy',p.y);};placeDot();
tl.to(motion,{p:.44,duration:3.5,ease:'power2.inOut',onUpdate:placeDot},.045);
show('#failure',at(3.2),.2);
document.querySelectorAll('.rumination').forEach((p,i)=>{const len=p.getTotalLength();gsap.set(p,{strokeDasharray:len,strokeDashoffset:len});tl.to(p,{opacity:.52,strokeDashoffset:0,duration:1.7,ease:'power2.inOut'},at(6.4)+i*.53);});
tl.fromTo('#world',{scale:1},{scale:2.4,svgOrigin:'540 1080',duration:3.2,ease:'power2.inOut',immediateRender:false},at(9.6));
tl.to('#red-wash',{opacity:1,duration:2.5,ease:'power1.inOut'},at(9.6));
show('#judgment',at(12.3),.45);tl.to('#judgment',{opacity:0,duration:.4},at(15.5)-.2);
tl.to('#world',{scale:.88,svgOrigin:'540 1080',duration:3.2,ease:'power3.inOut'},at(15.5));
tl.to('#red-wash',{opacity:0,duration:2.4},at(15.5));
tl.to('.rumination',{opacity:0,duration:2},at(16.6));
draw('.branch',at(18.7),3.4);draw('.twig',at(22),3.4);draw('.web',at(21),4.2);
show('.leaf',at(22),1.1);
tl.to('#failure',{scale:.65,svgOrigin:'540 1080',duration:1.4},at(22));
tl.to(motion,{p:.72,duration:4,ease:'power2.inOut',onUpdate:placeDot},at(25.3));
tl.to('#network',{opacity:.23,duration:1},at(30));
tl.to('#life-path',{opacity:.3,duration:1},at(30));
draw('#prepare',at(31.6),2.6);draw('#method',at(34.8),2.6);
show('#label-prepare',at(34.8));show('#label-method',at(36.9));
tl.to('#failure',{fill:'#fff6ce',duration:2},at(38));
draw('#forward',at(38),4.2);show('#label-wait',at(41.2));
show('#note',at(38),.7);tl.to('#note',{opacity:0,duration:.7},at(44.5));
tl.to('#label-wait,#label-prepare,#label-method',{opacity:0,duration:.8},at(44.5));
tl.to('#network',{opacity:.68,duration:2.4},at(44.5));
tl.to('#life-path',{opacity:1,duration:1.6},at(44.5));
tl.to('#actions',{opacity:0,duration:1.6},at(44.5));
tl.to(motion,{p:1,duration:8.5,ease:'power1.inOut',onUpdate:placeDot},at(47.8));
tl.to('#world',{scale:1.03,svgOrigin:'540 1080',duration:7,ease:'power1.inOut'},at(47.8));
tl.to('#network',{opacity:.25,duration:2},at(54.4));
tl.to('.leaf',{opacity:0,duration:1.5},at(54.4));
beats.filter((b,i)=>b.time<59&&i%4===0).forEach((b)=>{tl.fromTo('#breath',{scale:.5,opacity:.24},{scale:1.4,opacity:0,duration:1.4,svgOrigin:'540 1080',ease:'power1.out',immediateRender:false},b.time);});
cues.forEach((c,i)=>{tl.fromTo('#phrase-'+i,{opacity:0,y:16},{opacity:1,y:0,duration:.38,ease:'power2.out',immediateRender:false},c.start);if(i<cues.length-1)tl.to('#phrase-'+i,{opacity:0,y:-7,duration:.22,ease:'power1.in'},c.end-.22);});
window.__timelines['inner-noise']=tl;
});
</script></body></html>'''
html_doc=html_doc.replace('WEB',''.join(web)).replace('BRANCHES',''.join(branches)).replace('LEAVES',''.join(leaves)).replace('LOOPS',''.join(loops)).replace('MAIN',main).replace('PHRASES',''.join(text_html)).replace('CUES',json.dumps(cues,ensure_ascii=False)).replace('BEATS',json.dumps([b for b in beats if b['time']<60]))
(ROOT/'index.html').write_text(html_doc)

chapters=[('00-15s','失误被放大','直线→失败红点→反复回放环→镜头靠近，红色自我标签出现。'),('15-30s','退后看全貌','从近景连续拉远，展示仍然存在的生活分支与正向节点。'),('30-45s','拆成具体问题','环形自责变为两条可行动的路；保留暂时搁置的选择。'),('45-60s','允许继续向前','主路径重新亮起，光点继续向上；完整短句收束。')]
board=['# 60 秒音乐卡点与镜头表','\n每次论点落点取音轨实测节拍，见 beat-map.json。规则组合：svg-path-draw、viewport-change、dynamic-content-sequencing。单一连续图形场景，四段按交付边界拆分。\n']
for i,(slug,title,action) in enumerate(chapters,1):
    start=(i-1)*15;end=i*15
    seg=EP/f'segment_{i:02}_{slug}';(seg/'frames').mkdir(parents=True,exist_ok=True);(seg/'output').mkdir(exist_ok=True)
    selected=[dict(c,start=max(c['start'],start),end=min(c['end'],end)) for c in cues if c['end']>start and c['start']<end]
    rows='\n'.join(f'| {c["start"]:.3f}–{c["end"]:.3f} | {c["title"]} {c["sub"]} |' for c in selected)
    sb=f'# 第 {i} 段：{title}\n\n{action}\n\n| 全片时间 / 秒 | 画面论点 |\n| --- | --- |\n{rows}\n\nBGM 连续使用原片 {start}–{end} 秒，不单独重启、不变速。'
    (seg/'storyboard.md').write_text(sb);board.append(sb)
    for state,t in [('first',start),('last',end-1/30)]:
        (seg/f'{state}-frame.md').write_text(f'# {"首帧" if state=="first" else "尾帧"}\n\n使用本地 HTML 时间线在全片 {t:.3f} 秒的确定性渲染状态。深墨色底，嵌入宋体，暖白细线，节点柔光。{action}\n\n实际文件：frames/{state}-frame.png。由成片抽帧，不调用图像生成 API。')
    prompt=f'# 本地动画导演提示\n\n9:16，1080×1920，15 秒，明显非真人的抽象路径动画。{action}\n\n首帧、尾帧继承本集同一几何与光点；不增加角色。背景 #0b0c08，暖白 #f3edd8，语义红 #e67470；宋体。\n\nBGM：《we never（若如初见）》，参考片原音轨 {start}–{end} 秒。无配音。卡点与文字以 beat-map.json 为准。\n\n运镜为连续推拉，不随机跳切。禁止游戏 HUD、卡片网格、过量锐化、未核验统计数据。\n\n制作引擎：HyperFrames HTML + GSAP。本段不提交视频 API。'
    (seg/'prompt.md').write_text(prompt);(seg/'director-promt.txt').write_text(prompt)
    (seg/'api-request.md').write_text('# 本地渲染记录\n\n- 平台：本地 HyperFrames 0.8.170 + FFmpeg。\n- 外部视频 API：NOT_RUN，本片为确定性矢量动画，无需调用。\n- 状态：待成片抽段，由 delivery-qa.json 回填。\n- 源工程：production/inner-noise/index.html。\n- 结果：output/video.mp4。\n- 重试：修改局部时间线后重渲染，不替换原始参考。')
    subtitles(seg/'output',selected,offset=start,name='segment.zh-CN')
(ROOT/'STORYBOARD.md').write_text('\n\n'.join(board))
(EP/'publish-package.md').write_text('# 发布候选\n\n标题：\n- 别把一次失误，判成整个人失败\n- 你也许不是不行，只是靠得太近\n- 把心事画成线：给自己留一条路\n\n封面：失败节点旁的暖白分支，画面大字“不是你的全部”。\n\n评论引导：你最近想对自己宽容一点的事，是什么？\n\n标签：#认知 #停止内耗 #成长\n\nBGM 名称由用户指定；仅完成本地交付，未发布。')
print(json.dumps({'html':str(ROOT/'index.html'),'cues':len(cues),'segments':4,'duration':60},ensure_ascii=False))
