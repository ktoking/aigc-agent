from pathlib import Path
import json,re,math
P=Path(__file__).resolve().parents[1]
rows=[]
for line in (P/'storyboard.tsv').read_text().splitlines():
    sid,chapter,roles,scene,text=line.split('\t')
    rows.append(dict(id=sid,chapter=chapter,roles=roles,scene=scene,text=text))
(P/'storyboard.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
parts=[]
for row in rows:
    sentences=re.findall(r'[^。！？]+[。！？]?',row['text'])
    for sentence in sentences:
        parts.append(dict(text=sentence,asset='s'+row['id'],chapter=row['chapter'],units=sum(c.isalnum() for c in sentence)))
# Use the accepted reference speed as a drafting range. Total length is an explicit user requirement.
# Allocate speech time to spoken units; no intro/outro holds or duplicated gap allowance.
budget=18000-3*(len(parts)-1)
units=sum(x['units'] for x in parts)
raw=[budget*x['units']/units for x in parts]
frames=[math.floor(x) for x in raw]
for i in sorted(range(len(parts)),key=lambda i:raw[i]-frames[i],reverse=True)[:budget-sum(frames)]:frames[i]+=1
episodes=[]
for x,n in zip(parts,frames):
    if not episodes or episodes[-1]['title']!=x['chapter']:
        episodes.append(dict(id='LONG-EP02-C'+x['chapter'].split()[0],title=x['chapter'],cues=[]))
    episodes[-1]['cues'].append(dict(text=x['text'],asset=x['asset'],duration_frames=n,timing_basis='text_estimate_calibrated_to_user_reference_10min_not_audio_aligned'))
spec=dict(name='山姆避难记·第二集：门外的人',fps=30,width=1920,height=1080,gap_seconds=.1,dissolve_seconds=.1,characters_per_second=units/(budget/30),assets={'s'+r['id']:'assets/s'+r['id']+'.png' for r in rows},episodes=episodes)
(P/'project.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
text='# 山姆避难记·第二集：门外的人\n\n接第一部八集合集；十分钟长篇续集，非旧短集EP002的替换。\n\n'
last=''
for r in rows:
    if last!=r['chapter']:text+='\n## '+r['chapter']+'\n\n';last=r['chapter']
    text+=r['text']+'\n\n'
(P/'script.md').write_text(text)
(P/'narration.txt').write_text('\n'.join(x['text'] for x in parts)+'\n')
print(json.dumps(dict(shots=len(rows),sentences=len(parts),units=units,speech_frames=budget,total_frames=sum(frames)+3*(len(parts)-1),duration=600,cps=spec['characters_per_second'],longest_sentence=max(len(x['text']) for x in parts)),ensure_ascii=False))
