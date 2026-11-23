from pathlib import Path
import hashlib, json, math, subprocess, time, wave
import numpy as np

P=Path(__file__).resolve().parents[1]
plan=json.loads((P/'voice-plan.json').read_text())
SR=48000; SPF=1600

def read(path):
    with wave.open(str(path)) as w:
        assert w.getnchannels()==1 and w.getsampwidth()==2
        return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').copy(),w.getframerate()

def save(path,x):
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,SR,0,'NONE','not compressed'))
        w.writeframes(np.rint(np.clip(x,-1,.999969)*32768).astype('<i2').tobytes())

done=set()
while len(done)<len(plan):
    for c in plan:
        cid=c['id'];src=P/'audio/raw'/(cid+'.wav');out=P/'audio/final'/(cid+'.wav')
        if cid in done:continue
        if out.exists() and out.with_suffix('.json').exists():done.add(cid);continue
        if not src.exists() or not src.with_suffix('.metadata.json').exists():continue
        pcm,sr=read(src);x=pcm.astype(np.float32)/32768
        hop=round(sr*.005);nr=len(x)//hop
        rms=np.sqrt(np.mean(x[:nr*hop].reshape(nr,hop)**2,axis=1))
        hit=np.where(rms>max(10**(-60/20),rms.max()*10**(-50/20)))[0]
        if not len(hit):raise ValueError('No speech: '+cid)
        a=max(0,int(hit[0]*hop-sr*.025));b=min(len(x),int((hit[-1]+1)*hop+sr*.04))
        raw=subprocess.check_output(['ffmpeg','-v','error','-f','s16le','-ar',str(sr),'-ac','1','-i','pipe:0','-af',f'aresample={SR}','-f','f32le','pipe:1'],input=pcm[a:b].tobytes())
        y=np.frombuffer(raw,dtype='<f4');frames=math.ceil(len(y)/SPF);z=np.pad(y,(0,frames*SPF-len(y)))
        save(out,z)
        info=dict(id=cid,source_text=c['source_text'],raw_seconds=len(pcm)/sr,trim_start=a/sr,trim_end=b/sr,voice_seconds=len(y)/SR,frames=frames,measured_seconds=frames/30,padding_seconds=(frames*SPF-len(y))/SR,post_speed_change=False,sha256=hashlib.sha256(out.read_bytes()).hexdigest())
        out.with_suffix('.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
        done.add(cid)
    (P/'qa/audio-processing-status.json').write_text(json.dumps(dict(completed=len(done),total=len(plan))))
    if len(done)<len(plan):time.sleep(5)

clips=[];cursor=0;cues=[]
for i,c in enumerate(plan):
    path=P/'audio/final'/(c['id']+'.wav');pcm,sr=read(path);assert sr==SR
    if i:clips.append(np.zeros(4800,np.float32));cursor+=3
    frames=len(pcm)//SPF
    cues.append(dict(**c,start_frame=cursor,end_frame_exclusive=cursor+frames,duration_frames=frames,audio='audio/final/'+c['id']+'.wav',display_text=c['source_text'].translate(str.maketrans({'，':' ', ',':' ', '。':'', '.':''}))))
    clips.append(pcm.astype(np.float32)/32768);cursor+=frames
joined=np.concatenate(clips);save(P/'audio/narration-premix.wav',joined)
log=subprocess.run(['ffmpeg','-v','info','-i',str(P/'audio/narration-premix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
loud=json.loads(log[log.rfind('{'):log.rfind('}')+1]);gain=min(-16-float(loud['input_i']),-1.5-float(loud['input_tp']))
save(P/'audio/narration.wav',joined*10**(gain/20))
timeline=dict(name='山姆第三集 白光之后',fps=30,width=1920,height=1080,frame_count=cursor,duration_seconds=cursor/30,gap_frames=3,dissolve_frames=3,audio_sample_rate=SR,audio_samples=len(joined),cues=cues,shots=[],voice_id='Chinese (Mandarin)_Gentleman',api_speed=1.2,emotion='calm',post_speed_change=False,subtitles_burned=True,independent_subtitle_files=False,loudness_measurement=loud,global_gain_db=gain)
(P/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2))
print(json.dumps(dict(status='COMPLETE',duration_seconds=cursor/30,cues=len(cues)),ensure_ascii=False),flush=True)
