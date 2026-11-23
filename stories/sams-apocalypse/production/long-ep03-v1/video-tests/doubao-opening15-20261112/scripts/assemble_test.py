#!/usr/bin/env python3
"""Assemble only real generated clips; reuse complete original narration cues."""
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parents[1]
OUTPUT = ROOT / 'segment_01_00-15s/output'
QA = ROOT / 'qa'


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def stamp(seconds):
    value = round(seconds * 100)
    return f'{value//360000}:{value//6000%60:02d}:{value//100%60:02d}.{value%100:02d}'


def main():
    clips = [OUTPUT/'p001/attempt-05/official-original.mp4', OUTPUT/'p002/official-original.mp4', OUTPUT/'p003/official-original.mp4']
    required = [181/30, 182/30, 93/30]
    for path, duration in zip(clips, required):
        if not path.is_file():
            raise SystemExit(f'缺少实际生成视频：{path.name}；不使用静态图替代')
        metadata = probe(path)
        if float(metadata['format']['duration']) < duration:
            raise SystemExit('生成素材不足，不冻结画面或变速凑时长')
    timeline = json.loads((SOURCE/'timeline.json').read_text())
    cues = timeline['cues'][:4]
    assert cues[-1]['end_frame_exclusive']/30 == 11.8
    QA.mkdir(exist_ok=True)
    caption_file = QA/'test-captions.ass'
    header = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,PingFang SC,32,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,1,2,70,70,40,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    lines = [f"Dialogue: 0,{stamp(c['start_frame']/30)},{stamp(c['end_frame_exclusive']/30)},Default,,0,0,0,,{c['display_text']}" for c in cues]
    caption_file.write_text(header+'\n'.join(lines)+'\n')
    # This local FFmpeg has no libass filter. Draw only the captions as PNG
    # overlays; the moving picture always comes from the generated MP4s.
    font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 32)
    caption_images = []
    for cue in cues:
        layer = Image.new('RGBA', (1280,720), (0,0,0,0))
        draw = ImageDraw.Draw(layer)
        caption = cue['display_text']
        lines = [caption]
        if draw.textlength(caption,font=font) > 1080:
            choices = [(abs(draw.textlength(caption[:k],font=font)-draw.textlength(caption[k:],font=font)),k)
                       for k in range(1,len(caption))
                       if max(draw.textlength(caption[:k],font=font),draw.textlength(caption[k:],font=font)) <= 1080]
            assert choices, caption
            split = min(choices)[1]
            lines = [caption[:split],caption[split:]]
        y = 720-52-43*len(lines)
        for line in lines:
            width = draw.textlength(line,font=font)
            draw.text(((1280-width)/2,y),line,font=font,fill='white',stroke_width=2,stroke_fill='black')
            y += 43
        path = QA / f"caption-{cue['id']}.png"
        layer.save(path)
        caption_images.append(path)
    filters = [f'[{index}:v]fps=30,scale=1280:720,setsar=1,trim=end_frame={frames},setpts=PTS-STARTPTS[v{index}]' for index,frames in enumerate([181,182,93])]
    filters += [
        '[v0][v1]xfade=transition=fade:duration=0.1:offset=5.933333333[x1]',
        '[x1][v2]xfade=transition=fade:duration=0.1:offset=11.9,trim=duration=15,setpts=PTS-STARTPTS[visual]',
        '[3:a]atrim=end=11.8,asetpts=PTS-STARTPTS,apad,atrim=end=15[a]',
    ]
    previous = 'visual'
    for index,cue in enumerate(cues):
        target = 'v' if index == len(cues)-1 else f'captioned{index}'
        filters.append(f"[{previous}][{index+4}:v]overlay=0:0:enable='gte(n,{cue['start_frame']})*lt(n,{cue['end_frame_exclusive']})'[{target}]")
        previous = target
    output = OUTPUT/'video-test-15s.mp4'
    if output.exists():
        raise SystemExit('已有测试成片，未覆盖')
    command = ['ffmpeg','-v','error']
    for path in clips:
        command += ['-i',str(path)]
    command += ['-i',str(SOURCE/'audio/narration-premix.wav')]
    for path in caption_images:
        command += ['-loop','1','-framerate','30','-i',str(path)]
    command += ['-filter_complex',';'.join(filters),'-map','[v]','-map','[a]',
                '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k','-ar','48000','-t','15','-movflags','+faststart',str(output)]
    subprocess.run(command,check=True)
    result = probe(output)
    (QA/'final-ffprobe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
    video = next(stream for stream in result['streams'] if stream['codec_type']=='video')
    assert abs(float(result['format']['duration'])-15)<.05
    assert int(video['nb_frames'])==450
    summary = {'status':'RENDERED_AND_DECODED','video':str(output),'durationSeconds':float(result['format']['duration']),
        'width':video['width'],'height':video['height'],'frames':int(video['nb_frames']), 'presentationFps':30,'sourceFps':24,
        'sourceClips':[str(path) for path in clips],'originalNarrationCues':[cue['id'] for cue in cues],
        'narrationSpeedChanged':False,'narrationEndSeconds':11.8,'trailingNoNarrationSeconds':3.2,'watermarkProcessing':'none; official watermark retained',
        'independentSubtitleDelivery':False,'newTtsGenerated':False,'fullHumanPlayback':'NOT_RUN'}
    (QA/'final-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    main()
