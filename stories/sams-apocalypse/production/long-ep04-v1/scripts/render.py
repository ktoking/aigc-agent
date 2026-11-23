from pathlib import Path
import argparse,json,wave,subprocess,hashlib,jieba
from functools import lru_cache
from PIL import Image,ImageOps,ImageDraw,ImageFont
P=Path(__file__).resolve().parents[1];O=P.parents[1]/'output/LONG-EP04-v1'
W,H,FPS=1920,1080,30
FONT=ImageFont.truetype('/System/Library/Fonts/PingFang.ttc',48)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def preview(seconds):
    t=json.loads((P/'timeline.json').read_text())
    capframe=max(c['end_frame_exclusive'] for c in t['cues'] if c['end_frame_exclusive']<=seconds*30)
    t['frame_count']=capframe
    t['cues']=[c for c in t['cues'] if c['start_frame']<capframe]
    t['shots']=[dict(s,end_frame_exclusive=min(s['end_frame_exclusive'],capframe)) for s in t['shots'] if s['start_frame']<capframe]
    audio=P/'qa/preview-audio.wav'
    with wave.open(str(P/'audio/narration.wav')) as src, wave.open(str(audio),'wb') as out:
        out.setparams(src.getparams());out.writeframes(src.readframes(capframe*1600))
    return t,audio,P/'qa/opening-preview.mp4'
def caption(text):
    layer=Image.new('RGBA',(W,H),(0,0,0,0));draw=ImageDraw.Draw(layer)
    if not text:return layer
    if draw.textlength(text,font=FONT)<=1370:
        lines=[text]
    else:
        options=[]
        word_bounds=set(); cursor=0
        for token in jieba.cut(text,HMM=False):
            cursor+=len(token);word_bounds.add(cursor)
        for k in range(6,len(text)-5):
            if k not in word_bounds:continue
            left,right=text[:k],text[k:]
            wa,wb=draw.textlength(left,font=FONT),draw.textlength(right,font=FONT)
            if max(wa,wb)>1500:continue
            score=abs(wa-wb)-(180 if text[k-1] in '，、：； ' else 0)
            options.append((score,k))
        assert options,text
        k=min(options)[1];lines=[text[:k],text[k:]]
    assert len(lines)<=2,(text,lines)
    y=H-78-64*len(lines)
    for line in lines:
        width=draw.textlength(line,font=FONT);x=(W-width)/2
        draw.text((x,y),line,font=FONT,fill=(255,255,250,255),stroke_width=4,stroke_fill=(0,0,0,245))
        y+=64
    return layer
def render(t,audio,video):
    video.parent.mkdir(parents=True,exist_ok=True)
    assert not video.exists(),'Refuse to overwrite existing video'
    shots=t['shots'];cues=t['cues'];n=t['frame_count']
    paths={s['id']:P/s['asset'] for s in shots}
    for path in paths.values():assert path.exists(),path
    @lru_cache(maxsize=2)
    def picture(sid):
        with Image.open(paths[sid]) as im:return ImageOps.fit(im.convert('RGB'),(W,H),Image.Resampling.LANCZOS)
    cue_text={c['id']:c.get('display_text',c['source_text'].translate(str.maketrans({'，':' ', ',':' ', '。':'', '.':''}))) for c in cues}
    @lru_cache(maxsize=2)
    def cap(cid):return caption(cue_text[cid])
    boundaries={0,n}
    for c in cues:boundaries.update([c['start_frame'],c['end_frame_exclusive']])
    for s in shots[1:]:boundaries.update(range(max(0,s['start_frame']-3),s['start_frame']+1))
    boundaries=sorted(boundaries);ci=si=0;written=0
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','pipe:0','-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-tune','stillimage','-bf','0','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','1','-movflags','+faststart',str(video)]
    with video.with_suffix('.render.log').open('w') as log:
        enc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
        try:
            for a,b in zip(boundaries,boundaries[1:]):
                while si+1<len(shots) and a>=shots[si+1]['start_frame']:si+=1
                while ci<len(cues) and a>=cues[ci]['end_frame_exclusive']:ci+=1
                current=picture(shots[si]['id'])
                if si+1<len(shots) and a>=shots[si+1]['start_frame']-3:
                    alpha=(a-(shots[si+1]['start_frame']-3)+1)/3
                    current=Image.blend(current,picture(shots[si+1]['id']),alpha)
                if ci<len(cues) and cues[ci]['start_frame']<=a<cues[ci]['end_frame_exclusive']:
                    current=current.copy();current.paste(cap(cues[ci]['id']),(0,0),cap(cues[ci]['id']))
                raw=current.tobytes()
                for _ in range(b-a):enc.stdin.write(raw)
                written+=b-a
            enc.stdin.close()
            if enc.wait():raise RuntimeError('Encoder failed')
        except BaseException:
            if enc.poll() is None:enc.terminate();enc.wait()
            raise
    assert written==n
    return dict(video=str(video.resolve()),frames=n,duration_seconds=n/30,subtitles_burned=True,independent_subtitle_files=False,source_images=len(shots),voice_model='speech-2.8-turbo',voice_id='Chinese (Mandarin)_Gentleman',api_speed=1.2,post_audio_speed_change=False,caption_commas_as_spaces=True,caption_full_stops_removed=True,video_sha256=sha(video),audio_sha256=sha(audio),render_style='Fixed camera, image-only 3-frame dissolves, clear captions on separate layer')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preview-seconds',type=float);args=parser.parse_args()
    if args.preview_seconds:t,audio,video=preview(args.preview_seconds)
    else:t=json.loads((P/'timeline.json').read_text());audio=P/'audio/narration.wav';video=P/'qa/video-base.mp4'
    result=render(t,audio,video)
    video.with_suffix('.manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False),flush=True)
