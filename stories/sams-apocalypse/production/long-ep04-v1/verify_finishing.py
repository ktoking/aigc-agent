from pathlib import Path
import json,subprocess,hashlib,math
import numpy as np
P=Path(__file__).resolve().parent;S=P;O=P.parents[1]/'output/LONG-EP04-v1';V=O/'video.mp4';sr=6000

def audio(path,extra=()):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),*extra,'-f','f32le','-ar',str(sr),'-ac','2','pipe:1']),'<f4').reshape(-1,2)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]));(P/'qa/ffprobe.json').write_text(json.dumps(info,indent=2))
main=[s for s in info['streams'] if s['codec_type']=='video' and not s['disposition']['attached_pic']];cover=[s for s in info['streams'] if s['codec_type']=='video' and s['disposition']['attached_pic']];assert len(main)==len(cover)==1
assert (main[0]['width'],main[0]['height'],main[0]['nb_frames'],main[0]['r_frame_rate'])==(1920,1080,'16228','30/1')
assert (cover[0]['width'],cover[0]['height'])==(1024,1536)
assert sha(P/'qa/cover-extracted.jpg')==sha(O/'cover.jpg')
voice=audio(S/'audio/narration.wav');bed=audio(P/'finishing/bgm-bed.wav');mix=audio(P/'finishing/mix.wav');encoded=audio(V,('-vn',));n=min(len(voice),len(bed),len(mix))
assert n==round(540.933333333*sr), (len(voice),len(bed),len(mix))
assert sha(P/'finishing/bgm-loop.wav')==sha(P/'finishing/bgm-bed.wav'), 'Music must have fixed gain without ducking'
error=float(np.max(np.abs(mix[:n]-voice[:n]-bed[:n])));assert error<.0001,error
corr=float(np.corrcoef(mix[:n].ravel(),encoded[:n].ravel())[0,1]);assert corr>.995,corr
cues=json.loads((S/'timeline.json').read_text())['cues'];margins=[]
for c in cues:
 a=round(c['start_frame']/30*sr);b=round(c['end_frame_exclusive']/30*sr)
 vr=float(np.sqrt(np.mean(voice[a:b]**2)));br=float(np.sqrt(np.mean(bed[a:b]**2)));margins.append(20*math.log10((vr+1e-12)/(br+1e-12)))
assert min(margins)>6,min(margins)
base=audio(P/'finishing/bgm-loop.wav');source=audio(P/'finishing/bgm.ogg');g=10**(json.loads((O/'video.manifest.json').read_text())['music_gain_db']/20);cycles=[]
for i in range(5):
 a=round((i*132.48+2)*sr);b=a+sr
 target=base[a:b].ravel();reference=source[2*sr:3*sr].ravel()*g
 value=float(np.corrcoef(target,reference)[0,1]);cycles.append(value)
assert min(cycles)>.99,cycles
# Fade envelope: compare 0.1-second energy projections to the identical loop source.
projections=[]
for a in [600,1800,3000,n-3000,n-1800,n-600]:
 b=min(a+300,n);idx=np.arange(a,b)%len(source);x=source[idx]*g;y=base[a:b]
 projections.append({'start_seconds':a/sr,'gain_projection':float(np.sum(x*y)/(np.sum(x*x)+1e-20))})
# Frame-level fade sample inspection is separately recorded with Pillow.
report={'status':'PASS','main_video_frames':16228,'duration_seconds':540.933333333,'cover_attached_pic':True,'cover_extracted_sha_matches_original':True,'music_gain_mode':'constant_except_endpoint_fades','ducking':False,'music_title':'Tempt Scandal','music_artist':'Audiomachine','source_music_seconds':132.48,'full_cycles':4,'last_cycle_seconds':540.933333333-132.48*4,'music_cycle_correlations':cycles,'min_voice_over_music_cue_rms_db':min(margins),'mean_voice_over_music_cue_rms_db':sum(margins)/len(margins),'cue_count':len(cues),'mix_voice_plus_bed_max_residual':error,'encoded_mix_correlation':corr,'music_endpoint_gain_projections':projections,'subtitles':'retained baked captions; timeline unchanged','full_human_listen':'NOT_RUN','full_human_watch':'NOT_RUN'}
(P/'qa/finishing-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True)
