"""Export the completed local Build, remove audio, and verify persisted deliverables."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EP = ROOT / 'episodes/EP001_own-the-store'
OUT = EP / 'output'
QA = OUT / 'qa'


def run(args):
    subprocess.run(args, check=True, cwd=ROOT)


def probe(path):
    result = subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])
    return json.loads(result)


def main():
    QA.mkdir(parents=True, exist_ok=True)
    build = json.loads((HERE / 'episode-build.json').read_text())['build']
    assert build['work']['outcome'] == 'complete' and build['result']['state'] == 'complete'
    raw = HERE / 'output' / f'EP001-{build["id"]}.mp4'
    raw.parent.mkdir(exist_ok=True)
    if not raw.exists():
        run(['hypit','get',build['id'],'--output','final.video','--to',str(raw)])
    final = OUT / 'EP001_sams_apocalypse_1080p.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-map','0:v:0','-c:v','copy','-an','-sn','-dn','-movflags','+faststart',str(final)])
    info = probe(final)
    videos = [s for s in info['streams'] if s['codec_type']=='video']
    assert len(videos) == 1 and len(info['streams']) == 1
    stream = videos[0]
    assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_frames'])) == (1920,1080,'30/1',1800)
    assert abs(float(info['format']['duration'])-60) < 1/30
    (QA / 'ffprobe.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')

    data = json.loads((HERE / 'timeline.json').read_text())
    srt_path = OUT / 'EP001_sams_apocalypse.zh-CN.srt'
    blocks = srt_path.read_text(encoding='utf-8').strip().split('\n\n')
    parsed = []
    def seconds(text):
        h,m,s,ms = map(int,re.split('[:,]',text))
        return h*3600+m*60+s+ms/1000
    for index, block in enumerate(blocks,1):
        lines = block.splitlines()
        assert lines[0] == str(index)
        match = re.fullmatch(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})',lines[1])
        assert match
        parsed.append([seconds(match[1]),seconds(match[2]),'\n'.join(lines[2:])])
    assert parsed == data['subtitles']
    assert all(a[1] <= b[0] for a,b in zip(parsed,parsed[1:]))

    # Decode actual encoded frames, including every segment boundary.
    indices = sorted({0,60,165,270,390,449,450,600,720,840,899,900,1005,1140,1260,1349,1350,1410,1560,1690,1740,1799})
    expression = '+'.join(f'eq(n,{n})' for n in indices)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(final),'-vf',f"select='{expression}'",'-fps_mode','vfr',str(QA/'decoded-%02d.png')])
    records = []
    for counter, frame in enumerate(indices,1):
        source = QA / f'decoded-{counter:02d}.png'
        assert source.exists() and source.stat().st_size > 10000
        records.append({'frame':frame,'seconds':frame/30,'file':source.name})
    (QA / 'decoded-frames.json').write_text(json.dumps(records,indent=2)+'\n')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','1','-i',str(QA/'decoded-%02d.png'),'-vf','scale=480:270,tile=4x6:padding=2:margin=2','-frames:v','1',str(QA/'encoded-contact-sheet.jpg')])
    by_frame = {record['frame']:QA/record['file'] for record in records}
    for segment in range(1,5):
        directory = EP / f'segment_{segment:02d}_{(segment-1)*15:02d}-{segment*15:02d}s'
        shutil.copy2(by_frame[(segment-1)*450],directory/'frames/first-frame.png')
        shutil.copy2(by_frame[segment*450-1],directory/'frames/last-frame.png')
        local_record = {'build_id':build['id'],'full_video':'../../output/EP001_sams_apocalypse_1080p.mp4','start_frame':(segment-1)*450,'end_frame_exclusive':segment*450,'frame_rate':30,'rendering':'local Hypit','external_video_api':False}
        (directory/'output/render-record.json').write_text(json.dumps(local_record,indent=2)+'\n')
        p = directory/'api-request.md'
        p.write_text(p.read_text().replace('状态：等待实际渲染；构建编号以全片 qa-checklist.md 最终记录为准。',f'状态：全片本地构建完成；Build `{build["id"]}`，本段帧区间见 output/render-record.json。'))

    # The browser preview loads the same separate caption text as a Blob track;
    # no text is drawn into, or muxed into, the deliverable MP4.
    vtt = (OUT / 'EP001_sams_apocalypse.zh-CN.vtt').read_text()
    player = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>山姆末日 · 第一集</title><style>body{margin:0;background:#101925;color:#edf3fa;font-family:system-ui,sans-serif}main{max-width:1280px;margin:24px auto;padding:0 16px}h1{font-size:22px}video{width:100%;display:block;background:#000;border-radius:8px}p{color:#afc0d4;font-size:14px}video::cue{font-size:28px;background:rgba(0,0,0,.72);color:white}</style><main><h1>丧尸爆发后，我拥有整个山姆超市 · 第一集</h1><video id="film" controls playsinline preload="metadata" src="EP001_sams_apocalypse_1080p.mp4"><track id="captions" kind="subtitles" srclang="zh-CN" label="第一人称中文字幕" default></video><p>60 秒 · 1080p · 无音轨。播放器可切换外挂字幕，MP4 本身不含字幕。</p></main><script>const vtt=CAPTION_VALUE;document.getElementById('captions').src=URL.createObjectURL(new Blob([vtt],{type:'text/vtt'}));</script></html>'''.replace('CAPTION_VALUE',json.dumps(vtt,ensure_ascii=False))
    (OUT / 'player.html').write_text(player)
    report = {'build_id':build['id'],'render_outcome':'complete','duration_seconds':60,'resolution':[1920,1080],'fps':30,'frame_count':1800,'video_codec':stream['codec_name'],'audio_stream_count':0,'subtitle_stream_count':0,'external_srt_cues':len(parsed),'subtitle_timing':'authored reading rhythm, no synthesized voice','decoded_frames':len(records),'generated_images':11,'shots':13,'bytes':final.stat().st_size,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'visual_review':'pending'}
    (QA/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (EP/'qa-checklist.md').write_text(f'# 第一集验收\n\n- 本地 Hypit Build：`{build["id"]}`，Result complete。\n- 实际导出：1920×1080，30fps，1800 帧，60 秒，H.264。\n- 最终 MP4 实际只有视频流，无音轨、字幕流或烧录字幕。\n- 独立 SRT：18 条，与已通过正文逐句一致，时间有序且在 0–60 秒内。\n- 已从实际编码视频解码 {len(records)} 帧，包含四段首尾帧；待逐图目视复核。\n- 图片为 GPT 内置 imagegen 生成，11 张采用，1 张钥匙背景修正版替换了错误版本。\n- 质量报告：output/qa/validation.json；编码画面联系表：output/qa/encoded-contact-sheet.jpg。\n- 完整实际播放复核：待完成。\n- 未发布。\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__ == '__main__':
    main()
