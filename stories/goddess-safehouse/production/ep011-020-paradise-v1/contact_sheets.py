from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,math,sys
P=Path(__file__).resolve().parent;R=P.parents[1]
q=json.loads((P/'image-queue.json').read_text());root=P/'contacts';root.mkdir(exist_ok=True)
eps=sys.argv[1:] or sorted(set(s['episode'] for s in q))
for eid in eps:
 rows=[s for s in q if s['episode']==eid and s.get('image_path')]
 if not rows:continue
 w,h=480,270;sheet=Image.new('RGB',(w*3,(h+28)*math.ceil(len(rows)/3)),(24,24,24));draw=ImageDraw.Draw(sheet)
 for i,s in enumerate(rows):
  with Image.open(R/s['image_path']) as im:sheet.paste(ImageOps.fit(im.convert('RGB'),(w,h)),((i%3)*w,(i//3)*(h+28)))
  draw.text(((i%3)*w+8,(i//3)*(h+28)+h+6),s['shot_id'],fill='white')
 out=root/f'{eid}.jpg';sheet.save(out,quality=92)
 print(json.dumps({'episode':eid,'images':len(rows),'path':str(out)},ensure_ascii=False))
