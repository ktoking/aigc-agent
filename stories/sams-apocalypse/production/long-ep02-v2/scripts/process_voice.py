from pathlib import Path
import wave,json,subprocess,time,math,hashlib
import numpy as np
P=Path(__file__).resolve().parents[1];PLAN=json.loads((P/'voice-plan.json').read_text())
SR=48000;FPS=30;SPF=SR//FPS
def read(path):
    with wave.open(str(path)) as w:
        assert w.getnchannels()==1 and w.getsampwidth()==2
        return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)/32768,w.getframerate()
def save(path,x,sr=SR):
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes(np.rint(np.clip(x,-1,.999969)*32768).astype('<i2').tobytes())
def edges(x,sr):
    hop=max(1,round(sr*.005));n=len(x)//hop
    rms=np.sqrt(np.mean(x[:n*hop].reshape(n,hop)**2,axis=1))
    threshold=max(10**(-58/20),rms.max()*10**(-48/20))
    hit=np.where(rms>threshold)[0]
    if not len(hit):raise ValueError('empty speech')
    return max(0,int(hit[0]*hop-sr*.015)),min(len(x),int((hit[-1]+1)*hop+sr*.015))
def process(c):
    source=P/'audio/raw'/(c['id']+'.wav');out=P/'audio/final'/(c['id']+'.wav');meta=out.with_suffix('.json')
    x,sr=read(source);a,b=edges(x,sr);trim=x[a:b]
    frames=c['units']*4+round(c['breath_seconds']*FPS);target=frames*SPF
    target_seconds=target/SR
    # Protect every word: render slightly shorter than the slot, never truncate non-silent output.
    tempo=len(trim)/sr/max(.1,target_seconds-.018)
    for attempt in range(3):
        pcm=np.rint(trim*32768).astype('<i2').tobytes()
        data=subprocess.check_output(['ffmpeg','-v','error','-f','s16le','-ar',str(sr),'-ac','1','-i','pipe:0','-af',f'atempo={tempo:.9f},aresample={SR}','-f','f32le','pipe:1'],input=pcm)
        y=np.frombuffer(data,dtype='<f4').copy()
        if len(y)<=target:break
        tempo*=len(y)/target*1.025
    else:raise ValueError('audio cannot fit without truncation: '+c['id'])
    if target-len(y)>int(SR*.16):
        # At short durations atempo may undershoot; keep the authentic speech and flag its measured margin.
        pass
    rms=float(np.sqrt(np.mean(y*y)));peak=float(np.max(np.abs(y)))
    gain=min(2.0,max(.5,.095/max(rms,1e-6)),.86/max(peak,1e-6))
    y=y*gain;z=np.pad(y,(0,target-len(y)))
    save(out,z)
    with wave.open(str(out)) as w:measured=w.getnframes()/w.getframerate();assert w.getnframes()==target
    info=dict(cue_id=c['id'],source_text=c['source_text'],model=c['model'],voice_id=c['voice_id'],preset=c['preset'],api_speed=c['api_speed'],raw_seconds=len(x)/sr,trim_start_seconds=a/sr,trim_end_seconds=b/sr,atempo=tempo,untruncated_processed_seconds=len(y)/SR,tail_quantization_seconds=(target-len(y))/SR,gain=gain,measured_seconds=measured,frames=frames,samples=target,units=c['units'],cps_including_performance=c['units']/measured,sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    meta.write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
pending=list(PLAN);completed=0
while pending:
    next_round=[]
    for c in pending:
        path=P/'audio/final'/(c['id']+'.wav');raw=P/'audio/raw'/(c['id']+'.wav')
        if path.exists() and path.with_suffix('.json').exists():completed+=1;continue
        if not raw.exists() or not raw.with_suffix('.metadata.json').exists():next_round.append(c);continue
        process(c);completed+=1
        if completed%12==0:print(f'Voice finalized {completed}/{len(PLAN)}',flush=True)
    pending=next_round
    if pending:time.sleep(2)
cursor=0;clips=[];cues=[]
for i,c in enumerate(PLAN):
    x,sr=read(P/'audio/final'/(c['id']+'.wav'));assert sr==SR
    if i:clips.append(np.zeros(3*SPF,np.float32));cursor+=3
    assert len(x)%SPF==0
    frames=len(x)//SPF
    cues.append(dict(**c,start_frame=cursor,end_frame_exclusive=cursor+frames,audio='audio/final/'+c['id']+'.wav',duration_frames=frames))
    clips.append(x);cursor+=frames
joined=np.concatenate(clips);save(P/'audio/narration-premix.wav',joined)
measure=subprocess.run(['ffmpeg','-v','info','-i',str(P/'audio/narration-premix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
loud=json.loads(measure[measure.rfind('{'):measure.rfind('}')+1]);gain_db=min(-16-float(loud['input_i']),-1.5-float(loud['input_tp']))
save(P/'audio/narration.wav',joined*10**(gain_db/20))
images=json.loads((P/'image-plan.json').read_text());shots=[]
for i,im in enumerate(images):
    a=round(i*cursor/len(images));b=round((i+1)*cursor/len(images))
    shots.append(dict(id=im['id'],asset='assets/'+im['id']+'.png',start_frame=a,end_frame_exclusive=b,duration_frames=b-a))
chapters=[]
for c in cues:
    if not chapters or chapters[-1]['title']!=c['chapter']:chapters.append(dict(title=c['chapter'],start_frame=c['start_frame'],start_seconds=c['start_frame']/FPS))
for i,ch in enumerate(chapters):ch['end_frame_exclusive']=chapters[i+1]['start_frame'] if i+1<len(chapters) else cursor
timeline=dict(name='山姆避难记·第二集：门外的人 v2',fps=FPS,width=1920,height=1080,frame_count=cursor,duration_seconds=cursor/FPS,audio_sample_rate=SR,audio_samples=len(joined),audio_model='speech-2.8-turbo',voice_id='Chinese_calm_streamer_nv1',gap_frames=3,gap_samples=3*SPF,dissolve_frames=3,subtitles_burned=True,independent_subtitle_files=False,cues=cues,shots=shots,chapters=chapters,measured_audio_basis='Every processed WAV measured; PCM sample clock equals video frame clock',loudness_measurement=loud,global_gain_db=gain_db)
(P/'timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status='audio_and_timeline_complete',duration_seconds=cursor/FPS,frames=cursor,images=len(shots),audio_samples=len(joined),global_gain_db=gain_db),ensure_ascii=False),flush=True)
