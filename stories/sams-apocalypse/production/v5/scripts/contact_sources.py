from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,math
P=Path(__file__).resolve().parents[1]
T=json.loads((P/'timeline.json').read_text())
for page in range(math.ceil(len(T['jobs'])/12)):
    out=Image.new('RGB',(1440,1200),'#141a21');draw=ImageDraw.Draw(out)
    for i,j in enumerate(T['jobs'][page*12:(page+1)*12]):
        x=i%3*480;y=i//3*300;f=P/j['path']
        if f.exists():
            with Image.open(f) as im:out.paste(ImageOps.fit(im.convert('RGB'),(480,270)),(x,y))
        else:draw.text((x+20,y+100),'PENDING',fill='red')
        draw.text((x+8,y+275),j['id'],fill='white')
    out.save(P/'qa'/f'source-{page+1:02d}.jpg')
print('Source galleries updated')
