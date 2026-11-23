from pathlib import Path
import json,wave,time,re,difflib
import numpy as np
from faster_whisper import WhisperModel
from pypinyin import lazy_pinyin
P=Path(__file__).resolve().parents[1];plan=json.loads((P/'voice-plan.json').read_text())
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
out=P/'qa/voice-asr.json';results=json.loads(out.read_text()) if out.exists() else []
seen={x['id'] for x in results}
def normalized(s):return ''.join(lazy_pinyin(''.join(c for c in s if c.isalnum())))
while len(seen)<len(plan):
    progress=False
    for c in plan:
        if c['id'] in seen:continue
        p=P/'audio/final'/(c['id']+'.wav')
        if not p.exists() or not p.with_suffix('.json').exists():continue
        with wave.open(str(p)) as w:
            assert w.getframerate()==48000
            audio=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)[::3]/32768
        segments,info=model.transcribe(audio,language='zh',beam_size=5,condition_on_previous_text=False,initial_prompt='许棠，山姆，霰弹枪，收货亭，机房。',max_new_tokens=128)
        heard=''.join(s.text for s in segments)
        ratio=difflib.SequenceMatcher(None,normalized(c['source_text']),normalized(heard),autojunk=False).ratio()
        results.append(dict(id=c['id'],source=c['source_text'],asr=heard,phonetic_similarity=ratio,status='REVIEW' if ratio<.8 else 'MATCHED_PHONETICALLY'))
        seen.add(c['id']);progress=True
        out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
        if len(seen)%24==0:print(f'ASR checked {len(seen)}/{len(plan)}',flush=True)
    if not progress:time.sleep(2)
review=[x for x in results if x['status']=='REVIEW']
(P/'qa/voice-asr-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(checked=len(results),review=len(review),limitations='Whisper phonetic comparison is automated, not a full human listening review'),ensure_ascii=False),flush=True)
