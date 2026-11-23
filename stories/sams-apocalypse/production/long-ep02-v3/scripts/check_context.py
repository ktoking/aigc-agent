from pathlib import Path
import json,wave,time,difflib
import numpy as np
from faster_whisper import WhisperModel
from pypinyin import lazy_pinyin
P=Path(__file__).resolve().parents[1];plan=json.loads((P/'voice-plan.json').read_text());out=P/'qa/asr-context-review.json'
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
results=json.loads(out.read_text()) if out.exists() else [];done={r['id'] for r in results}
def norm(s):return lazy_pinyin(''.join(x for x in s if x.isalnum()))
while True:
    f=P/'qa/voice-asr.json';all_rows=json.loads(f.read_text()) if f.exists() else []
    flags=[r for r in all_rows if r['status']=='REVIEW']
    for flag in flags:
        if flag['id'] in done:continue
        i=next(i for i,c in enumerate(plan) if c['id']==flag['id']);ns=plan[max(0,i-1):min(len(plan),i+2)]
        paths=[P/'audio/final'/(c['id']+'.wav') for c in ns]
        if not all(x.exists() and x.with_suffix('.json').exists() for x in paths):continue
        parts=[]
        for path in paths:
            with wave.open(str(path)) as w:a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)[::3]/32768
            if parts:parts.append(np.zeros(1600,np.float32))
            parts.append(a)
        heard=''.join(s.text for s in model.transcribe(np.concatenate(parts),language='zh',beam_size=5,condition_on_previous_text=False,initial_prompt='许棠，山姆，林岚，周强。')[0])
        source=''.join(c['source_text'] for c in ns);target=norm(flag['source']);tokens=norm(heard)
        best=max((difflib.SequenceMatcher(None,target,tokens[a:a+length],autojunk=False).ratio() for length in range(max(1,len(target)-2),len(target)+3) for a in range(max(1,len(tokens)-length+1))),default=0)
        row={'id':flag['id'],'source':flag['source'],'context_source':source,'context_asr':heard,'target_phonetic_best_similarity':best,'status':'CONTEXT_PHONETIC_MATCH' if best>=.9 else 'REVIEW','note':'Automated contextual recognition, not human listening.'}
        results.append(row);done.add(flag['id']);out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print(json.dumps(row,ensure_ascii=False),flush=True)
    if len(all_rows)==len(plan) and all(r['id'] in done for r in flags):break
    time.sleep(3)
print('Context ASR review finished',flush=True)
