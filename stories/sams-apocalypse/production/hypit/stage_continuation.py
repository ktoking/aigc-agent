from pathlib import Path
import json,shutil
from continue_series import ROOT,HERE,PLAN,episode,segdir
records=json.loads((HERE/'continuation-sources.json').read_text())
for j in PLAN:
 v=records.get(j['id'])
 if not v or v.get('status')!='accepted':continue
 d=segdir(episode(j['episode']),j['segment'])/'frames';d.mkdir(parents=True,exist_ok=True)
 target=d/f'{j["id"]}.png';source=Path(v['path'])
 if not target.exists() or target.read_bytes()!=source.read_bytes():shutil.copy2(source,target)
print('staged',sum(1 for j in PLAN if (segdir(episode(j['episode']),j['segment'])/'frames'/f'{j["id"]}.png').exists()))
