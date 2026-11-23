from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parents[1];O=P.parents[1]/'output/LONG-EP02-v2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
t=json.loads((P/'timeline.json').read_text());selected=[]
for s in t['shots']:
    f=P/s['asset'];revision=f.with_stem(f.stem+'-v2')
    if revision.exists():f=revision;s['asset']=str(f.relative_to(P))
    assert f.exists(),f
    meta=P/'references'/(f.stem+'-generation.json');assert meta.exists(),meta
    generation=json.loads(meta.read_text())
    selected.append(dict(id=s['id'],file=s['asset'],sha256=sha(f),generation=generation))
assert len(selected)==120 and len({s['sha256'] for s in selected})==120
old={x['sha256'] for x in json.loads((P.parent/'long-ep02-v1/selected-images.json').read_text())}
assert not ({s['sha256'] for s in selected}&old),'Reused previous delivered picture'
(P/'timeline.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
(P/'selected-images.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
O.mkdir(parents=True,exist_ok=True)
(O/'chapters.json').write_text(json.dumps(t['chapters'],ensure_ascii=False,indent=2)+'\n')
print(dict(selected_images=120,reused_previous_images=0,duration=t['duration_seconds'],min_shot_seconds=min(s['duration_frames'] for s in t['shots'])/30,max_shot_seconds=max(s['duration_frames'] for s in t['shots'])/30))
