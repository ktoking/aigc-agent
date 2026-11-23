const fs=require('node:fs'),path=require('node:path');
const puppeteer=require('/opt/homebrew/lib/node_modules/@hypit/hypit/node_modules/puppeteer-core');
const root=path.resolve(__dirname,'../../..');const out=path.join(root,'output/EP001-EP008-v4');
(async()=>{
const browser=await puppeteer.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--autoplay-policy=no-user-gesture-required']});
try{
 const page=await browser.newPage();await page.setViewport({width:1280,height:950});const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('http://127.0.0.1:5195/',{waitUntil:'load'});
 await page.waitForFunction(()=>document.querySelector('video').readyState>=2);
 await page.click('#play');await new Promise(r=>setTimeout(r,18000));
 const normal=await page.evaluate(()=>{let v=document.querySelector('video');return {time:v.currentTime,rate:v.playbackRate,error:v.error?.message||null,paused:v.paused,width:v.videoWidth,height:v.videoHeight,duration:v.duration}});
 if(normal.time<15||normal.rate!==1||normal.error)throw Error('Normal playback failed '+JSON.stringify(normal));
 await page.screenshot({path:path.join(out,'qa/browser-normal-1x.png')});
 console.log('Normal 1x first18s verified '+JSON.stringify(normal),flush=true);
 const chapters=JSON.parse(fs.readFileSync(path.join(out,'chapters.json')));const checks=[];
 for(const c of chapters){
  await page.evaluate(async t=>{const v=document.querySelector('video');v.pause();await new Promise(r=>{v.addEventListener('seeked',r,{once:true});v.currentTime=t;});},c.start_seconds+.3);
  checks.push(await page.evaluate(()=>{let v=document.querySelector('video');return {time:v.currentTime,error:v.error?.message||null}}));
 }
 await page.evaluate(async()=>{let v=document.querySelector('video');v.currentTime=0;v.playbackRate=8;await v.play()});
 await page.waitForFunction(()=>document.querySelector('video').ended,{timeout:65000,polling:300});
 const ended=await page.evaluate(()=>{let v=document.querySelector('video');return {time:v.currentTime,duration:v.duration,ended:v.ended,error:v.error?.message||null,rate:v.playbackRate}});
 if(!ended.ended||ended.error||errors.length)throw Error(JSON.stringify({ended,errors}));
 await page.screenshot({path:path.join(out,'qa/browser-ended.png')});
 const report={normal_1x_sample:normal,chapter_checks:checks,full_sequential_8x:ended,page_errors:errors,note:'Browser codec/seek/playback proof; speech boundaries independently checked against VAD and retained PCM, not a claim of complete human listening.'};
 fs.writeFileSync(path.join(out,'qa/browser-playback.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
}finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
