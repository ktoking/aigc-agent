#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,re,hashlib,struct
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=R/'output/photoreal-6min-v1';D=json.loads((P/'timeline.json').read_text());V=O/'you-are-safe-photoreal-6min-v1.mp4'
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))
def seconds(stamp):
 h,m,s=stamp.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
info=probe(V);streams=info['streams'];video=[s for s in streams if s['codec_type']=='video'];audio=[s for s in streams if s['codec_type']=='audio'];subs=[s for s in streams if s['codec_type']=='subtitle']
assert len(video)==1 and not audio and not subs
v=video[0];assert (v['width'],v['height'])==(1920,1080) and v['r_frame_rate']=='30/1';assert int(v['nb_read_frames'])==D['frames']
subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],stderr=(P/'qa/full-decode.log').open('w'),check=True)
srt=(O/'you-are-safe.zh-CN.srt').read_text();blocks=srt.strip().split('\n\n');assert len(blocks)==len(D['cues'])
gaps=[];previous=0
for b,c in zip(blocks,D['cues']):
 lines=b.splitlines();a,z=map(seconds,lines[1].split(' --> '));text=''.join(lines[2:]);assert text==c['text'];assert abs(a-c['start_frame']/30)<=.001 and abs(z-c['end_frame_exclusive']/30)<=.001
 assert a>=previous and z>a
 if a>previous+.002:gaps.append({'start':previous,'end':a,'seconds':round(a-previous,3)})
 previous=z
if D['frames']/30>previous+.002:gaps.append({'start':previous,'end':D['frames']/30,'seconds':round(D['frames']/30-previous,3)})
assert abs(sum(g['seconds'] for g in gaps)-sum(s['pause_frames'] for s in D['shots'])/30)<.02
narration=(P/'narration.txt').read_text();assert ''.join(narration.split())==''.join(c['text'] for c in D['cues'])
assert all(not re.match(r'^(客服|母亲|朵朵|医生)[：:]',c['text']) for c in D['cues'])
assert sum(len(re.findall(r'[\u4e00-\u9fffA-Za-z0-9]',c['text'])) for c in D['cues'])==D['reading_units']
assets=[]
for s in D['shots']:
 f=P/s['asset'];raw=f.read_bytes();w,h=struct.unpack('>II',raw[16:24]);assert w>h
 assets.append({'id':s['id'],'path':str(f.relative_to(R)),'width':w,'height':h,'sha256':hashlib.sha256(raw).hexdigest()})
report={'status':'PASS_technical_checks','video':str(V.relative_to(R)),'width':1920,'height':1080,'fps':30,'frames':D['frames'],'seconds':D['duration_seconds'],'audio_streams':len(audio),'embedded_subtitle_streams':len(subs),'caption_cues':len(blocks),'reading_units':D['reading_units'],'reading_rate_estimate':7.5,'authored_pause_seconds':sum(s['pause_frames'] for s in D['shots'])/30,'gaps':gaps,'full_decode':'PASS','subtitle_text_and_frame_timing':'PASS','first_person_voice_policy':'single narrator text; no audio generated','timing_basis':'text_estimate_not_audio_aligned','native_source_dimensions':sorted(set((x['width'],x['height']) for x in assets)),'upscaled_delivery':True,'assets':assets,'visual_review':'record separately; structural checks do not prove identity or motion quality','video_sha256':hashlib.sha256(V.read_bytes()).hexdigest()}
(P/'qa/technical-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
manifest={'film':'you-are-safe-photoreal-6min-v1.mp4','srt':'you-are-safe.zh-CN.srt','vtt':'you-are-safe.zh-CN.vtt','narration':'narration.txt','frames':D['frames'],'seconds':D['duration_seconds'],'reading_rate':7.5,'timing_basis':'text_estimate_not_audio_aligned','audio':False,'subtitles_burned':False,'style':'正常自然光、干燥洁净真人写实','transition_seconds':D['transition_seconds'],'source_shots':96,'technical_report':'../../production/photoreal-6min-v1/qa/technical-report.json'}
(O/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','frames','seconds','audio_streams','embedded_subtitle_streams','caption_cues','authored_pause_seconds','native_source_dimensions']},ensure_ascii=False))
if __name__=='__main__':pass
