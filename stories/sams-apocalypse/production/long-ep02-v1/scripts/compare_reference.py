from pathlib import Path
import json,re,difflib,statistics
from zhconv import convert
P=Path(__file__).resolve().parents[1]
def norm(s):
    s=convert(s,'zh-cn')
    for a,b in [('12','十二'),('18','十八'),('10','十'),('8','八'),('6','六'),('4','四')]:s=s.replace(a,b)
    return ''.join(x for x in s if x.isalnum())
old=json.loads((P.parent/'v6/timeline.json').read_text())['cues']
asr=json.loads((P/'analysis/asr.json').read_text())
speech=[]
for seg in asr:
    for w in seg['words']:
        txt=norm(w['word'])
        for i,c in enumerate(txt): speech.append((c,w['start']+(w['end']-w['start'])*i/max(1,len(txt)),w['start']+(w['end']-w['start'])*(i+1)/max(1,len(txt))))
script=''.join(norm(c['text']) for c in old);heard=''.join(x[0] for x in speech)
mapping={}
matcher=difflib.SequenceMatcher(None,script,heard,autojunk=False)
for a,b,size in matcher.get_matching_blocks():
    for k in range(size):mapping[a+k]=b+k
rows=[];cursor=0
for c in old:
    txt=norm(c['text']);indices=[mapping[k] for k in range(cursor,cursor+len(txt)) if k in mapping]
    row=dict(index=c['index'],text=c['text'],srt_start=c['start_frame']/30,srt_end=c['end_frame_exclusive']/30,match_fraction=len(indices)/len(txt))
    if indices:
        row.update(asr_start=speech[min(indices)][1],asr_end=speech[max(indices)][2])
        row['start_delta']=row['srt_start']-row['asr_start'];row['end_delta']=row['srt_end']-row['asr_end']
    rows.append(row);cursor+=len(txt)
changes=[dict(op=op,old=script[a:b],asr=heard[c:d]) for op,a,b,c,d in matcher.get_opcodes() if op!='equal']
result=dict(method='Whisper word timestamps plus sequence alignment; ASR can misrecognize; not forced phoneme alignment',rows=rows,text_difference_candidates=changes)
(P/'analysis/timing-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps([x for x in rows if x.get('match_fraction',0)>.85 and (abs(x.get('end_delta',0))>.38 or abs(x.get('start_delta',0))>.38)],ensure_ascii=False,indent=2))
print('CONTENT CANDIDATES',json.dumps(changes,ensure_ascii=False))
