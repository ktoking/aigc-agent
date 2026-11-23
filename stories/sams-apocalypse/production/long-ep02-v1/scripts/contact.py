from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
P=Path(__file__).resolve().parents[1]
(P/'qa').mkdir(exist_ok=True)
for page in range(6):
    sheet=Image.new('RGB',(1536,4*310),(26,29,33));draw=ImageDraw.Draw(sheet)
    for slot in range(12):
        sid=page*12+slot+1;path=P/'assets'/f's{sid:02d}.png'
        corrected=path.with_stem(path.stem+'-v2')
        if corrected.exists():path=corrected
        x=(slot%3)*512;y=(slot//3)*310
        if path.exists():
            with Image.open(path) as im:sheet.paste(ImageOps.fit(im.convert('RGB'),(512,288)),(x,y))
        draw.text((x+8,y+291),f'SHOT {sid:02d} - {path.name if path.exists() else "PENDING"}',fill='white')
    sheet.save(P/'qa'/f'contact-{page+1:02d}.jpg',quality=88)
print(len(list((P/'assets').glob('*.png'))),'images on disk')
