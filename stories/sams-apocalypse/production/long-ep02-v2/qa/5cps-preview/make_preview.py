from pathlib import Path
import json,subprocess,wave,hashlib
import numpy as np
P=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
T=json.loads((P/'timeline.json').read_text());SR=48000
cues={c['id']:c for c in T['cues']}
sections=[('01-opening','开场悬疑',range(1,7)),('02-danger','危险段落',range(136,142)),('03-gentle','温柔段落',range(245,251))]
report=[]
for slug,title,ids in sections:
    clips=[];rows=[];cursor=0
    for i,n in enumerate(ids):
        cid=f'c{n:03}';c=cues[cid];m=json.loads((P/'audio/final'/f'{cid}.json').read_text())
        with wave.open(str(P/'audio/raw'/f'{cid}.wav')) as w:
            sr=w.getframerate();x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2')
        x=x[round(m['trim_start_seconds']*sr):round(m['trim_end_seconds']*sr)]
        target=round((c['units']/5+c.get('breath_seconds',0))*SR)
        tempo=(len(x)/sr)/(target/SR-.018)
        for attempt in range(4):
            data=subprocess.check_output(['ffmpeg','-v','error','-f','s16le','-ar',str(sr),'-ac','1','-i','pipe:0','-af',f'atempo={tempo:.9f},aresample={SR}','-f','f32le','pipe:1'],input=x.tobytes())
            y=np.frombuffer(data,dtype='<f4').copy()
            if len(y)<=target:break
            tempo*=len(y)/target*1.01
        else:raise RuntimeError(cid)
        gain=m['gain']*10**(T['global_gain_db']/20)
        y=np.pad(y*gain,(0,target-len(y)))
        if i:clips.append(np.zeros(4800,np.float32));cursor+=4800
        rows.append({'id':cid,'text':c['source_text'],'units':c['units'],'start_seconds':cursor/SR,'duration_seconds':len(y)/SR,'atempo_from_raw':tempo})
        clips.append(y);cursor+=len(y)
    audio=np.concatenate(clips)
    wav=O/f'{slug}-5cps.wav';mp3=O/f'{slug}-5cps.mp3'
    with wave.open(str(wav),'wb') as w:
        w.setparams((1,2,SR,0,'NONE','not compressed'));w.writeframes(np.rint(np.clip(audio,-1,.999969)*32768).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-c:a','libmp3lame','-b:a','192k',str(mp3)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(mp3),'-f','null','-'],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(mp3)]))
    row={'title':title,'file':str(mp3.resolve()),'duration_seconds':len(audio)/SR,'cps_target':5,'gap_seconds':.1,'pitch_preserved':True,'new_tts_requests':0,'full_decode':'PASS','peak':float(abs(audio).max()),'cues':rows,'probe_duration_seconds':float(probe['format']['duration']),'sha256':hashlib.sha256(mp3.read_bytes()).hexdigest()}
    report.append(row)
(O/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['title','file','duration_seconds','cps_target','full_decode']} for r in report],ensure_ascii=False))
