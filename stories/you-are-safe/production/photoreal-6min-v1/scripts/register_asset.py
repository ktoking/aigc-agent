from pathlib import Path
import json,sys,shutil,struct,hashlib,datetime
P=Path(__file__).resolve().parents[1]
ident,source=sys.argv[1:3];src=Path(source);dst=P/'assets'/f'{ident}.png'
if src.resolve()!=dst.resolve():shutil.copy2(src,dst)
raw=dst.read_bytes();w,h=struct.unpack('>II',raw[16:24])
req=next(x for x in json.loads((P/'image-requests.json').read_text()) if x['id']==ident)
metadata={'id':ident,'status':'GENERATED','method':'built-in image_gen','source':str(src),'path':str(dst),'width':w,'height':h,'sha256':hashlib.sha256(raw).hexdigest(),'prompt':req['prompt'],'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(P/'assets'/f'{ident}.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:metadata[k] for k in ['id','status','width','height']}))
