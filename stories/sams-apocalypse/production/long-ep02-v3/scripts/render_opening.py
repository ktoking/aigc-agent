from pathlib import Path
import json,wave,importlib.util
import numpy as np
P=Path(__file__).resolve().parents[1];plan=json.loads((P/'voice-plan.json').read_text())[:18];old=json.loads((P/'previous-timeline.json').read_text());cues=[];cursor=0
wav=P/'qa/opening-new-voice.wav'
with wave.open(str(wav),'wb') as w:
 w.setparams((1,2,48000,0,'NONE','not compressed'))
 for i,c in enumerate(plan):
  m=json.loads((P/'audio/final'/(c['id']+'.json')).read_text())
  if i:w.writeframes(bytes(9600));cursor+=3
  with wave.open(str(P/'audio/final'/(c['id']+'.wav'))) as src:w.writeframes(src.readframes(src.getnframes()))
  cues.append(dict(**c,display_text=c['source_text'].translate(str.maketrans({'，':' ', ',':' ', '。':'', '.':''})),start_frame=cursor,end_frame_exclusive=cursor+m['frames']));cursor+=m['frames']
a=[0];b=[0]
for x,y in zip(old['cues'],cues):
 for k in ['start_frame','end_frame_exclusive']:
  if x[k]==a[-1]:continue
  a.append(x[k]);b.append(y[k])
end=a[-1];shots=[]
for s in old['shots']:
 if s['start_frame']>=end:break
 x=round(float(np.interp(s['start_frame'],a,b)));y=round(float(np.interp(min(s['end_frame_exclusive'],end),a,b)));shots.append(dict(s,start_frame=x,end_frame_exclusive=y,duration_frames=y-x))
t=dict(frame_count=cursor,cues=cues,shots=shots,dissolve_frames=3)
(P/'qa/opening-new-voice.timeline.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('renderer',P/'scripts/render.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
r=module.render(t,wav,P/'qa/opening-new-voice.mp4');(P/'qa/opening-new-voice.manifest.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r),flush=True)
