from pathlib import Path
import json, subprocess
import numpy as np
from PIL import Image, ImageOps, ImageDraw
P=Path(__file__).resolve().parents[1]
O=P.parents[1]/'output/LONG-EP05-v1'
t=json.loads((P/'timeline.json').read_text());n=t['frame_count']
def frame(f):
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/30),'-i',str(O/'video.mp4'),'-map','0:v:0','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
    return Image.frombytes('RGB',(1920,1080),raw)
frames=[0,4,8,30,t['cues'][30]['end_frame_exclusive'],t['cues'][30]['end_frame_exclusive']+1,t['cues'][31]['start_frame'],n//2,n-10,n-5,n-1]
page=Image.new('RGB',(1440,1210),'#202020');draw=ImageDraw.Draw(page)
means=[]
for i,f in enumerate(frames):
    im=frame(f);im.save(P/f'qa/final-frame-{f:05d}.png');means.append(float(np.asarray(im).mean()))
    x=(i%3)*480;y=(i//3)*300;page.paste(ImageOps.fit(im,(472,266)),(x,y));draw.text((x+4,y+271),f'frame {f} / {f/30:.3f}s',fill='white')
page.save(P/'qa/final-frames.jpg')
assert means[0]<1 and means[-1]<1
assert means[0]<means[1]<means[2] and means[-3]>means[-2]>means[-1]
assert len(t['shots'])==113
assert all(120<=s['end_frame_exclusive']-s['start_frame']<=180 for s in t['shots'])
assert all(b['start_frame']-a['end_frame_exclusive']==3 for a,b in zip(t['cues'],t['cues'][1:]))
assert all(not any(x in c['display_text'] for x in ',，.。') for c in t['cues'])
report=dict(status='PASS',frame_samples=frames,frame_mean_rgb=means,endpoint_fades='PASS first/last black and monotonic sampled ramps',shot_count=len(t['shots']),shot_range_seconds=[min(s['end_frame_exclusive']-s['start_frame'] for s in t['shots'])/30,max(s['end_frame_exclusive']-s['start_frame'] for s in t['shots'])/30],external_gap_frames=3,dissolve_frames=3,caption_punctuation='PASS',human_full_watch='NOT_RUN',human_full_listen='NOT_RUN')
(P/'qa/final-frames.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
