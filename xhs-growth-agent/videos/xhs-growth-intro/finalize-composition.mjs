import fs from 'node:fs';
const font=fs.readFileSync('assets/fonts/NotoSC.woff2').toString('base64');
for(const f of fs.readdirSync('compositions/frames')){
 const p='compositions/frames/'+f;
 let html=fs.readFileSync(p,'utf8').replaceAll("url('assets/fonts/NotoSC.woff2')",`url('data:font/woff2;base64,${font}')`);
 fs.writeFileSync(p,html);
}
let html=fs.readFileSync('index.html','utf8');
html=html.replace(/<script src="https:\/\/cdn[^<]+<\/script>/, '<script src="assets/gsap.min.js"></script>');
html=html.replace('<html lang="en">','<html lang="zh-CN">');
html=html.replace('data-composition-id="main"','data-composition-id="main" data-fps="60"');
html=html.replace(/(#root\s*\{[\s\S]*?)width: 1080px;\s*height: 1920px;/,'$1width: 100%; height: 100%;');
html=html.replaceAll('class="scene"','class="clip scene"');
const overlay=`
<canvas id="flow-rail" width="28" height="930" aria-hidden="true" data-layout-allow-overlap style="position:absolute;left:24px;top:640px;width:28px;height:930px;z-index:80;pointer-events:none"></canvas>
<div aria-hidden="true" style="position:absolute;left:80px;top:80px;z-index:81;font:550 24px 'Noto Sans SC';letter-spacing:2px;display:flex;align-items:center;gap:18px"><span style="width:17px;height:17px;border:2px solid #1a1a1a;background:#E85D4E;border-radius:50%;display:inline-block"></span>XHS GROWTH AGENT</div>`;
html=html.replace('\n    </div>\n\n    <script>',`${overlay}\n    </div>\n\n    <script>`);
html=html.replace('</head>',`<style>@font-face{font-family:'Noto Sans SC';font-weight:100 900;src:url('data:font/woff2;base64,${font}') format('woff2')}</style></head>`);
const rail=`
<script>(()=>{
 const canvas=document.getElementById('flow-rail'),ctx=canvas.getContext('2d');
 const state={time:0};
 function draw(){const t=state.time;ctx.clearRect(0,0,28,930);ctx.strokeStyle='#1a1a1a18';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(14,10);ctx.lineTo(14,920);ctx.stroke();const y=10+910*(t/57);ctx.strokeStyle='#1a1a1a60';ctx.beginPath();ctx.moveTo(14,10);ctx.lineTo(14,y);ctx.stroke();ctx.fillStyle='#1a1a1a';ctx.beginPath();ctx.arc(14,y,6,0,Math.PI*2);ctx.fill();}
 const main=window.__timelines.main;
 main.to(state,{time:57,duration:57,ease:'none',onUpdate:draw},0);draw();
})();</script>`;
html=html.replace('</body>',rail+'</body>');
fs.writeFileSync('index.html',html);
console.log('Offline GSAP + embedded CJK font + deterministic Canvas2D rail added; no audio/captions.');
