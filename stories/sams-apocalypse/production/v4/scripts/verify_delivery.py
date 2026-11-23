from pathlib import Path
import json,re,subprocess,hashlib,wave,statistics,zipfile
import numpy as np
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'production/v4';OUT=ROOT/'output/EP001-EP008-v4';Q=OUT/'qa'
e=json.loads((P/'edit-timeline.json').read_text());video=OUT/'EP001-EP008_sams_apocalypse_v4.mp4'
def run(args):return subprocess.run(list(map(str,args)),check=True,capture_output=True,text=True)
probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',video]).stdout)
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(960,544,'30/1',e['output_frames'])
assert abs(float(v['duration'])-e['output_seconds'])<.001
assert len(probe['streams'])==2 and a['sample_rate']=='44100'
run(['ffmpeg','-v','error','-i',video,'-f','null','-'])
# Validate removed ranges against the unpadded original speech detector output.
vad=json.loads((P/'analysis/vad.json').read_text());removed_voice=[]
for r in e['sentence_pause_removals']:
 a,b=r['start_frame']/30,r['end_frame_exclusive']/30
 overlap=sum(max(0,min(b,x['end'])-max(a,x['start'])) for x in vad)
 if overlap>0:removed_voice.append({'removal':r,'overlap':overlap})
assert not removed_voice
# PCM sample-for-sample equality in each retained region away from 2ms anticlick ramps.
with wave.open(str(P/'analysis/source-fullrate.wav'),'rb') as f:raw=np.frombuffer(f.readframes(f.getnframes()),np.int16)
with wave.open(str(P/'analysis/compacted.wav'),'rb') as f:edited=np.frombuffer(f.readframes(f.getnframes()),np.int16)
cursor=0
for a,b in e['keep_ranges']:
 original=raw[a*1470:b*1470];length=len(original)
 assert np.array_equal(original[88:-88],edited[cursor+88:cursor+length-88]);cursor+=length
assert cursor==len(edited)==e['output_frames']*1470
# Subtitle text and continuity.
old=(ROOT/'output/EP001-EP008-v3/EP001-EP008_sams_apocalypse_v3.zh-CN.srt').read_text().strip().split('\n\n')
new=(OUT/'EP001-EP008_sams_apocalypse_v4.zh-CN.srt').read_text().strip().split('\n\n')
assert len(old)==len(new)==130
for x,y in zip(old,new):assert ''.join(x.splitlines()[2:])==''.join(y.splitlines()[2:])
b=[x.splitlines()[1].split(' --> ') for x in new];assert all(x[1]==y[0] for x,y in zip(b,b[1:]))
# Source/script rate evidence; exclude voice groups crossing known sentence boundaries.
rates=[]
for c in e['cues']:
 ss=[x for x in vad if x['end']>c['source_start'] and x['start']<c['source_end']]
 if ss and ss[0]['start']>=c['source_start'] and ss[-1]['end']<=c['source_end']:
  chars=len(re.findall(r'[\u4e00-\u9fffA-Za-z0-9]',c['text']));span=ss[-1]['end']-ss[0]['start']
  rates.append({'text':c['text'],'characters':chars,'speech_phrase_span':span,'cps':chars/span})
speed={'method':'known authored text / first-to-last VAD speech inside original cue; includes natural internal phrasing pauses; not forced word alignment','sample_count':len(rates),'median_cps':statistics.median(x['cps'] for x in rates),'p25_cps':statistics.quantiles([x['cps'] for x in rates],n=4)[0],'p75_cps':statistics.quantiles([x['cps'] for x in rates],n=4)[2],'future_draft_cps':7.5,'final_timing_basis':'actual supplied audio','samples':rates}
(P/'analysis/speaking-rate.json').write_text(json.dumps(speed,ensure_ascii=False,indent=2)+'\n')
# All 69 transition midpoint frames plus 10 regular views.
times=sorted(set([t['output_frame']+1 for t in e['transitions']]+[round(s*30) for s in range(0,int(e['output_seconds']),25)]))
expr='+'.join(f'eq(n,{i})' for i in times)
run(['ffmpeg','-v','error','-y','-i',video,'-vf',f"select='{expr}',scale=320:181,tile=10x9:padding=2:margin=2",'-frames:v','1',Q/'dissolve-review.jpg'])
# Six-frame sequences centered around four first transitions.
for i,t in enumerate(e['transitions'][:4],1):
 start=max(0,t['output_frame']-1);end=start+6
 run(['ffmpeg','-v','error','-y','-i',video,'-vf',f"select='gte(n,{start})*lt(n,{end})',scale=480:272,tile=6x1:padding=2:margin=2",'-frames:v','1',Q/f'transition-{i:02d}.jpg'])
with zipfile.ZipFile(OUT/'EP001-EP008_v4_subtitles.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in OUT.glob('*.srt'):z.write(p,p.name)
report={'status':'technical_checks_passed_review_pending','source_seconds':e['source_seconds'],'output_seconds':e['output_seconds'],'removed_seconds':e['removed_seconds'],'sentence_pause_removals':len(e['sentence_pause_removals']),'picture_dissolves':len(e['transitions']),'transition_duration_frames':4,'audio_preserved':True,'speech_regenerated':False,'speech_rate_changed':False,'audio_overlap':False,'removed_detected_speech_seconds':0,'retained_pcm_inner_samples_exact':True,'audio_edge_ramps_ms':2,'external_subtitle_cues':130,'subtitle_text_exact':True,'subtitle_boundaries_continuous':True,'existing_burned_subtitles_retained':True,'new_subtitles_burned':False,'resolution':[960,544],'resolution_note':'preserves supplied source raster; no invented native 1080p','fps':30,'frames':e['output_frames'],'audio_streams':1,'full_decode':'passed','speaking_rate_median_cps':speed['median_cps'],'speaking_rate_samples':len(rates),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'bytes':video.stat().st_size,'visual_review':'pending','browser_review':'pending','forced_word_alignment':'NOT_RUN; supplied source timing remapped and actual audio protected'}
(Q/'ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n');(OUT/'delivery-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
