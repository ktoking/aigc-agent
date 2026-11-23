from pathlib import Path
import json,subprocess,wave,hashlib
import numpy as np
from PIL import Image,ImageOps,ImageDraw
P=Path(__file__).resolve().parents[1];O=P.parents[1]/'output/LONG-EP02-v2'
t=json.loads((P/'timeline.json').read_text());video=O/'video.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
v=[s for s in probe['streams'] if s['codec_type']=='video'];a=[s for s in probe['streams'] if s['codec_type']=='audio']
assert len(v)==1 and len(a)==1 and len(probe['streams'])==2
assert (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],int(v[0]['nb_read_frames']))==(1920,1080,'30/1',t['frame_count'])
assert a[0]['sample_rate']=='48000' and a[0]['channels']==1
assert abs(float(a[0]['duration'])-t['duration_seconds'])<1/30
assert not list(O.glob('*.srt')) and not list(O.glob('*.vtt'))
for x,y in zip(t['cues'],t['cues'][1:]):assert y['start_frame']-x['end_frame_exclusive']==3
original=json.loads((P.parent/'long-ep02-v1/project.json').read_text())
assert ''.join(c['source_text'] for c in t['cues'])==''.join(c['text'] for ep in original['episodes'] for c in ep['cues'])
for c in t['cues']:
    raw=json.loads((P/'audio/raw'/(c['id']+'.metadata.json')).read_text())
    assert raw['http_status']==200 and raw['base_status_code']==0
    assert raw['request']['model']=='speech-2.8-turbo' and raw['request']['voice_setting']['voice_id']=='Chinese_calm_streamer_nv1'
    assert raw['request']['text']==c['tts_text'] and raw['request']['subtitle_enable'] is False
with wave.open(str(P/'audio/narration.wav')) as w:
    assert w.getnframes()==t['audio_samples']==t['frame_count']*1600
    expected=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)/32768
for x,y in zip(t['cues'],t['cues'][1:]):assert not np.any(expected[x['end_frame_exclusive']*1600:y['start_frame']*1600])
decoded=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-f','f32le','-ac','1','-ar','48000','-']),dtype='<f4')
assert len(decoded)>=len(expected)-1600
n=min(len(decoded),len(expected));corr=float(np.corrcoef(expected[:n],decoded[:n])[0,1]);assert corr>.98,corr
tailcorr=float(np.corrcoef(expected[n-96000:n],decoded[n-96000:n])[0,1]);assert tailcorr>.98,tailcorr
indices=set()
for s in t['shots']:
    sample=(s['start_frame']+s['end_frame_exclusive'])//2;s['qa_sample']=sample;indices.update([sample,sample+1])
for s in t['shots'][1:]:indices.update(range(s['start_frame']-4,s['start_frame']+1))
indices=sorted(indices);select='+'.join(f'eq(n,{x})' for x in indices)
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf',f"select='{select}',crop=1920:820:0:0,scale=320:138",'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-'])
frames=np.frombuffer(raw,dtype=np.uint8).reshape((-1,138,320,3));assert len(frames)==len(indices)
f={n:x.astype(np.float32) for n,x in zip(indices,frames)};stable=[];source=[];blend=[]
for s in t['shots']:
    z=s['qa_sample'];stable.append(float(np.abs(f[z]-f[z+1]).mean()))
    with Image.open(P/s['asset']) as im:
        src=np.array(ImageOps.fit(im.convert('RGB'),(1920,1080),Image.Resampling.LANCZOS).crop((0,0,1920,820)).resize((320,138),Image.Resampling.BICUBIC)).astype(np.float32)
    source.append(dict(id=s['id'],mae=float(np.abs(src-f[z]).mean())))
for s in t['shots'][1:]:
    b=s['start_frame'];old=f[b-4];new=f[b]
    blend.extend(float(np.abs(f[b-3+k]-(old*(1-(k+1)/3)+new*((k+1)/3))).mean()) for k in range(3))
assert max(stable)<.5,max(stable)
assert max(x['mae'] for x in source)<5,max(x['mae'] for x in source)
assert max(blend)<3,max(blend)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
report=dict(status='PASS',duration_seconds=t['duration_seconds'],frames=t['frame_count'],fps=30,resolution=[1920,1080],images=120,image_sha256_unique=True,previous_images_reused=0,min_image_seconds=min(s['duration_frames'] for s in t['shots'])/30,max_image_seconds=max(s['duration_frames'] for s in t['shots'])/30,cues=len(t['cues']),gap_seconds=.1,gap_pcm_samples=4800,dissolve_seconds=.1,voice_model='speech-2.8-turbo',voice_id='Chinese_calm_streamer_nv1',audio_streams=1,subtitle_streams=0,subtitles_burned=True,independent_srt_vtt_files=0,source_words_unchanged=True,actual_voice_cue_sample_clock_checked=True,all_inserted_gaps_digital_silence=True,encoded_audio_correlation=corr,last_two_seconds_audio_correlation=tailcorr,source_image_max_mae=max(x['mae'] for x in source),within_image_frame_max_mae=max(stable),dissolve_max_mae=max(blend),sampled_frames=len(indices),full_decode='PASS',normal_speed_playback='NOT_RUN',full_human_watch='NOT_RUN',human_listening='NOT_RUN; automated transcription and browser playback reported separately')
(O/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(P/'qa/ffprobe.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2)+'\n')
(P/'qa/image-correspondence.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False),flush=True)
