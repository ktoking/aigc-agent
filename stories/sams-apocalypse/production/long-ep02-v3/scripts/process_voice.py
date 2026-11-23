from pathlib import Path
import wave,json,subprocess,time,math,hashlib
import numpy as np
P=Path(__file__).resolve().parents[1];PLAN=json.loads((P/'voice-plan.json').read_text())
SR=48000;FPS=30;SPF=1600

def read(path):
    with wave.open(str(path)) as w:
        assert w.getnchannels()==1 and w.getsampwidth()==2
        return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').copy(),w.getframerate()
def save(path,x):
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,SR,0,'NONE','not compressed'))
        w.writeframes(np.rint(np.clip(x,-1,.999969)*32768).astype('<i2').tobytes())
def edges(pcm,sr):
    x=pcm.astype(np.float32)/32768;hop=max(1,round(sr*.005));n=len(x)//hop
    rms=np.sqrt(np.mean(x[:n*hop].reshape(n,hop)**2,axis=1));threshold=max(10**(-58/20),rms.max()*10**(-48/20))
    hit=np.where(rms>threshold)[0]
    if not len(hit):raise ValueError('Empty speech')
    return max(0,int(hit[0]*hop-sr*.015)),min(len(x),int((hit[-1]+1)*hop+sr*.015))
def process(c):
    src=P/'audio/raw'/(c['id']+'.wav');out=P/'audio/final'/(c['id']+'.wav');pcm,sr=read(src);a,b=edges(pcm,sr)
    # Natural duration is preserved: sample-rate conversion only, never atempo/asetrate.
    data=subprocess.check_output(['ffmpeg','-v','error','-f','s16le','-ar',str(sr),'-ac','1','-i','pipe:0','-af',f'aresample={SR}','-f','f32le','pipe:1'],input=pcm[a:b].tobytes())
    y=np.frombuffer(data,dtype='<f4').copy();frames=math.ceil(len(y)/SPF);target=frames*SPF
    rms=float(np.sqrt(np.mean(y*y)));peak=float(abs(y).max());gain=min(2.,max(.5,.095/max(rms,1e-6)),.86/max(peak,1e-6))
    z=np.pad(y*gain,(0,target-len(y)));save(out,z)
    info=dict(cue_id=c['id'],source_text=c['source_text'],model=c['model'],voice_id=c['voice_id'],preset=c['preset'],api_speed=1.2,post_speed_change=False,processing='Exterior silence trim + 48kHz resample + gain + subframe tail pad; no tempo/pitch change',raw_seconds=len(pcm)/sr,trim_start_seconds=a/sr,trim_end_seconds=b/sr,untruncated_processed_seconds=len(y)/SR,tail_quantization_seconds=(target-len(y))/SR,gain=gain,measured_seconds=target/SR,frames=frames,samples=target,units=c['units'],cps_including_performance=c['units']/(target/SR),sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    out.with_suffix('.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
completed=0;pending=list(PLAN)
while pending:
    next_round=[]
    for c in pending:
        f=P/'audio/final'/(c['id']+'.wav');r=P/'audio/raw'/(c['id']+'.wav')
        if f.exists() and f.with_suffix('.json').exists():completed+=1;continue
        if not r.exists() or not r.with_suffix('.metadata.json').exists():next_round.append(c);continue
        process(c);completed+=1
        if completed%12==0:print(f'Voice finalized {completed}/{len(PLAN)}',flush=True)
    pending=next_round
    if pending:time.sleep(2)
cursor=0;clips=[];cues=[]
for i,c in enumerate(PLAN):
    pcm,sr=read(P/'audio/final'/(c['id']+'.wav'));assert sr==SR and len(pcm)%SPF==0
    if i:clips.append(np.zeros(4800,np.float32));cursor+=3
    frames=len(pcm)//SPF;cues.append(dict(**c,start_frame=cursor,end_frame_exclusive=cursor+frames,audio='audio/final/'+c['id']+'.wav',duration_frames=frames));clips.append(pcm.astype(np.float32)/32768);cursor+=frames
joined=np.concatenate(clips);save(P/'audio/narration-premix.wav',joined)
measure=subprocess.run(['ffmpeg','-v','info','-i',str(P/'audio/narration-premix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
loud=json.loads(measure[measure.rfind('{'):measure.rfind('}')+1]);gain_db=min(-16-float(loud['input_i']),-1.5-float(loud['input_tp']));save(P/'audio/narration.wav',joined*10**(gain_db/20))
old=json.loads((P/'previous-timeline.json').read_text());old_points=[0];new_points=[0]
for x,y in zip(old['cues'],cues):
    assert x['id']==y['id'] and x['source_text']==y['source_text']
    for a,b in [(x['start_frame'],y['start_frame']),(x['end_frame_exclusive'],y['end_frame_exclusive'])]:
        if a==old_points[-1]:assert b==new_points[-1]
        else:old_points.append(a);new_points.append(b)
def mapped(frame):return round(float(np.interp(frame,old_points,new_points)))
shots=[]
for s in old['shots']:
    a=mapped(s['start_frame']);b=mapped(s['end_frame_exclusive']);assert b-a>3
    shots.append(dict(id=s['id'],asset=s['asset'],start_frame=a,end_frame_exclusive=b,duration_frames=b-a))
assert shots[0]['start_frame']==0 and shots[-1]['end_frame_exclusive']==cursor
chapters=[]
for c in cues:
    if not chapters or chapters[-1]['title']!=c['chapter']:chapters.append(dict(title=c['chapter'],start_frame=c['start_frame'],start_seconds=c['start_frame']/FPS))
for i,ch in enumerate(chapters):ch['end_frame_exclusive']=chapters[i+1]['start_frame'] if i+1<len(chapters) else cursor
t=dict(name='山姆避难记·第二集：门外的人 Gentleman 1.2',fps=30,width=1920,height=1080,frame_count=cursor,duration_seconds=cursor/30,audio_sample_rate=SR,audio_samples=len(joined),audio_model='speech-2.8-turbo',voice_id='Chinese (Mandarin)_Gentleman',api_speed=1.2,post_speed_change=False,gap_frames=3,gap_samples=4800,dissolve_frames=3,subtitles_burned=True,independent_subtitle_files=False,cues=cues,shots=shots,chapters=chapters,measured_audio_basis='Natural-duration WAVs measured individually; no post tempo/pitch adjustment. Old picture narrative positions mapped within corresponding speech cues.',loudness_measurement=loud,global_gain_db=gain_db)
(P/'timeline.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n');O=P.parents[1]/'output/LONG-EP02-v3';(O/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status='audio_and_timeline_complete',duration_seconds=cursor/30,frames=cursor,images=len(shots),min_shot_seconds=min(s['duration_frames'] for s in shots)/30,max_shot_seconds=max(s['duration_frames'] for s in shots)/30,global_gain_db=gain_db),ensure_ascii=False),flush=True)
