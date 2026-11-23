import fs from 'node:fs';
const scenes=JSON.parse(fs.readFileSync('scenes.json','utf8'));
const gsap=fs.readFileSync('assets/gsap.min.js','utf8');
const font=fs.readFileSync('assets/fonts/NotoSC.woff2').toString('base64');
let start=0;
const data=scenes.map(s=>{
 const fragment=fs.readFileSync(s.file,'utf8').trim().replace(/^<template>/,'').replace(/<\/template>$/,'');
 const html=`<!doctype html><html><head><meta charset="UTF-8"><style>html,body{margin:0;width:100%;height:100%;overflow:hidden}</style><script>${gsap}</script><script>window.__timelines={};</script></head><body>${fragment}</body></html>`;
 const item={...s,start,html};start+=s.duration;return item;
});
const payload=JSON.stringify(data).replaceAll('<','\\u003c');
const html=`<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>XHS Growth Agent · 57秒动效介绍</title><style>
@font-face{font-family:'Noto Sans SC';font-weight:100 900;src:url('data:font/woff2;base64,${font}') format('woff2')}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#222522;color:#f5f5f0;font-family:'Noto Sans SC',sans-serif}body{display:flex;flex-direction:column;align-items:center;padding:16px;gap:12px}.screen{position:relative;flex:1;min-height:0;aspect-ratio:9/16;max-width:100%;overflow:hidden;background:#f5f5f0;border-radius:12px}.stage{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0}.stage iframe{position:absolute;inset:0;width:1080px;height:1920px;border:0;display:none;pointer-events:none}.brand{position:absolute;left:80px;top:80px;z-index:100;font:550 24px 'Noto Sans SC';letter-spacing:2px;display:flex;align-items:center;gap:18px;color:#1a1a1a}.brand i{width:17px;height:17px;border:2px solid #1a1a1a;background:#e85d4e;border-radius:50%}canvas{position:absolute;left:24px;top:640px;width:28px;height:930px;z-index:99}nav{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:center;font-size:13px;max-width:900px}button{border:1px solid #f5f5f04a;background:transparent;color:inherit;border-radius:99px;padding:7px 14px;font:inherit;cursor:pointer}button:hover{background:#f5f5f018}input{width:min(70vw,500px);accent-color:#e85d4e}small{color:#bbb;font-size:11px}.time{font-variant-numeric:tabular-nums;min-width:96px}
</style></head><body><div class="screen"><div class="stage"><canvas width="28" height="930"></canvas><div class="brand"><i></i>XHS GROWTH AGENT</div></div></div><nav><button id="play">加载中…</button><input aria-label="播放进度" id="seek" type="range" min="0" max="57" step="0.01" value="0"><span class="time">00:00 / 00:57</span></nav><nav><button data-t="0">开场</button><button data-t="14.8">选题</button><button data-t="22">语气</button><button data-t="30">图文</button><button data-t="37">审核发布</button><button data-t="45">写法记忆</button><button data-t="54">结尾</button></nav><small>57秒 · HTML / SVG / Canvas 2D · 全静音 · 无烧录字幕</small><script>
const scenes=${payload};
const stage=document.querySelector('.stage'),screen=document.querySelector('.screen'),seek=document.getElementById('seek'),play=document.getElementById('play'),clock=document.querySelector('.time'),ctx=document.querySelector('canvas').getContext('2d');
let time=0,playing=false,base=0,since=0;
function fit(){stage.style.transform='scale('+Math.min(screen.clientWidth/1080,screen.clientHeight/1920)+')'}
new ResizeObserver(fit).observe(screen);fit();
const ready=scenes.map(s=>new Promise(resolve=>{const iframe=document.createElement('iframe');iframe.title=s.title;iframe.srcdoc=s.html;stage.appendChild(iframe);s.node=iframe;iframe.onload=async()=>{await iframe.contentDocument.fonts.ready;s.timeline=iframe.contentWindow.__timelines[s.id];resolve()}}));
function paint(t){time=Math.min(57,Math.max(0,t));for(const s of scenes){let local=time-s.start;const active=local>=0&&local<s.duration+(s.start+s.duration<57?.5:.01);s.node.style.display=active?'block':'none';if(active){s.node.style.zIndex=String(scenes.indexOf(s));s.node.style.opacity=s.start&&local<.5?local/.5:1;s.timeline?.pause().seek(Math.max(0,Math.min(local,s.duration+.5)))}}ctx.clearRect(0,0,28,930);ctx.strokeStyle='#1a1a1a18';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(14,10);ctx.lineTo(14,920);ctx.stroke();const y=10+910*time/57;ctx.strokeStyle='#1a1a1a60';ctx.beginPath();ctx.moveTo(14,10);ctx.lineTo(14,y);ctx.stroke();ctx.fillStyle='#1a1a1a';ctx.beginPath();ctx.arc(14,y,6,0,Math.PI*2);ctx.fill();seek.value=time;clock.textContent='00:'+String(Math.floor(time)).padStart(2,'0')+' / 00:57'}
function tick(now){if(playing){paint(base+(now-since)/1000);if(time>=57){playing=false;play.textContent='重播'}}requestAnimationFrame(tick)}
function go(){if(time>=57)paint(0);base=time;since=performance.now();playing=true;play.textContent='暂停'}
play.onclick=()=>{if(playing){playing=false;play.textContent='播放'}else go()};seek.oninput=()=>{playing=false;play.textContent='播放';paint(Number(seek.value))};document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{playing=false;play.textContent='播放';paint(Number(b.dataset.t))});
Promise.all(ready).then(()=>{paint(0);go();requestAnimationFrame(tick)});
</script></body></html>`;
fs.writeFileSync('renders/xhs-growth-intro.html',html);
console.log('Standalone offline HTML',Buffer.byteLength(html),'bytes');
