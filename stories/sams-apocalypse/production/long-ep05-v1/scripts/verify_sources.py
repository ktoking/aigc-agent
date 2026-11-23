from pathlib import Path
import json,hashlib,wave
from PIL import Image,ImageOps,ImageDraw
P=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
t=json.loads((P/'timeline.json').read_text());plan=json.loads((P/'voice-plan.json').read_text())
assert sha(P/'narration.txt')=='ceb4d6a639c083690dc221f74f182c8cffb6e600491e4c295156463ffde7e5ed'
assert len(t['cues'])==len(plan)==150
assert all(b['start_frame']-a['end_frame_exclusive']==3 for a,b in zip(t['cues'],t['cues'][1:]))
assert all(not any(k in c['display_text'] for k in ',，.。') for c in t['cues'])
for c in plan:
 m=json.loads((P/'audio/raw'/(c['id']+'.metadata.json')).read_text());r=m['request'];v=r['voice_setting']
 assert m['http_status']==200 and m['base_status_code']==0
 assert r['text']==c['source_text']
 assert r['model']=='speech-2.8-turbo' and v==dict(voice_id='Chinese (Mandarin)_Gentleman',emotion='calm',speed=1.2,vol=1.0,pitch=0)
with wave.open(str(P/'audio/narration.wav')) as w:
 assert w.getframerate()==48000 and w.getnframes()==t['frame_count']*1600
ss=t['shots'];assert len(ss)==113 and ss[0]['start_frame']==0 and ss[-1]['end_frame_exclusive']==t['frame_count']
assert all(a['end_frame_exclusive']==b['start_frame'] for a,b in zip(ss,ss[1:]))
assert all(120<=s['end_frame_exclusive']-s['start_frame']<=180 for s in ss)
assets=[];finaljobs=[]
for s in ss:
 f=P/s['asset'];g=json.loads(f.with_suffix('.generation.json').read_text())
 with Image.open(f) as im:
  size=im.size;assert abs(size[0]/size[1]-16/9)<.01
 for ref in g['args'].get('referenced_image_paths',[]):assert Path(ref).exists(),ref
 assets.append(dict(id=s['id'],path=s['asset'],sha256=sha(f),size=size,generated_source=g['source'],references=g['args'].get('referenced_image_paths',[])))
 (P/s['prompt_file']).write_text(json.dumps(g['args'],ensure_ascii=False,indent=2))
 finaljobs.append(dict(id=s['id'],args=g['args'],event=s['event']))
 s['selected_image_sha256']=sha(f)
assert len({a['sha256'] for a in assets})==113
(P/'timeline.json').write_text(json.dumps(t,ensure_ascii=False,indent=2))
(P/'shot-plan.json').write_text(json.dumps(ss,ensure_ascii=False,indent=2))
(P/'image-jobs-final.json').write_text(json.dumps(finaljobs,ensure_ascii=False,indent=2))
asr=json.loads((P/'qa/voice-asr.json').read_text());assert len(asr)==150 and not [r for r in asr if r['status']=='REVIEW']
for page in range((len(ss)+23)//24):
 sheet=Image.new('RGB',(1600,1500),'#202020');draw=ImageDraw.Draw(sheet)
 for i,s in enumerate(ss[page*24:(page+1)*24]):
  x=(i%4)*400;y=(i//4)*250
  with Image.open(P/s['asset']) as im:sheet.paste(ImageOps.fit(im.convert('RGB'),(396,223)),(x,y))
  draw.text((x+4,y+228),f"{s['id']}  {s['seconds']:.2f}s  {s['start_frame']/30:.2f}s",fill='white')
 sheet.save(P/f'qa/contact-{page+1}.jpg',quality=92)
report=dict(status='PASS',script='restored complete v2; exact SHA256',tts_cues=150,tts_requests='all actual provider success, exact source text, Gentleman1.2/calm',asr='150 phonetic matches; full human listening NOT_RUN',frames=t['frame_count'],seconds=t['duration_seconds'],shots=113,unique_image_hashes=113,shot_seconds=[min(s['seconds'] for s in ss),max(s['seconds'] for s in ss)],external_gap_frames=3,dissolve_frames=3,subtitles='burned; comma to space; full stop removed; no SRT/VTT',assets=assets,contact_visual_review='PENDING',render='PENDING')
(P/'qa/source-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='assets'},ensure_ascii=False))
