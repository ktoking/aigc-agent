"""Stage accepted GPT images and author the local Hypit film and detached captions."""
from pathlib import Path
import json
import re
import shutil
import struct
import xml.sax.saxutils as xml

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EP = ROOT / 'episodes/EP001_own-the-store'
DATA = json.loads((HERE / 'timeline.json').read_text())
SOURCES = json.loads((HERE / 'generated-sources.json').read_text())
SEGS = [EP / f'segment_{i:02d}_{(i-1)*15:02d}-{i*15:02d}s' for i in range(1, 5)]


def stamp(seconds, separator=','):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f'{hours:02d}:{minutes:02d}:{secs:02d}{separator}{milliseconds:03d}'


def narration_lines():
    draft = (ROOT / 'drafts/EP001-script-v1.md').read_text()
    blocks = re.findall(r'第一人称正文：\n\n(.*?)(?=\n## )', draft, re.S)
    return ''.join(''.join(block.split()) for block in blocks)


def main():
    for segment in SEGS:
        (segment / 'frames').mkdir(parents=True, exist_ok=True)
        (segment / 'output').mkdir(exist_ok=True)
    out = EP / 'output'
    out.mkdir(exist_ok=True)
    # The accepted wording is checked independently against the approved draft.
    assert narration_lines() == ''.join(''.join(c[2].split()) for c in DATA['subtitles'])
    previous = 0
    for start, end, _ in DATA['subtitles']:
        assert start >= previous and end > start and end <= DATA['duration']
        assert start * DATA['fps'] == round(start * DATA['fps'])
        assert end * DATA['fps'] == round(end * DATA['fps'])
        previous = end
    staged = {}
    for key, asset in DATA['assets'].items():
        source = Path(SOURCES[asset['source']]['path'])
        destination = SEGS[asset['segment'] - 1] / 'frames' / asset['file']
        if not destination.exists():
            shutil.copy2(source, destination)
        with destination.open('rb') as f:
            header = f.read(24)
        assert header[:8] == b'\x89PNG\r\n\x1a\n'
        width, height = struct.unpack('>II', header[16:24])
        staged[key] = {**asset, 'path': str(destination.relative_to(ROOT)), 'width': width, 'height': height}
    (EP / 'image-manifest.json').write_text(json.dumps(staged, ensure_ascii=False, indent=2) + '\n')

    srt = '\n\n'.join(f'{i}\n{stamp(start)} --> {stamp(end)}\n{text}' for i, (start, end, text) in enumerate(DATA['subtitles'], 1)) + '\n'
    (out / 'EP001_sams_apocalypse.zh-CN.srt').write_text(srt, encoding='utf-8')
    vtt = 'WEBVTT\n\n' + '\n\n'.join(f'{stamp(start,".")} --> {stamp(end,".")}\n{text}' for start, end, text in DATA['subtitles']) + '\n'
    (out / 'EP001_sams_apocalypse.zh-CN.vtt').write_text(vtt, encoding='utf-8')

    lines = ['<?svml using="@hypit/markup@1"?>', '<svml>']
    for alias, package in [('time','timeline-author'),('space','spatial'),('media','media'),('visual','visual-track'),('film','film'),('html','html-video')]:
        lines.append(f'  <import as="{alias}" from="@hypit/{package}@1"/>')
    lines += ['  <import as="look" source="./look.svs"/>', '  <time:Clock id="clock" frame-rate="30"/>', '  <time:Timeline id="program" clock={clock} end="60s">']
    for i, shot in enumerate(DATA['shots']):
        # A 6-frame overlap lets the incoming picture dissolve over the old shot.
        end = min(60, shot['end'] + (0.2 if i < len(DATA['shots']) - 1 else 0))
        lines.append(f'    <time:Window id="{shot["id"]}" from="{shot["start"]}s" until="{end}s"/>')
    lines += ['  </time:Timeline>', '  <space:Canvas id="canvas" width="1920" height="1080"/>']
    for key, asset in staged.items():
        lines += [f'  <space:Extent id="extent-{key}" width="{asset["width"]}" height="{asset["height"]}"/>', f'  <media:Image id="asset-{key}" src="../../{xml.escape(asset["path"])}"/>']
    for i, shot in enumerate(DATA['shots']):
        lines.append(f'  <visual:Motion id="motion-{shot["id"]}">')
        duration = min(60, shot['end'] + 0.2) - shot['start']
        for at, ratio, opacity in [('start',0,1 if i == 0 else 0),('6f',0.2/duration,1),('end',1,1)]:
            scale = shot['scale'][0] + (shot['scale'][1] - shot['scale'][0]) * ratio
            x = shot['x'][0] + (shot['x'][1] - shot['x'][0]) * ratio
            y = shot['y'][0] + (shot['y'][1] - shot['y'][0]) * ratio
            lines.append(f'    <visual:Pose at="{at}" scale="{scale:.6f}" x="{x:.4f}" y="{y:.4f}" origin-x="0.5" origin-y="0.5" opacity="{opacity}" easing="linear"/>')
        lines.append('  </visual:Motion>')
    lines.append('  <visual:Track id="picture" timeline={program.timeline}>')
    for i, shot in enumerate(DATA['shots']):
        key = shot['asset']
        lines.append(f'    <visual:Clip id="{shot["id"]}" image={{asset-{key}}} extent={{extent-{key}}} during={{program.{shot["id"]}}} frame={{canvas.bounds}} z="{i+1}" fit="cover" motion={{motion-{shot["id"]}}}/>')
    lines += ['  </visual:Track>', '  <film:Film id="main" canvas={canvas.canvas} timeline={program.timeline} appearance={look.film.main}>', '    <film:Track source={picture.visual}/>', '  </film:Film>', '  <html:Video id="final" composition={main.composition} timeline={program.timeline}/>', '</svml>']
    (HERE / 'episode.svml').write_text('\n'.join(lines) + '\n')
    (HERE / 'episode.svrun').write_text('<?svml using="@hypit/markup/run@1"?>\n<svrun version="1">\n  <author source="./episode.svml"/>\n  <target output="final.video"/>\n</svrun>\n')

    (EP / 'episode.md').write_text((ROOT / 'drafts/EP001-script-v1.md').read_text().replace('状态：供用户审阅的第一稿。暂按约 60 秒、四段安排；未用配音实测，也未锁定字幕时间。','状态：用户已通过剧本，正在制作。60 秒、四段；无配音，按阅读速度编排独立字幕。'))
    overview = ['# 第一集镜头表', '', '16:9，1920×1080，30fps，60秒；GPT 镜头图，本地运镜，独立字幕，无配音。', '', '| 镜头 | 时间 | 图片 | 画面与运镜 |', '| --- | --- | --- | --- |']
    for shot in DATA['shots']:
        overview.append(f'| {shot["id"]} | {shot["start"]}–{shot["end"]}s | {shot["asset"]} | {staged[shot["asset"]]["description"]}；缩放 {shot["scale"][0]}→{shot["scale"][1]}，水平位移 {shot["x"][0]}→{shot["x"][1]}px |')
    (EP / 'overview-storyboard.md').write_text('\n'.join(overview) + '\n')
    image_list = ['# 图像清单', '', '全部通过 GPT 内置 imagegen 生成。具体提示词和来源见 `../../production/hypit/generated-sources.json`。', '拒绝版本不进入播放；首尾帧将从实际渲染视频提取。', '']
    for key, asset in staged.items():
        image_list.append(f'- `{key}`：`{asset["path"]}`，{asset["width"]}×{asset["height"]}；{asset["description"]}。')
    (EP / 'image-manifest.md').write_text('\n'.join(image_list) + '\n')

    for number, segment in enumerate(SEGS, 1):
        start, end = (number - 1) * 15, number * 15
        shots = [s for s in DATA['shots'] if s['start'] < end and s['end'] > start]
        cues = [c for c in DATA['subtitles'] if c[0] < end and c[1] > start]
        rows = ['# 分段故事板', '', f'本段为全片 {start}–{end} 秒，使用漫画静帧与本地运镜，无声音。', '', '| 镜头 | 全片时间 | 素材 | 画面 |', '| --- | --- | --- | --- |']
        for s in shots:
            a = staged[s['asset']]
            rows.append(f'| {s["id"]} | {max(start,s["start"])}–{min(end,s["end"])}s | `{a["path"]}` | {a["description"]} |')
        rows += ['', '独立字幕：', ''] + [c[2].replace('\n','') for c in cues]
        (segment / 'storyboard.md').write_text('\n'.join(rows) + '\n')
        for label, s in [('first',shots[0]),('last',shots[-1])]:
            a = staged[s['asset']]
            (segment / f'{label}-frame.md').write_text(f'# {"首" if label=="first" else "尾"}帧\n\n以 `{a["path"]}` 为实际图片来源。\n画面：{a["description"]}。\n使用 `episode.svml` 中同名镜头的缩放与位置，从最终编码视频提取 `frames/{label}-frame.png`，不是重新生图。\n')
        instructions = f'16:9，1920×1080，30fps，15秒，清晰彩色漫画。\n本段使用本地 Hypit，不向视频 API 提交。\n主角锁定：圆头点眼、青绿色针织帽、芥末黄帽衫、海军蓝马甲、深灰裤。\n图片按 storyboard.md 顺序出现，主运镜为缓推、缓拉或小幅横移，相邻镜头用6帧叠化。具体数值与字幕时间以 ../../../production/hypit/timeline.json 为准。\n无配音、无背景音乐、无音效、无烧录字幕；第一人称文本仅输出独立 SRT。\n首尾帧以本段真实编码画面为连续性证据，不用首尾帧插值生成人物动作。\n禁止换服装、增添角色、手脚扭曲、生成文字、水印、黑边或资源无限补货。\n'
        (segment / 'prompt.md').write_text('# 本地运镜与合成指令\n\n' + instructions)
        (segment / 'director-promt.txt').write_text(instructions)
        (segment / 'api-request.md').write_text('# 本段执行记录\n\n- 平台：本地 Hypit 0.3.1 与 FFmpeg。\n- 视频生成 API：不适用，没有提交，不存在 API 任务 ID。\n- 图片来源：GPT 内置 imagegen，来源与提示词保存在 generated-sources.json。\n- 本地构建 Run：`production/hypit/episode.svrun`。\n- 状态：等待实际渲染；构建编号以全片 qa-checklist.md 最终记录为准。\n- 重试：保留既有图片；失败只修复本地编排或环境，再提交新的本地 Build，不重复生图。\n')
    (EP / 'continuity.md').write_text('# 连续性\n\n- 主角衣帽固定，夜晚与上午只改变光线。\n- 监控中店长被扑倒并未确认死亡；结尾保持健康状态不明，不添加丧尸红眼或伤口。\n- 店长棕色短发、黑框眼镜、白衬衫、蓝马甲、红挂绳；结尾在卷帘门外持两把银色钥匙。\n- 钥匙特写使用修正后的室外背景版本，拒绝原来错误的室内货架背景。\n- 监控室后半段复用前半段房间参考，床为新搬入的露营床。\n- 资源有限、当日上午冷库仍运转；没有长期供电或全店绝对安全的断言。\n- 片头购物车为当日上午，随后回忆昨夜，第三段回到清晨，第四段安家后发现来客。\n')
    (EP / 'publish-package.md').write_text('# 发布草案\n\n- 标题：丧尸爆发后，我拥有整个山姆超市｜第一集\n- 备选：昨天还在搬货，今天整个超市都是我的避难所\n- 备选：我刚在超市铺好床，店长就带着钥匙回来了\n- 封面：主角与满载购物车，身后高货架；使用片头原图，无额外图中文字。\n- 评论引导：如果是你，会给店长开门吗？\n- 标签方向：末日生存、漫画故事、囤货避难。\n- 状态：未发布。\n')
    print(json.dumps({'images':len(staged),'shots':len(DATA['shots']),'subtitles':len(DATA['subtitles']),'duration':DATA['duration'],'narration_matches_approved_script':True},ensure_ascii=False))


if __name__ == '__main__':
    main()
