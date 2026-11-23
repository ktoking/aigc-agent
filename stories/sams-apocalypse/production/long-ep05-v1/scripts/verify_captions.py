from pathlib import Path
import json,subprocess,importlib.util
import numpy as np
from PIL import Image,ImageOps
P=Path(__file__).resolve().parents[1];t=json.loads((P/'timeline.json').read_text())
spec=importlib.util.spec_from_file_location('render_ep05',P/'scripts/render.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
samples={}
for c in t['cues']:
 f=(c['start_frame']+c['end_frame_exclusive'])//2
 samples[f]=dict(cue=c,caption=c['display_text'],mode='speech')
 if c is not t['cues'][-1]:samples[c['end_frame_exclusive']+1]=dict(cue=c,caption='',mode='external_gap')
frames=sorted(samples)
expr='+'.join(f'eq(n,{f})' for f in frames)
cmd=['ffmpeg','-v','error','-i',str(P/'qa/video-base.mp4'),'-an','-vf',f"select='{expr}',crop=1920:280:0:800",'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','pipe:1']
proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
cache={};rows=[]
def picture(s):
 sid=s['id']
 if sid not in cache:
  with Image.open(P/s['asset']) as im:cache[sid]=ImageOps.fit(im.convert('RGB'),(1920,1080),Image.Resampling.LANCZOS)
 return cache[sid]
for f in frames:
 row=samples[f];raw=proc.stdout.read(1920*280*3);assert len(raw)==1920*280*3
 actual=np.frombuffer(raw,np.uint8).reshape(280,1920,3)
 si=max(i for i,s in enumerate(t['shots']) if s['start_frame']<=f);base=picture(t['shots'][si])
 if si+1<len(t['shots']) and f>=t['shots'][si+1]['start_frame']-3:
  alpha=(f-(t['shots'][si+1]['start_frame']-3)+1)/3;base=Image.blend(base,picture(t['shots'][si+1]),alpha)
 cap=renderer.caption(row['cue']['display_text']);cm=np.asarray(cap.crop((0,800,1920,1080)))
 bg=np.asarray(base.crop((0,800,1920,1080)))
 mask=(cm[:,:,3]>250)&(cm[:,:,0]>240)&(bg.mean(axis=2)<185)
 expected=base.copy()
 if row['caption']:expected.paste(cap,(0,0),cap)
 exp=np.asarray(expected.crop((0,800,1920,1080)))
 assert mask.sum()>50,(f,mask.sum())
 error=float(np.abs(actual.astype(np.float32)-exp.astype(np.float32))[mask].mean())
 assert error<16,(f,row['mode'],error)
 rows.append(dict(frame=f,cue=row['cue']['id'],mode=row['mode'],contrast_core_pixels=int(mask.sum()),mean_absolute_pixel_error=error))
assert proc.wait()==0,proc.stderr.read().decode()
report=dict(status='PASS',speech_caption_samples=sum(r['mode']=='speech' for r in rows),blank_external_gap_samples=sum(r['mode']=='external_gap' for r in rows),method='Actual encoded caption-region pixels compared against exact expected image and caption raster; high-contrast glyph cores tested in speech and blank gaps',max_mean_core_error=max(r['mean_absolute_pixel_error'] for r in rows),threshold=16,rows=rows)
(P/'qa/caption-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False),flush=True)
