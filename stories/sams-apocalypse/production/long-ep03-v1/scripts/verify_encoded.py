from pathlib import Path
import subprocess,json,wave,statistics
import numpy as np
P=Path(__file__).resolve().parents[1];V=P.parents[1]/'output/LONG-EP03-v1/video.mp4';t=json.loads((P/'timeline.json').read_text());n=t['frame_count']
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(V)]))
(P/'qa/ffprobe.json').write_text(json.dumps(probe,indent=2))
streams=probe['streams'];vs=[s for s in streams if s['codec_type']=='video'];a=[s for s in streams if s['codec_type']=='audio'];assert len(vs)==len(a)==1 and len(streams)==2
assert (vs[0]['width'],vs[0]['height'],vs[0]['r_frame_rate'],int(vs[0]['nb_frames']))==(1920,1080,'30/1',n)
assert abs(float(a[0]['duration'])-n/30)<1/30
# Independently inspect every encoded picture above the caption region.
cmd=['ffmpeg','-v','error','-xerror','-i',str(V),'-an','-vf','crop=1920:780:0:0,scale=192:78','-pix_fmt','gray','-f','rawvideo','pipe:1']
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);previous=None;diffs=[];count=0
while True:
 b=p.stdout.read(192*78)
 if not b:break
 assert len(b)==192*78
 current=np.frombuffer(b,np.uint8).astype(np.int16)
 if previous is not None:diffs.append(float(np.abs(current-previous).mean()))
 previous=current;count+=1
assert p.wait()==0,p.stderr.read().decode();assert count==n
fade_frames=set()
for shot in t['shots'][1:]:fade_frames.update(range(shot['start_frame']-3,shot['start_frame']))
# Current-frame changes through three dissolve frames are excluded from fixed-frame measurements.
fixed=[d for f,d in enumerate(diffs,1) if f not in fade_frames]
assert max(fixed)<0.8,('unexpected frame movement',max(fixed))
fade_checks=[]
for shot in t['shots'][1:]:
 b=shot['start_frame'];values=diffs[b-4:b-1]
 fade_checks.append({'shot':shot['id'],'frames':[b-3,b-2,b-1],'mean_abs_deltas':values,'has_three_visible_changes':all(d>0.8 for d in values)})
assert all(x['has_three_visible_changes'] for x in fade_checks)
# Decode actual AAC and compare each spoken cue to source audio, detecting drift/truncation.
encoded=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(V),'-vn','-f','f32le','-ac','1','-ar','48000','pipe:1']),'<f4')
with wave.open(str(P/'audio/narration.wav')) as w:source=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
correlations=[]
for cue in t['cues']:
 l=cue['start_frame']*1600;r=cue['end_frame_exclusive']*1600
 x=source[l:r:8];y=encoded[l:r:8];assert len(x)==len(y)
 correlations.append(float(np.corrcoef(x,y)[0,1]))
assert min(correlations)>.985,min(correlations)
report={'status':'PASS','frame_count':count,'width':1920,'height':1080,'fps':30,'duration_seconds':n/30,'full_decode':'PASS ffmpeg -xerror all frames and audio','fixed_image_motion_check':{'status':'PASS','region':'upper 1920x780 excluding captions; reduced to192x78 grayscale','measured_frame_pairs':len(fixed),'max_mean_abs_pixel_delta':max(fixed),'threshold':0.8,'note':'compression changes allowed; all intended image changes confined to3frame dissolves'},'dissolves':fade_checks,'cue_audio_correlation':{'count':144,'min':min(correlations),'mean':statistics.mean(correlations),'status':'PASS'},'external_gap_frames':3,'audio_streams':1,'subtitle_streams':0,'captions':'burned; sample frames reviewed separately','human_full_listen':'NOT_RUN','human_full_watch':'NOT_RUN'}
(P/'qa/encoded-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='dissolves'},ensure_ascii=False),flush=True)
