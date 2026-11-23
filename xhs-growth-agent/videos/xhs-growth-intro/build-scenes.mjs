import fs from 'node:fs';
import path from 'node:path';

// All motion is authored against one paused, seekable timeline per scene.
// Registry references: shared-axis-y, morph-swap, svg-line-draw-loader.
const C={cream:'#F5F5F0',ink:'#1A1A1A',coral:'#E85D4E',lime:'#C4D94E',lavender:'#C5B5E0',sky:'#8BB4F7',mint:'#A8E6CF',white:'#FFFFFF'};
const frames=[];
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;');
const box=(cls,style,content='')=>`<div class="${cls}" style="${style}">${content}</div>`;
const label=(text,x,y,size=34,color=C.ink)=>box('label',`left:${x}px;top:${y}px;font-size:${size}px;color:${color}`,text);
const pill=(text,x,y,w=250,bg=C.white,extra='')=>box('pill',`left:${x}px;top:${y}px;width:${w}px;background:${bg};${extra}`,text);
const svg=(content,style='',view='0 0 1080 1100')=>`<svg viewBox="${view}" style="position:absolute;${style}" fill="none" xmlns="http://www.w3.org/2000/svg">${content}</svg>`;
const line=(d,color=C.ink,width=5,cls='draw')=>`<path class="${cls}" d="${d}" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>`;
const note=(text,style='',cls='note')=>box(cls,style,`<div class="note-dot"></div><div class="note-title">${text}</div><div class="note-bar"></div><div class="note-bar" style="width:74%"></div><div class="note-bar" style="width:86%"></div>`);
const head=(a,b,third='')=>`<div class="headline">${[a,b,third].filter(Boolean).map((s,i)=>`<div class="line"><span class="word ${i===1?'accent':''}">${s}</span></div>`).join('')}</div>`;
const common=`
@font-face{font-family:'Noto Sans SC';font-style:normal;font-weight:100 900;src:url('assets/fonts/NotoSC.woff2') format('woff2');font-display:block}
*{box-sizing:border-box}#root{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;container-type:size;color:${C.ink};font-family:'Noto Sans SC',sans-serif}
.clip{position:absolute;inset:0}.stage{position:absolute;inset:0;overflow:hidden}.headline{position:absolute;left:80px;top:205px;width:930px;font-size:103px;font-weight:850;letter-spacing:-5px;line-height:1.29}.line{overflow:hidden;padding-bottom:9px}.word{display:inline-block}.accent{color:${C.coral}}
.label{position:absolute;font-weight:550;letter-spacing:1px;white-space:nowrap}.pill{position:absolute;height:94px;border:3px solid ${C.ink};border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:650;letter-spacing:1px;box-shadow:6px 7px 0 #1a1a1a10}
.note{position:absolute;border:3px solid ${C.ink};border-radius:30px;background:white;padding:38px;box-shadow:9px 11px 0 #1a1a1a10;overflow:hidden}.note-dot{width:25px;height:25px;border:2px solid ${C.ink};border-radius:50%;background:${C.coral};margin-bottom:25px}.note-title{font-size:35px;font-weight:700;white-space:nowrap;margin-bottom:30px}.note-bar{height:10px;width:90%;border-radius:8px;background:#1a1a1a24;margin-bottom:20px;transform-origin:left center}
.ghost{position:absolute;border:2px solid ${C.ink};border-radius:28px;background:${C.lavender};opacity:.2}
.hero{position:absolute;transform-origin:50% 50%}.thin{stroke-width:4;stroke:${C.ink};stroke-linecap:round;stroke-linejoin:round;fill:none}.small{font-size:30px}
`;
const runtime=`
const r=document.getElementById(PREFIX+'-stage');
const q=s=>r.querySelectorAll(s), one=s=>r.querySelector(s);
const tl=gsap.timeline({paused:true});
function arrive(s,at=0,from={y:65,opacity:0},dur=.9){tl.fromTo(q(s),from,{x:0,y:0,scale:1,rotation:0,opacity:1,duration:dur,ease:'power3.out',stagger:.075},at)}
function stroke(s,at,dur=1.2){q(s).forEach((p,i)=>{const n=p.getTotalLength();p.style.strokeDasharray=n;p.style.strokeDashoffset=n;tl.fromTo(p,{strokeDashoffset:n},{strokeDashoffset:0,duration:dur,ease:'power2.inOut',immediateRender:false},at+i*.12)})}
if(PREFIX==='f01-studio'){arrive('.line:not(:first-child) .word',.18,{y:150,opacity:0},1.05);}else{arrive('.word',.12,{y:150,opacity:0},1.05);}
`;

function scene(id,duration,title,body,motion,css='',bg=C.cream){
  const p=`f${String(frames.length+1).padStart(2,'0')}-${id}`;
  const content=`<template><style>${common}${css}</style><div id="root" data-composition-id="${p}" data-width="1080" data-height="1920" data-duration="${duration}"><div id="${p}-bg" class="clip" data-start="0" data-duration="${duration}" data-track-index="0" style="background:${bg}"></div><div id="${p}-stage" class="stage">${body}</div></div><script>(()=>{const PREFIX='${p}';${runtime}${motion}\nwindow.__timelines['${p}']=tl;})();</script></template>`;
  const file=`compositions/frames/${p}.html`;
  fs.writeFileSync(file,content);
  frames.push({id:p,file,duration,title});
}

scene('studio',7,'一个人的内容工作室',
  head('一个人，','一整个','内容工作室')+
  box('workspace hero','left:135px;top:820px;width:810px;height:470px',
    svg(`<rect class="draw" x="2" y="2" width="806" height="466" rx="42" fill="white" stroke="${C.ink}" stroke-width="4"/>${line('M4 85H806')}<circle cx="40" cy="43" r="9" fill="${C.coral}"/><circle cx="75" cy="43" r="9" fill="${C.lime}"/><circle cx="110" cy="43" r="9" fill="${C.lavender}"/>`,'inset:0;width:100%;height:100%','0 0 810 470')+
    note('一个想法','left:48px;top:135px;width:220px;height:280px;background:#F5F5F0')+
    box('tools','left:310px;top:160px;position:absolute',
      ['选题','写作','审核','发布'].map((s,i)=>pill(s,(i%2)*220,Math.floor(i/2)*130,190,[C.lime,C.lavender,C.sky,C.mint][i],'height:90px')).join('')))+
  label('XHS GROWTH AGENT',80,1435,33)+
  svg(line('M480 30C480 90 490 140 490 205',C.coral,8),'left:0;top:610px;width:1080px;height:600px','0 0 1080 600'),
  `tl.fromTo(q('.workspace'),{scale:.8,y:120,rotation:-7,opacity:0},{scale:1,y:0,rotation:0,opacity:1,duration:1.4,ease:'power3.out'},2.4);stroke('.workspace .draw',2.7,.9);arrive('.note',3.3,{x:-90,y:25,opacity:0},1.1);arrive('.pill',4.3,{x:80,y:0,scale:.6,opacity:0},.85);arrive('.label',5.45);stroke('svg>.draw',4.9,1.1);`,
  `.headline{top:180px;font-size:123px;line-height:1.24}.headline .line:nth-child(3){font-size:123px}.workspace .note-title{font-size:29px}.workspace .note{padding:27px}.workspace .note-bar{margin-bottom:17px}`);

const phrase='周末，别把休息排满。';
scene('direction',7,'从你的方向开始',
  head('先有想法，','再有内容。')+
  box('thought hero','left:135px;top:650px;width:810px;height:250px',
    svg(`<path class="draw" d="M60 5H750Q805 5 805 60V175Q805 230 750 230H240L180 275V230H60Q5 230 5 175V60Q5 5 60 5Z" fill="white" stroke="${C.ink}" stroke-width="4"/>`,'inset:0;width:100%;height:280px','0 0 810 280')+
    box('typed','position:absolute;left:55px;top:78px;white-space:nowrap;font-size:49px;font-weight:700',Array.from(phrase).map(c=>`<span class="char" style="display:inline-block">${c}</span>`).join('')))+
  pill('生活',135,1040,225,C.lime)+pill('职场',430,1040,225,C.lavender)+pill('消费',725,1040,225,C.sky)+
  svg(line('M295 10C295 145 540 80 540 220',C.ink,5),'left:0;top:1130px;width:1080px;height:230px','0 0 1080 230')+
  pill('准备内容',335,1380,410,C.coral,'height:120px;font-size:47px'),
  `arrive('.thought',.5,{y:120,scale:.9,opacity:0},1.1);stroke('.thought .draw',.55,.9);tl.fromTo(q('.char'),{opacity:0,y:12},{opacity:1,y:0,duration:.12,stagger:.13,ease:'none'},1.45);arrive('.pill',3.35,{y:80,opacity:0},.95);stroke('svg>.draw',4.7,1.05);tl.fromTo(one('.pill:last-child'),{scale:.9},{scale:1,duration:.7,ease:'power3.out',immediateRender:false},5.8);`);

scene('radar',7,'找到合适的选题',
  head('热点很多，','只挑合适的。')+
  box('radar hero','left:105px;top:635px;width:870px;height:870px',
    svg(`<circle class="draw" cx="435" cy="435" r="325" stroke="#1a1a1a20" stroke-width="3"/><circle class="draw" cx="435" cy="435" r="235" stroke="#1a1a1a20" stroke-width="3"/><circle class="draw" cx="435" cy="435" r="140" stroke="#1a1a1a20" stroke-width="3"/><path class="sweep" d="M435 435L435 110A325 325 0 0 1 760 435Z" fill="${C.lime}" fill-opacity=".33"/><path d="M435 90V780M90 435H780" stroke="#1a1a1a14" stroke-width="2"/>`,'inset:0;width:870px;height:870px','0 0 870 870')+
    note('职场','left:25px;top:270px;width:230px;height:260px;background:#FFF')+
    note('消费','left:570px;top:80px;width:230px;height:260px;background:#FFF')+
    note('生活','left:545px;top:535px;width:230px;height:260px;background:#FFF')+
    box('target','position:absolute;left:315px;top:315px;width:240px;height:240px;border-radius:50%;border:4px solid #1a1a1a;background:#E85D4E;display:grid;place-items:center',
      svg(line('M45 125L95 175L195 70',C.ink,13),'left:0;top:0;width:240px;height:240px','0 0 240 240')))+
  pill('近期热点 · 按方向筛选',265,1505,550,C.white,'font-size:31px;height:80px'),
  `arrive('.radar',.4,{scale:.77,y:110,opacity:0},1.25);stroke('.radar circle',.9,1.4);tl.fromTo(q('.sweep'),{rotation:-55,opacity:0,svgOrigin:'435 435'},{rotation:225,opacity:1,svgOrigin:'435 435',duration:4.5,ease:'none'},.8);arrive('.note',1.65,{y:65,scale:.72,opacity:0},1.1);arrive('.target',4.3,{scale:.15,opacity:0},.9);stroke('.target .draw',4.85,.65);arrive('.pill',5.65);`,
  `.radar .note{padding:26px}.radar .note-title{font-size:37px;margin-bottom:22px}.radar .note-dot{margin-bottom:20px}`);

const tones=[['自然',C.white],['批判',C.lime],['客观',C.sky],['主观',C.coral],['犀利',C.white],['温和',C.lavender],['幽默',C.white],['共情',C.mint]];
scene('voice',8,'组合你的表达语气',
  head('同一个题，','不止一种说法。')+
  tones.map(([s,c],i)=>pill(s,135+(i%2)*435,650+Math.floor(i/2)*145,375,c,`height:102px`)).join('')+
  svg(line('M320 0C320 105 540 80 540 195M755 0C755 105 540 80 540 195',C.ink,5),'left:0;top:1220px;width:1080px;height:210px','0 0 1080 210')+
  box('voice-result note','left:135px;top:1380px;width:810px;height:200px;padding:43px;background:white',
      `<div style="font-size:39px;font-weight:700">个人看法 × 看见具体处境</div><div style="font-size:29px;margin-top:19px;color:#444">方向和措辞，都由你来选。</div>`),
  `arrive('.pill',.7,{y:75,scale:.86,opacity:0},1.0);q('.pill').forEach((p,i)=>{if(i!==3&&i!==7)tl.to(p,{opacity:.24,duration:.8,ease:'power2.out'},3.25)});tl.to(q('.pill')[3],{x:-25,scale:1.07,duration:1.0,ease:'power3.inOut'},3.25);tl.to(q('.pill')[7],{x:-25,scale:1.07,duration:1.0,ease:'power3.inOut'},3.65);stroke('svg>.draw',4.8,1.0);arrive('.voice-result',5.6,{y:70,scale:.92,opacity:0},1.15);`,
  `.headline{font-size:96px}.voice-result{box-shadow:10px 12px 0 #1a1a1a0d}`);

scene('note',7,'一张首图，正文写透',
  head('一张首图，','正文写透。')+
  box('phone hero','left:260px;top:660px;width:560px;height:930px;background:white;border:4px solid #1a1a1a;border-radius:62px;padding:32px;box-shadow:16px 18px 0 #1a1a1a10',
    box('phone-top','height:28px;display:flex;gap:7px;align-items:center;padding:0 4px',`<div style="width:12px;height:12px;border-radius:50%;background:#E85D4E"></div><div style="width:120px;height:8px;border-radius:9px;background:#1a1a1a25"></div>`)+
    box('cover','position:relative;margin-top:25px;width:488px;height:488px;border:3px solid #1a1a1a;border-radius:28px;background:#C4D94E;overflow:hidden',
      `<div style="position:absolute;left:35px;top:35px;font-size:62px;font-weight:850;line-height:1.35">周末</div><div style="position:absolute;left:35px;top:125px;font-size:54px;font-weight:850">留一半空白</div>`+
      svg(`<circle class="sun" cx="340" cy="315" r="66" fill="${C.coral}" stroke="${C.ink}" stroke-width="4"/>${line('M25 420C135 285 210 410 270 365S410 365 470 290',C.ink,4)}${line('M-15 465C105 365 180 480 270 425S410 415 510 350',C.ink,4)}`,'left:0;top:0;width:488px;height:488px','0 0 488 488'))+
    box('body-copy','position:absolute;left:38px;top:615px;width:480px',`<div style="font-size:29px;font-weight:750;margin-bottom:23px">把时间留给真正想做的事</div>${[95,82,96,73,90].map(w=>`<div class="body-line" style="height:10px;margin-bottom:22px;border-radius:10px;background:#1a1a1a35;width:${w}%;transform-origin:left"></div>`).join('')}`)),
  `arrive('.phone',.4,{scale:.8,y:120,rotation:-7,opacity:0},1.5);arrive('.cover',1.9,{scale:.8,y:30,opacity:0},1.1);tl.fromTo(q('.sun'),{y:55,opacity:0},{y:0,opacity:1,duration:1.2,ease:'power3.out'},2.5);stroke('.cover .draw',2.8,1.4);arrive('.body-copy>div:first-child',4.0,{y:30,opacity:0});tl.fromTo(q('.body-line'),{scaleX:0},{scaleX:1,duration:.8,stagger:.22,ease:'power3.out'},4.4);`,
  `.phone .body-line{opacity:.8}`);

scene('review',8,'你拍板，它去排队',
  head('你拍板，','它去排队。')+
  note('保留好观点','left:110px;top:680px;width:390px;height:420px;background:#FFFFFF','note approved')+
  note('删掉空话','left:580px;top:680px;width:390px;height:420px;background:#FFFFFF','note filtered')+
  box('stamp','position:absolute;left:360px;top:990px;width:160px;height:160px;border-radius:50%;background:#A8E6CF;border:4px solid #1a1a1a',svg(line('M36 82L66 112L124 49',C.ink,10),'inset:0;width:160px;height:160px','0 0 160 160'))+
  svg(line('M305 0V160Q305 230 400 230H830',C.ink,5),'left:0;top:1115px;width:1080px;height:260px','0 0 1080 260')+
  label('批准后，进入发布队列',120,1435,36)+
  [0,1,2].map(i=>pill(i===0?'待发布':'排队中',115+i*300,1260,255,i===0?C.lime:C.white,'height:100px;font-size:34px')).join(''),
  `arrive('.note',.6,{y:100,rotation:4,opacity:0},1.2);arrive('.stamp',2.25,{scale:1.5,y:-60,opacity:0},.85);stroke('.stamp .draw',2.6,.6);tl.to(q('.filtered'),{opacity:.22,x:60,rotation:5,duration:1.2,ease:'power3.inOut'},3.3);stroke('svg>.draw',3.8,1.25);arrive('.pill',5.0,{x:95,y:0,opacity:0},.9);arrive('.label',6.3,{y:45,opacity:0});`,
  `.note-title{font-size:33px}.note{padding:35px}.note-bar{height:12px;margin-bottom:29px}`);

const sampleCards=Array.from({length:20},(_,i)=>{
  const x=85+(i%5)*190, y=660+Math.floor(i/5)*205;
  return box('sample',`position:absolute;left:${x}px;top:${y}px;width:100px;height:140px;border:2px solid #1a1a1a;border-radius:15px;padding:18px;background:${[C.white,C.lime,C.mint,C.white,C.sky][i%5]}`,`<div style="width:16px;height:16px;border-radius:50%;background:#E85D4E;margin-bottom:19px"></div><div style="height:6px;background:#1a1a1a35;margin-bottom:12px"></div><div style="height:6px;background:#1a1a1a35;width:75%"></div>`);
}).join('');
scene('memory',7,'积累成自己的写法',
  head('每次反馈，','不白费。')+sampleCards+
  box('book hero','left:290px;top:860px;width:500px;height:560px;background:#C5B5E0;border:4px solid #1a1a1a;border-radius:20px 46px 46px 20px;box-shadow:18px 19px 0 #1a1a1a10;overflow:hidden',
    `<div style="position:absolute;left:45px;top:0;height:100%;width:4px;background:#1a1a1a"></div><div style="position:absolute;left:93px;top:78px;font-size:73px;font-weight:850;line-height:1.25">写法<div>记忆</div></div>`+
    ['观点','攻略','共情','观察'].map((s,i)=>pill(s,85+(i%2)*190,330+Math.floor(i/2)*94,165,[C.white,C.lime,C.mint,C.sky][i],'height:70px;font-size:30px;box-shadow:none')).join(''))+
  pill('20 篇真实样本',110,1510,410,C.white,'height:83px;font-size:32px')+pill('4 套写法结构',555,1510,410,C.white,'height:83px;font-size:32px'),
  `arrive('.sample',.4,{y:80,scale:.6,opacity:0},.8);q('.sample').forEach((p,i)=>{const x=85+(i%5)*190,y=660+Math.floor(i/5)*205;tl.to(p,{x:490-x,y:1060-y,scale:.6,rotation:(i%2?18:-18),opacity:0,duration:1.4,ease:'power3.inOut'},1.5+i*.06)});arrive('.book',2.1,{scale:.65,y:80,rotation:-7,opacity:0},1.4);arrive('.book .pill',3.9,{x:100,y:0,opacity:0},.9);arrive('.stage>.pill',5.2,{y:50,opacity:0},.9);`,
  `.headline .accent{color:#1a1a1a}.book .pill{box-shadow:none}`, '#EFEBF4');

scene('invite',6,'想看搭建过程，留言工作室',
  head('内容你来定，','重复交给它。')+
  box('brand hero','left:180px;top:725px;width:720px;height:340px;border:4px solid #1a1a1a;border-radius:54px;background:#F5F5F0;display:flex;align-items:center;gap:36px;padding:55px;box-shadow:12px 15px 0 #1a1a1a15',
    svg(`<rect x="3" y="3" width="140" height="170" rx="24" fill="#C4D94E" stroke="#1a1a1a" stroke-width="5"/>${line('M34 53H110M34 88H92M34 122H103',C.ink,8)}`,'position:relative;width:150px;height:185px;flex:none','0 0 150 185')+
    `<div><div style="font-size:44px;font-weight:850;line-height:1.3;letter-spacing:-1px">XHS GROWTH<div>AGENT</div></div><div style="font-size:27px;margin-top:22px">一个人的内容工作室</div></div>`)+
  label('想看搭建过程？',270,1210,42)+
  pill('留言「工作室」 ↗',155,1320,770,C.ink,'height:136px;font-size:56px;color:#F5F5F0;box-shadow:none'),
  `arrive('.brand',.45,{y:95,scale:.85,rotation:-4,opacity:0},1.3);stroke('.brand .draw',1.25,.9);arrive('.label',2.3,{y:45,opacity:0},.8);arrive('.pill',2.9,{y:55,scale:.86,opacity:0},1.05);`,
  `.headline .accent{color:#1a1a1a}.headline{font-size:96px}.label{font-weight:650}`,C.coral);

fs.writeFileSync('scenes.json',JSON.stringify(frames,null,2));
const subtitles=[
 [0,3.1,'一个人做内容，最累的是来回切换。'],
 [3.1,7,'选题、写作、配图、发布，都得自己盯。'],
 [7,10.5,'这个系统，把这些步骤放进同一个工作室。'],
 [10.5,14,'先说你想写什么，生活、职场、消费都可以。'],
 [14,17.5,'没想法时，就从近期热点里找切口。'],
 [17.5,21,'按方向筛选，把合适的话题留下。'],
 [21,25,'再选表达语气：主观、客观、幽默，或者共情。'],
 [25,29,'语气可以组合，写法也有结构和示例可参考。'],
 [29,32.5,'一篇笔记，只做一张首图。'],
 [32.5,36,'把真正有用的内容，完整放进正文。'],
 [36,40,'生成之后先到审核中心，由你修改、筛选。'],
 [40,44,'满意再批准，当前版本直接进入发布队列。'],
 [44,47.5,'真实高赞样本，会沉淀成可复用的写法。'],
 [47.5,51,'采用和过滤也留下记录，积累后调整下一次推荐。'],
 [51,54,'方向和判断留给你，重复的步骤交给系统。'],
 [54,57,'想看怎么搭起来？留言“工作室”。']
];
function stamp(t){let m=Math.round(t*1000);const h=Math.floor(m/3600000);m%=3600000;const n=Math.floor(m/60000);m%=60000;return `${String(h).padStart(2,'0')}:${String(n).padStart(2,'0')}:${String(Math.floor(m/1000)).padStart(2,'0')},${String(m%1000).padStart(3,'0')}`}
fs.writeFileSync('renders/xhs-growth-intro.zh-CN.srt',subtitles.map(([a,b,s],i)=>`${i+1}\n${stamp(a)} --> ${stamp(b)}\n${s}\n`).join('\n'));
let at=0;
fs.writeFileSync('STORYBOARD.md',`---\nformat: 1080x1920\nduration: 57s\nmessage: 一个人，也能拥有自己的内容工作室\narc: 价值承诺 → 给方向 → 选题 → 语气 → 单图正文 → 审核发布 → 记忆反馈 → CTA\naudience: 想稳定做内容的个人创作者\nmode: autonomous\nmusic: none\ncaptions: disabled\n---\n\n## Video direction\n原创平面产品动效，奶油白、墨黑、珊瑚红与少量薄荷/薰衣草色。所有可见字为设计标题或UI词，独立SRT不挂载进视频。每场有3至4次有意义的状态变化，power3长尾减速，无默认弹跳。\n\n`+frames.map((f,i)=>{
 const start=at;at+=f.duration;
 return `## Frame ${i+1} — ${f.title}\n\n- status: animated\n- src: ${f.file}\n- duration: ${f.duration}s\n- transition_in: ${i?'crossfade':'cut'}\n- scene: ${f.title}\n- poster: ${Math.min(f.duration-1,4.8)}s\n- asset_candidates: fonts/NotoSC.woff2\n- blueprint: compose\n- focal: ${f.title}\n- roles: 标题指明价值，核心图形证明产品机制\n- voiceover: （无语音，完整解说在独立SRT中）\n\nScene 1 (0.0–1.5s): 标题以shared-axis-y显现，核心图形开始进入。\nScene 2 (1.5–3.5s): svg-path-draw呈现机制，主对象以power3曲线完成状态变化。\nScene 3 (3.5–${f.duration-1}s): 下一批有意义的信息和对象沿原来的动线接续显现。\nScene 4 (${f.duration-1}–${f.duration}s): 重点停留，交由根时间线处理转场。全片时间${start}–${at}s。\n\n`;
}).join(''));
console.log(`Built ${frames.length} scenes, ${at}s, SRT detached.`);
