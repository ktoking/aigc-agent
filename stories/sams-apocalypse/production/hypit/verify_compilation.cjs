/* Verify the actual local MP4 and detached VTT using system Chrome. */
const fs=require('node:fs');
const path=require('node:path');
const puppeteer=require('/opt/homebrew/lib/node_modules/@hypit/hypit/node_modules/puppeteer-core');
const ROOT=path.resolve(__dirname,'../..');
const OUT=path.join(ROOT,'output/EP001-EP008');
const QA=path.join(OUT,'qa');
(async()=>{
 const browser=await puppeteer.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--no-sandbox','--autoplay-policy=no-user-gesture-required','--allow-file-access-from-files']});
 try {
  const page=await browser.newPage();await page.setViewport({width:1440,height:1080,deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto('file://'+path.join(OUT,'player.html'),{waitUntil:'load'});
  await page.waitForFunction(()=>{const v=document.querySelector('video');return v.readyState>=2&&v.duration===480&&v.textTracks.length===1&&v.textTracks[0].cues?.length===130},{timeout:30000});
  const checks=[];
  for(let ep=1;ep<=8;ep++){
   const target=(ep-1)*60+10;
   await page.evaluate(async t=>{const v=document.querySelector('video');v.textTracks[0].mode='showing';v.pause();await new Promise(resolve=>{v.addEventListener('seeked',resolve,{once:true});v.currentTime=t})},target);
   const state=await page.evaluate(()=>{const v=document.querySelector('video');return{time:v.currentTime,width:v.videoWidth,height:v.videoHeight,error:v.error?.message||null,cues:Array.from(v.textTracks[0].activeCues||[]).map(c=>c.text)}});
   if(state.error||state.width!==1920||state.height!==1080||!state.cues.length)throw new Error('bad chapter '+ep+JSON.stringify(state));
   checks.push({episode:ep,...state});
   await page.screenshot({path:path.join(QA,`browser-EP${String(ep).padStart(3,'0')}.png`)});
  }
  const started=Date.now();
  await page.evaluate(async()=>{const v=document.querySelector('video');v.currentTime=0;v.playbackRate=8;await v.play()});
  console.log('Started complete sequential browser playback at 8x');
  await page.waitForFunction(()=>document.querySelector('video').ended,{timeout:150000,polling:500});
  const ended=await page.evaluate(()=>{const v=document.querySelector('video');const q=v.getVideoPlaybackQuality();return{time:v.currentTime,duration:v.duration,ended:v.ended,paused:v.paused,error:v.error?.message||null,playbackRate:v.playbackRate,cueCount:v.textTracks[0].cues.length,decodedFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames}});
  if(!ended.ended||ended.error||ended.time!==480||errors.length)throw new Error(JSON.stringify({ended,errors}));
  await page.screenshot({path:path.join(QA,'browser-playback-end.png')});
  const report={chapter_checks:checks,sequential_playback:ended,playback_speed:8,elapsed_wall_seconds:(Date.now()-started)/1000,page_errors:errors};
  fs.writeFileSync(path.join(QA,'browser-playback.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
 } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
