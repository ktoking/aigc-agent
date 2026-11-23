"""联系表供逐集看图；--accept仅在实际看过之后显式调用。"""
from pathlib import Path
import argparse,fcntl,json,math
from PIL import Image,ImageDraw,ImageOps

R=Path(__file__).resolve().parents[1];V=R/'production/user-script-v2'
p=argparse.ArgumentParser();p.add_argument('episode');p.add_argument('--accept',action='store_true');a=p.parse_args()
q=json.loads((V/'image-queue-speed1p3.json').read_text());ss=[s for s in q if s['episode']==a.episode];assert all(s.get('image_path') for s in ss),'镜头未齐'
if not a.accept:
 w,h=480,270;sheet=Image.new('RGB',(w*4,(h+30)*math.ceil(len(ss)/4)),(22,24,28));draw=ImageDraw.Draw(sheet)
 for i,s in enumerate(ss):
  with Image.open(R/s['image_path']) as im:sheet.paste(ImageOps.fit(im.convert('RGB'),(w,h)),((i%4)*w,(i//4)*(h+30)))
  draw.text(((i%4)*w+10,(i//4)*(h+30)+h+5),s['shot_id'],fill='white')
 out=V/'release-speed1p3'/f'contact-{a.episode}.jpg';sheet.save(out,quality=92);print(out)
else:
 with (V/'.image-assets.lock').open('w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);ids={s['shot_id'] for s in ss}
  for path in [V/'image-queue.json',V/'image-queue-speed1p3.json',R/'episodes'/a.episode/'timeline-speed1p3.json']:
   j=json.loads(path.read_text());rows=j['shots'] if isinstance(j,dict) else j
   for s in rows:
    if s['shot_id'] in ids:s.update(visual_review='PASS_MODEL_CONTACT_SHEET_REVIEW',generation_status='VISUAL_REVIEW_PASS')
   path.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
  path=R/'assets/manifest.json';assets=json.loads(path.read_text())
  for s in assets:
   if s['asset_id'] in ids:s.update(status='PASS_MODEL_CONTACT_SHEET_REVIEW',selected_for_production=True)
  path.write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
 print(a.episode,len(ss),'shots reviewed; this is model image review, not user aesthetic acceptance')
