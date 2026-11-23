from pathlib import Path
import argparse, hashlib, json, shutil, struct

p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--source',required=True);p.add_argument('--args-json');a=p.parse_args()
P=Path(__file__).resolve().parents[1];src=Path(a.source);out=P/'assets'/(a.id+'.png')
assert src.exists(),src
args=json.loads(a.args_json) if a.args_json else json.loads((P/'prompts'/(a.id+'.json')).read_text())
if out.exists():
    assert hashlib.sha256(out.read_bytes()).digest()==hashlib.sha256(src.read_bytes()).digest(),'Refuse overwrite'
else:shutil.copy2(src,out)
data=out.read_bytes();width,height=struct.unpack('>II',data[16:24]);sha=hashlib.sha256(data).hexdigest()
for f in (P/'assets').glob('p*.generation.json'):
    if f.stem.split('.')[0]!=a.id:assert json.loads(f.read_text())['sha256']!=sha,'Image reused'
meta=dict(id=a.id,source=str(src),file=str(out.relative_to(P)),sha256=sha,width=width,height=height,builtin_imagegen=True,args=args)
out.with_suffix('.generation.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print(json.dumps(dict(id=a.id,width=width,height=height,saved=str(out),sha256=sha)))
