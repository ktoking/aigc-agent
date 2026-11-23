from pathlib import Path
import json,subprocess
P=Path(__file__).resolve().parents[1];D=json.loads((P/'timeline.json').read_text());Q=P/'qa'
assert D['transition_frames']==3 and D['transition_seconds']==0.1
render=json.loads((P/'render-manifest.json').read_text());assert render['transition_frames']==3
def cmd(args):return subprocess.check_output(['ffmpeg','-v','error']+args)
def gray(path):
 return cmd(['-i',str(path),'-vf','scale=160:90:flags=area','-frames:v','1','-pix_fmt','gray','-f','rawvideo','-'])
def diff(a,b):return sum(abs(x-y) for x,y in zip(a,b))/len(a)
results=[]
for idx in [1,8,24,40,56,72,77,80,88,95]:
 s=D['shots'][idx];prev=gray(P/D['shots'][idx-1]['asset']);now=gray(P/s['asset']);size=len(now)
 raw=cmd(['-i',str(P/'clips'/f"{s['id']}.mp4"),'-vf','scale=160:90:flags=area','-frames:v','5','-pix_fmt','gray','-f','rawvideo','-'])
 samples=[]
 for f in range(5):
  frame=raw[f*size:(f+1)*size];alpha=min(f/3,1);expected=bytes(round(a*(1-alpha)+b*alpha) for a,b in zip(prev,now))
  samples.append({'frame':f,'relative_seconds':f/30,'expected_incoming_alpha':alpha,'mean_abs_error':round(diff(frame,expected),4),'distance_to_incoming':round(diff(frame,now),4)})
 assert all(x['mean_abs_error']<5 for x in samples),(s['id'],samples)
 assert samples[3]['distance_to_incoming']<5
 results.append({'shot':s['id'],'frames':samples})
(Q/'transitions.json').write_text(json.dumps({'status':'PASS','transition_frames':3,'transition_seconds':0.1,'transition_count':95,'adds_to_runtime':False,'method':'encoded first five frames compared with three-frame linear blend; tolerance 5 gray levels; ten boundaries sampled','samples':results},ensure_ascii=False,indent=2)+'\n')
print('PASS: 0.1s transition configuration and ten encoded boundaries')
