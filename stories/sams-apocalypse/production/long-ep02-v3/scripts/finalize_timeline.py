from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parents[1]
t=json.loads((P/'timeline.json').read_text())
for c in t['cues']:
    meta=json.loads((P/'audio/raw'/(c['id']+'.metadata.json')).read_text())
    c['preset']=meta['preset'];c['actual_voice_setting']=meta['request']['voice_setting']
    c['display_text']=c['source_text'].translate(str.maketrans({'，':' ', ',':' ', '。':'', '.':''}))
    assert not any(x in c['display_text'] for x in ['，',',','。','.'])
t['caption_policy']='Comma converted to space, full stop removed; original narration text and TTS punctuation preserved.'
(P/'timeline.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
selected=json.loads((P/'selected-images.json').read_text())
assert len(selected)==120
for s,c in zip(t['shots'],selected):
    assert s['asset']==c['file']
    assert hashlib.sha256((P/s['asset']).read_bytes()).hexdigest()==c['sha256']
print({'captions_normalized':len(t['cues']),'images_verified':len(selected),'duration_seconds':t['duration_seconds']})
