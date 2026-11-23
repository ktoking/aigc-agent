from pathlib import Path
import importlib.util,json,wave,numpy as np
P=Path(__file__).resolve().parents[1]
plan=json.loads((P/'voice-plan.json').read_text());shots=json.loads((P/'shot-plan.json').read_text())
cursor=0;cues=[];clips=[]
for c in plan:
    info=json.loads((P/'audio/final'/(c['id']+'.json')).read_text())
    frames=info['frames'];start=cursor+(3 if cues else 0)
    if start+frames>30*30:break
    if cues:clips.append(np.zeros(4800,dtype='<i2'))
    with wave.open(str(P/'audio/final'/(c['id']+'.wav'))) as w:clips.append(np.frombuffer(w.readframes(w.getnframes()),dtype='<i2'))
    cues.append(dict(**c,start_frame=start,end_frame_exclusive=start+frames))
    cursor=start+frames
t=dict(frame_count=cursor,cues=cues,shots=[dict(s,end_frame_exclusive=min(s['end_frame_exclusive'],cursor)) for s in shots if s['start_frame']<cursor])
audio=P/'qa/early-preview.wav'
with wave.open(str(audio),'wb') as w:w.setparams((1,2,48000,0,'NONE','not compressed'));w.writeframes(np.concatenate(clips).tobytes())
spec=importlib.util.spec_from_file_location('renderer',P/'scripts/render.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
result=mod.render(t,audio,P/'qa/early-preview.mp4')
(P/'qa/early-preview.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
