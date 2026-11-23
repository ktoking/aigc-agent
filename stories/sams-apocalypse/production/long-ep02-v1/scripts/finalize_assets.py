from pathlib import Path
import json,hashlib,shutil,zipfile
P=Path(__file__).resolve().parents[1]
O=P.parents[1]/'output/LONG-EP02-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=json.loads((P/'project.json').read_text());rows=json.loads((P/'storyboard.json').read_text())
selected=[]
for row in rows:
    sid='s'+row['id'];path=P/'assets'/f'{sid}.png'
    correction=path.with_stem(sid+'-v2')
    if correction.exists():path=correction
    if not path.exists():raise SystemExit(f'Missing {sid}')
    spec['assets'][sid]=str(path.relative_to(P))
    meta=P/'references'/f'{path.stem}-generation.json'
    if not meta.exists():raise SystemExit(f'Missing provenance {meta}')
    generation=json.loads(meta.read_text())
    selected.append(dict(id=sid,chapter=row['chapter'],scene=row['scene'],narration=row['text'],file=str(path.relative_to(P)),sha256=sha(path),generation=generation))
(P/'project.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
(P/'selected-images.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
O.mkdir(parents=True,exist_ok=True)
for file in ['script.md','narration.txt','selected-images.json','storyboard.tsv']:
    shutil.copy2(P/file,O/file)
shutil.copy2(P/'analysis/reference-findings.md',O/'reference-findings.md')
shutil.copy2(P/'references/plot-research.md',O/'plot-research.md')
with zipfile.ZipFile(O/'images-and-script.zip','w',compression=zipfile.ZIP_STORED) as z:
    for r in selected:z.write(P/r['file'],'images/'+r['id']+'.png')
    for file in ['script.md','narration.txt','selected-images.json','storyboard.tsv','brief.md']:
        z.write(P/file,file)
print(json.dumps(dict(selected_images=len(selected),output=str(O),archive_bytes=(O/'images-and-script.zip').stat().st_size)))
