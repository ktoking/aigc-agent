// 所有状态均由绝对时间计算：无动画循环、帧间积分或随机时钟。
document.fonts.ready.then(()=>{
  const NS='http://www.w3.org/2000/svg';
  const stage=document.getElementById('journey-stage');
  const svg=document.getElementById('journey-svg');
  const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
  const mix=(a,b,p)=>a+(b-a)*p;
  const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
  const phase=(t,a,b)=>smooth((t-a)/Math.max(.001,b-a));
  const rgba=(r,g,b,a)=>`rgba(${r},${g},${b},${a})`;
  const el=(tag,attrs,parent)=>{const n=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));parent?.append(n);return n};
  const runtimes=[];
  for(const s of JOURNEY.scenes){
    const wrap=el('g',{id:s.id,opacity:0},stage);
    const world=el('g',{id:s.id+'-world'},wrap);
    const glowLayer=el('g',{},world),edgeLayer=el('g',{},world),packetLayer=el('g',{},world),nodeLayer=el('g',{},world),labelLayer=el('g',{},world),fxLayer=el('g',{},world);
    const edges=new Map(),nodes=new Map();
    for(const e of s.edges){
      const base=el('path',{id:e.id,class:'edge-base',d:e.d,stroke:'#d1b978','stroke-width':e.chosen?3.2:1.9},edgeLayer);
      const len=base.getTotalLength();base.setAttribute('stroke-dasharray',len);base.setAttribute('stroke-dashoffset',len);
      const glow=e.chosen?el('path',{class:'edge-glow',d:e.d,stroke:'#edc274','stroke-width':13,filter:'url(#bloom)',opacity:.33,'stroke-dasharray':len,'stroke-dashoffset':len},glowLayer):null;
      const packet=el('circle',{r:e.chosen?3:2.3,fill:'#fff2c4',opacity:0},packetLayer);
      // 点位提前烘焙，渲染时无需测量布局；回退使用同一曲线的反向采样。
      const samples=[];for(let k=0;k<=160;k++){const p=base.getPointAtLength(len*k/160);samples.push({x:p.x,y:p.y})}
      edges.set(e.id,{...e,base,glow,packet,len,samples,progress:0});
    }
    for(const n of s.nodes){
      const circle=el('circle',{cx:n.x,cy:n.y,r:n.key?4.6:2.6,fill:'#d6bd82',opacity:0},nodeLayer);
      const label=n.label?el('text',{class:'node-label',x:n.x,y:n.y-29,'font-size':36,'text-anchor':'middle',opacity:0},labelLayer):null;
      if(label)label.textContent=n.label;
      nodes.set(n.id,{...n,circle,label,incoming:s.edges.filter(e=>e.b===n.id).map(e=>e.id)});
    }
    const rings=Array.from({length:12},()=>el('circle',{fill:'none',stroke:'#edcd86','stroke-width':1,opacity:0},fxLayer));
    const sparks=Array.from({length:32},()=>el('line',{stroke:'#f18b7d','stroke-width':1.5,opacity:0},fxLayer));
    const tail=Array.from({length:13},(_,i)=>el('circle',{class:'trail-dot',r:mix(7,1,i/12),opacity:0},fxLayer));
    const halo=el('circle',{r:15,fill:'#f4ce78',filter:'url(#dot-glow)',opacity:.65},fxLayer);
    const head=el('circle',{id:s.id+'-hero',r:5.1,fill:'#fff9e4'},fxLayer);
    runtimes.push({s,wrap,world,edges,nodes,rings,sparks,tail,halo,head});
  }

  function onPath(e,p){
    const x=clamp(p)*160,i=Math.min(159,Math.floor(x)),a=e.samples[i],b=e.samples[i+1],f=x-i;
    return{x:mix(a.x,b.x,f),y:mix(a.y,b.y,f)};
  }
  function position(rt,t){
    const routes=rt.s.route;
    if(!routes.length){return {...rt.s.nodes[0],direction:'hold',route:null,p:0}}
    let r=routes[0];
    if(t<r.start){const q=onPath(rt.edges.get(r.edge),r.a);return{...q,direction:'hold',route:r,p:r.a}}
    for(const candidate of routes){if(t>=candidate.start)r=candidate;else break}
    const progress=phase(t,r.start,r.end),p=mix(r.a,r.b,progress),q=onPath(rt.edges.get(r.edge),p);
    return {...q,route:r,p,direction:t>=r.end?'hold':r.b<r.a?'backtrack':'advance'};
  }
  function camera(rt,t){
    const s=rt.s,lag=position(rt,t-.24),u=clamp((t-s.start)/(s.end-s.start));
    let follow=.9,z=s.zoom,rotation=0;
    if(s.id==='journey-1'){follow=mix(.3,.67,smooth(u));z=mix(1.06,.89,phase(u,.6,1));rotation=mix(0,-3,phase(u,.55,1))}
    if(s.id==='journey-2'){follow=.91;z=1.03+.10*Math.sin(u*Math.PI);rotation=3*Math.sin(u*Math.PI*1.5)}
    if(s.id==='journey-3'){follow=.92;z=1.03;rotation=-3+6*u}
    if(s.id==='journey-4'){follow=mix(.35,.78,phase(u,.35,1));z=mix(.91,1.06,u);rotation=0}
    if(s.id==='journey-5'){follow=t<JOURNEY.beats[80].time?.05:.86;z=t<JOURNEY.beats[80].time?1:1.1;rotation=-3*phase(u,.4,.8)}
    if(s.id==='journey-6'){
      const pull=phase(t,JOURNEY.beats[99].time,58.5);follow=mix(.91,.02,pull);z=mix(1.12,.58,pull);rotation=mix(-3,0,pull);
    }
    const cx=mix(s.center[0],lag.x,follow),cy=mix(s.center[1],lag.y,follow);
    return {x:cx,y:cy,z,rotation};
  }
  function project(p,cam){const a=cam.rotation*Math.PI/180,x=(p.x-cam.x)*cam.z,y=(p.y-cam.y)*cam.z;return{x:540+x*Math.cos(a)-y*Math.sin(a),y:1055+x*Math.sin(a)+y*Math.cos(a)}}
  function edgeProgress(e,t){
    let p=phase(t,e.start,e.end);
    if(e.retract&&t>=e.retract[0])p*=1-phase(t,e.retract[0],e.retract[1]);
    return p;
  }
  function renderScene(rt,t){
    const s=rt.s;
    const alpha=(s.start===0?1:clamp((t-(s.start-.15))/.30))*(s.end===60?1:clamp(((s.end+.15)-t)/.30));
    rt.wrap.setAttribute('opacity',alpha.toFixed(4));
    if(alpha===0)return;
    const cam=camera(rt,t),hero=position(rt,t);
    rt.world.setAttribute('transform',`translate(540 1055) rotate(${cam.rotation}) scale(${cam.z}) translate(${-cam.x} ${-cam.y})`);
    rt.world.setAttribute('data-camera-x',cam.x.toFixed(2));rt.world.setAttribute('data-camera-y',cam.y.toFixed(2));
    const pulses=[];const bursts=[];
    for(const e of rt.edges.values()){
      const p=edgeProgress(e,t);e.progress=p;
      const failed=e.fail!==undefined&&t>=e.fail;
      const selected=e.chosen;
      const focus=hero.route?.edge===e.id;
      const emergence=clamp(1-(t-e.end)/1.2);
      let opacity=p>0?(selected?.94:.55+.25*emergence):0;
      if(failed)opacity*=clamp(1-(t-e.fail)*.10,.18,1);
      if(s.id==='journey-4'&&t>JOURNEY.beats[67].time&&!selected)opacity*=.45;
      if(s.id==='journey-6'&&!selected)opacity=.72*(p>0?1:0);
      const color=failed?'#ed7969':focus?'#fff2c4':selected?'#edd09a':'#cabb96';
      e.base.setAttribute('stroke',color);e.base.setAttribute('stroke-dashoffset',(e.len*(1-p)).toFixed(3));e.base.setAttribute('opacity',opacity.toFixed(4));
      if(e.glow){e.glow.setAttribute('stroke',failed?'#e26353':'#e4b96a');e.glow.setAttribute('stroke-dashoffset',(e.len*(1-p)).toFixed(3));e.glow.setAttribute('opacity',p>0?(focus?.55:.22):0)}
      // 新生分支的流光，不依靠亮度呼吸伪装运动。
      const age=t-e.start,period=1.065,packetP=age>=0?(age%period)/period:0;
      const packet=onPath(e,Math.min(p,packetP));
      const packetOn=p>.03&&age>=0&&age<8&&!failed&&packetP<p;
      e.packet.setAttribute('cx',packet.x);e.packet.setAttribute('cy',packet.y);e.packet.setAttribute('opacity',packetOn?(selected?.85:.52):0);
      if(t>=e.end&&t-e.end<1.05&&p>.98){const n=rt.nodes.get(e.b);pulses.push({x:n.x,y:n.y,age:t-e.end,red:false})}
      if(e.fail!==undefined&&t>=e.fail&&t-e.fail<.8){const n=rt.nodes.get(e.b);bursts.push({x:n.x,y:n.y,age:t-e.fail});pulses.push({x:n.x,y:n.y,age:t-e.fail,red:true})}
    }
    for(const n of rt.nodes.values()){
      let incoming=n.incoming.map(id=>rt.edges.get(id));
      const root=n.id===s.nodes[0].id;
      const lit=root||incoming.some(e=>e.progress>.97);
      let op=lit?.95:incoming.some(e=>e.progress>.7)?.38:0;
      const failed=incoming.some(e=>e.fail!==undefined&&t>=e.fail&&e.progress>.2);
      n.circle.setAttribute('opacity',op);n.circle.setAttribute('fill',failed?'#ed7969':n.key?'#fff0c6':'#d4bd80');
      if(n.label){
        const pos=project(n,cam);const inside=pos.x>125&&pos.x<955&&pos.y>650&&pos.y<1475;
        const arrival=incoming.length?Math.min(...incoming.map(e=>e.end)):s.start;
        const fresh=t-arrival<5.5||s.id==='journey-1';
        const relevant=root||incoming.some(e=>e.chosen)||s.id==='journey-3';
        const lab=inside&&fresh&&relevant&&cam.z>.68?op:0;
        n.label.setAttribute('opacity',lab);n.label.setAttribute('font-size',35/cam.z);n.label.setAttribute('y',n.y-28/cam.z);n.label.setAttribute('fill',failed?'#f18b7d':'#eee2c0');
      }
    }
    for(let i=0;i<rt.tail.length;i++){
      const p=position(rt,t-i*.028),n=rt.tail[i];n.setAttribute('cx',p.x);n.setAttribute('cy',p.y);n.setAttribute('opacity',hero.direction==='hold'?.12*(1-i/14):.65*(1-i/14));
    }
    rt.halo.setAttribute('cx',hero.x);rt.halo.setAttribute('cy',hero.y);
    rt.head.setAttribute('cx',hero.x);rt.head.setAttribute('cy',hero.y);rt.head.setAttribute('data-direction',hero.direction);rt.head.setAttribute('data-edge',hero.route?.edge||'');rt.head.setAttribute('data-progress',hero.p.toFixed(4));
    for(let i=0;i<rt.rings.length;i++){
      const pulse=pulses[Math.floor(i/2)],n=rt.rings[i];
      if(!pulse){n.setAttribute('opacity',0);continue}
      const age=pulse.age+(i%2)*.13,r=6+age*68;
      n.setAttribute('cx',pulse.x);n.setAttribute('cy',pulse.y);n.setAttribute('r',r);n.setAttribute('opacity',clamp(1-age)*.65);n.setAttribute('stroke',pulse.red?'#ed7969':'#e9c984');
    }
    for(let i=0;i<rt.sparks.length;i++){
      const n=rt.sparks[i],burst=bursts[Math.floor(i/16)];
      if(!burst){n.setAttribute('opacity',0);continue}
      const a=i*2.3999632297,r=12+burst.age*(75+i%5*16),len=8*(1-burst.age),ca=Math.cos(a),sa=Math.sin(a);
      n.setAttribute('x1',burst.x+ca*r);n.setAttribute('y1',burst.y+sa*r);n.setAttribute('x2',burst.x+ca*(r+len));n.setAttribute('y2',burst.y+sa*(r+len));n.setAttribute('opacity',clamp(1-burst.age/.8));
    }
    if(t>=s.start&&t<s.end){
      svg.setAttribute('data-scene',s.id);svg.setAttribute('data-direction',hero.direction);svg.setAttribute('data-drawn-paths',[...rt.edges.values()].filter(e=>e.progress>.03).length);
      const name=document.getElementById('route-name');if(name.textContent!==s.name)name.textContent=s.name;
    }
  }
  function render(t){
    for(const rt of runtimes)renderScene(rt,t);
    let pulse=0;
    for(const s of JOURNEY.scenes){const dt=t-s.start;if(dt>=0&&dt<.4)pulse=Math.max(pulse,Math.sin(dt/.4*Math.PI)*.37)}
    document.getElementById('flash').style.opacity=pulse;
  }
  const time={value:0};
  const tl=gsap.timeline({paused:true});
  tl.fromTo(time,{value:0},{value:60,duration:60,ease:'none',onUpdate:()=>render(time.value)},0);
  JOURNEY.cues.forEach((c,i)=>{
    tl.fromTo('#caption-'+i,{opacity:0,y:12},{opacity:1,y:0,duration:.18,ease:'power2.out',immediateRender:false},c.start);
    if(i<JOURNEY.cues.length-1)tl.to('#caption-'+i,{opacity:0,y:-6,duration:.14,ease:'power1.in'},c.end-.14);
  });
  render(0);
  window.__timelines['fault-tolerance-v2']=tl;
});
