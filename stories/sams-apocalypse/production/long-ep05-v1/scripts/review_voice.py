from pathlib import Path
import difflib,json,wave
import numpy as np
from faster_whisper import WhisperModel
from pypinyin import lazy_pinyin
P=Path(__file__).resolve().parents[1]
def norm(s):return ''.join(lazy_pinyin(''.join(c for c in s if c.isalnum())))
allrows=json.loads((P/'qa/voice-asr.json').read_text())
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
reviews=[]
for row in allrows:
    if row['status']!='REVIEW':continue
    with wave.open(str(P/'audio/final'/(row['id']+'.wav'))) as w:
        audio=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)[::3]/32768
    tries=[]
    for beam in [1,3]:
        seg,_=model.transcribe(audio,language='zh',beam_size=beam,condition_on_previous_text=False,max_new_tokens=64)
        heard=''.join(x.text for x in seg);ratio=difflib.SequenceMatcher(None,norm(row['source']),norm(heard),autojunk=False).ratio()
        tries.append(dict(beam=beam,asr=heard,phonetic_similarity=ratio))
    reviews.append(dict(id=row['id'],source=row['source'],original_asr=row['asr'],rechecks=tries,status='RESOLVED_ASR_FALSE_POSITIVE' if max(x['phonetic_similarity'] for x in tries)>=.8 else 'UNRESOLVED'))
out=dict(total_checked=len(allrows),flagged=len(reviews),rechecks=reviews,unresolved=[x['id'] for x in reviews if x['status']=='UNRESOLVED'],full_human_listen='NOT_RUN')
(P/'qa/voice-asr-review-resolved.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False),flush=True)
