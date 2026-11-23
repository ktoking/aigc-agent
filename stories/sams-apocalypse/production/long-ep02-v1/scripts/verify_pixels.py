from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image,ImageOps
P=Path(__file__).resolve().parents[1]
O=P.parents[1]/'output/LONG-EP02-v1'
t=json.loads((O/'timeline.json').read_text())
shots=[]
for c in t['cues']:
    if not shots or shots[-1]['asset']!=c['asset']:shots.append(dict(asset=c['asset'],start=c['start_frame'],end=c['end_frame_exclusive']))
    else:shots[-1]['end']=c['end_frame_exclusive']
indices=set()
for s in shots:
    s['sample']=(s['start']+s['end'])//2
    indices.update([s['sample'],s['sample']+1])
for tr in t['transitions']:indices.update(range(tr['start_frame']-1,tr['end_frame_exclusive']+1))
indices=sorted(indices)
select='+'.join(f'eq(n,{i})' for i in indices)
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(O/'video.mp4'),'-vf',f"select='{select}',scale=320:180",'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-'])
frames=np.frombuffer(raw,dtype=np.uint8).reshape((-1,180,320,3))
assert len(frames)==len(indices)
f={n:x.astype(np.float32) for n,x in zip(indices,frames)}
stable=[];source=[];blends=[]
for s in shots:
    stable.append(float(np.abs(f[s['sample']]-f[s['sample']+1]).mean()))
    with Image.open(P/t['assets'][s['asset']]) as im:
        expected=np.array(ImageOps.fit(im.convert('RGB'),(1920,1080),method=Image.Resampling.LANCZOS).resize((320,180),Image.Resampling.BICUBIC)).astype(np.float32)
    source.append(dict(asset=s['asset'],mae=float(np.abs(expected-f[s['sample']]).mean())))
for tr in t['transitions']:
    a=tr['start_frame'];b=tr['end_frame_exclusive'];old=f[a-1];new=f[b]
    maes=[float(np.abs(f[n]-(old*(1-(n-a+1)/(b-a))+new*((n-a+1)/(b-a)))).mean()) for n in range(a,b)]
    blends.append(dict(start_frame=a,maes=maes))
assert max(stable)<.5,('unexpected within-shot movement',max(stable))
assert max(x['mae'] for x in source)<5,('source-to-render discrepancy',source)
assert max(v for x in blends for v in x['maes'])<3,('incorrect dissolve',blends)
report=dict(status='PASS',checked_shots=len(shots),checked_transitions=len(blends),sampled_encoded_frames=len(indices),within_shot_neighbor_mae_max=max(stable),source_correspondence_mae_max=max(x['mae'] for x in source),dissolve_mae_max=max(v for x in blends for v in x['maes']),source_samples=source,dissolves=blends,limitations='Static pixel check is not full normal-speed viewing or future audio alignment')
(O/'pixel-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
contact=Image.new('RGB',(4*480,3*292),(25,29,33))
from PIL import ImageDraw
d=ImageDraw.Draw(contact)
for k,si in enumerate([0,4,7,14,22,27,36,45,55,62,67,71]):
    s=shots[si];im=Image.fromarray(f[s['sample']].astype(np.uint8)).resize((480,270))
    x=(k%4)*480;y=(k//4)*292;contact.paste(im,(x,y));d.text((x+8,y+273),s['asset']+f" @ {s['sample']/30:.2f}s",fill='white')
contact.save(P/'qa/encoded-contact.jpg',quality=90)
print(json.dumps({k:v for k,v in report.items() if k not in ['source_samples','dissolves']},ensure_ascii=False))
