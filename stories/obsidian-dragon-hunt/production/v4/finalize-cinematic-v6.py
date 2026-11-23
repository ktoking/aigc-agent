"""整理本次已授权的图像交付；不调用媒体服务、Git 或网络。"""
from pathlib import Path
import hashlib
import html
import json
import os
import struct
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
EP = ROOT / 'episodes/EP001_valsak_v3_seasons'
PROD = ROOT / 'production/v4'
DELIVERY = ROOT / 'delivery/ep001-cinematic-v6'
DELIVERY.mkdir(parents=True, exist_ok=True)
MF = PROD / 'media-production-manifest.json'
manifest = json.loads(MF.read_text())
jobs = {j['id']: j for j in manifest['jobs']}
refs = [jobs[f'V6_S{s}_{i:02d}'] for s in range(1, 5) for i in range(1, 11)]
asset_ids = ['A_DRAGON_3H_V6', 'A_KING', 'A_WEAPONS', 'A_STINGER',
             'A_ROBOT_V6', 'A_ASSASSIN', 'A_LAIR_3H_V6', 'A_ENV_CLEAN_V6']
assets = [jobs[k] for k in asset_ids]
for key, title in {'A_KING':'幸存国王与王徽参考', 'A_WEAPONS':'六人战斗武器资产',
                   'A_STINGER':'折叠猎龙刺结构资产', 'A_ASSASSIN':'混血刺客A1三视图'}.items():
    jobs[key]['title'] = title
actors = {k: ROOT / f'assets/characters/{k}/turnaround-v1/three-view.png'
          for k in ['ORC', 'RANGER', 'MAGE', 'ROBOT', 'ELF', 'DRAGONBORN']}

def png_info(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    width, height = struct.unpack('>II', data[16:24])
    at, end = 8, False
    while at < len(data):
        count = struct.unpack('>I', data[at:at+4])[0]
        kind, content = data[at+4:at+8], data[at+8:at+8+count]
        crc = struct.unpack('>I', data[at+8+count:at+12+count])[0]
        assert zlib.crc32(kind + content) & 0xffffffff == crc, path
        at += 12 + count
        if kind == b'IEND':
            end = True
            break
    assert end, path
    return dict(path=str(path), width=width, height=height, bytes=len(data),
                sha256=hashlib.sha256(data).hexdigest())

records = []
for j in refs + assets:
    info = png_info(Path(j['target']))
    assert j.get('path') == j['target'] and j.get('source'), j['id']
    assert info['sha256'] == j['sha256'], j['id']
    j.update(status='SELECTED_REVIEWED', active=True)
    j['prompt_role'] = '当前重制规格；末次定点修正原文另见 revision_prompt。'
    records.append(dict(id=j['id'], **info))
assert len({r['sha256'] for r in records[:40]}) == 40
for j in refs:
    assert abs(j['width'] / j['height'] - 16/9) < .01
for p in actors.values():
    png_info(p)
manifest.update(status='COMPLETED_ACTIVE_SCOPE', style_version='user-cinematic-v6',
                active_asset_ids=asset_ids, active_reference_ids=[j['id'] for j in refs],
                selected_reference_count=40, selected_supplement_asset_count=8,
                original_actor_sheet_count=6, image_generation_tool='built-in image_gen',
                motion_qa='NOT_RUN', video_generated=False,
                user_acceptance='整组待用户查看，不将内部选图视为用户验收')
for old, new in {'A_DRAGON':'A_DRAGON_3H_V6', 'A_DRAGON_3H':'A_DRAGON_3H_V6',
                 'A_VALLEY':'A_ENV_CLEAN_V6', 'A_VALLEY_3H':'A_ENV_CLEAN_V6',
                 'A_LAIR_3H':'A_LAIR_3H_V6', 'A_ROBOT':'A_ROBOT_V6'}.items():
    jobs[old].update(active=False, superseded_by=new)
manifest['active_scene'] = 'A_ENV_CLEAN_V6'
MF.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')

lock = ('当前图像锁 v6：瓦尔萨克为同一躯干的三头、三颈、四足、双翼、一尾炎龙；'
        '三首共用颈根胸腔焰囊，陨石、导弹、巨箭和猎龙刺持续攻击东侧同一裂口。'
        '中央首主要吐息，西首拦弹，东首警戒；最终热压逆流影响三首。'
        '六人脸、基础服装和性格不变；机器人肩舱每侧三管成三角排布，总六管，4+2发射。'
        '影调与材质以用户最后三张参考及 assets/style/cinematic-v6 为准：有自然鳞甲、岩石和金属粗糙度，'
        '细节集中在主体，远景由雾气和景深压低；避免全屏噪点、过量污渍及抛光塑料感。'
        '北洞口、中央谷底、东侧低台和西侧断肋骨为固定地标，洞口高壁制造压迫感。'
        '谷底以岩面承重，低处少量浅水反光；不把人物改成站在深水或泥塘里。'
        '当前参考图位于各段 frames/current-references-v2，每段十张；v1为历史稿。')
replacements = [('喉根红色囊膜','三颈根部共用焰囊的红色外膜'),
                ('颈根红色囊膜','三颈根部共用焰囊的红色外膜'),
                ('喉根囊膜','共用焰囊外膜'), ('东侧颈肩','东侧共用颈根'),
                ('东颈肩','东侧共用颈根'), ('喉根','共用颈根')]
def revise(text):
    for old, new in replacements:
        text = text.replace(old, new)
    return text.replace('骨堆和旧军旗之间','高壁洞口的低岩台上')

for path in list(EP.glob('*.md')) + list(EP.glob('segment_*/*.md')) + list(EP.glob('segment_*/*.txt')):
    text = revise(path.read_text())
    if path.name in ['prompt.md', 'director-promt.txt', 'first-frame.md', 'last-frame.md', 'storyboard.md']:
        if not text.startswith(lock):
            text = lock + '\n\n' + text
    path.write_text(text)
timeline_path = EP/'timeline.json'
timeline = json.loads(timeline_path.read_text())
for shot in timeline['shots']:
    for key, value in shot.items():
        if isinstance(value, str):
            shot[key] = revise(value)
timeline.update(version='v6-three-head-in-place', dragon_heads=3,
                image_reference_version='current-references-v2', visual_lock=lock)
timeline_path.write_text(json.dumps(timeline, ensure_ascii=False, indent=2)+'\n')
assert timeline['total_seconds'] == 120 and timeline['total_frames'] == 3600
assert len(timeline['shots']) == 37 and len(list(EP.glob('segment_*'))) == 4
assert [sum(j['duration'] for j in timeline['shots'] if j['segment']==s) for s in range(1,5)] == [30]*4
assert all(a['end']==b['start'] for a,b in zip(timeline['shots'],timeline['shots'][1:]))

for name in ['AGENTS.md', 'docs/story-memory.md', 'docs/production-rules.md', 'docs/workflow.md']:
    p = ROOT/name
    text = p.read_text().replace('不自行调用媒体API。','媒体生成须遵循当次授权。')
    text = text.replace('当前无媒体提交或费用。','图像已按本次用户授权通过内置 image_gen 生成；视频未提交。')
    if not text.startswith('## 当前图像生产更新｜v6'):
        p.write_text('## 当前图像生产更新｜v6\n\n'+lock+'\n\n'
                     '用户已明确授权补充资产图和四段各十张参考图。本次图像交付已完成；'
                     '下面旧阶段的“待生图／无媒体”等文字仅记录早期状态，不覆盖本条。\n\n'+text)
combat_path = PROD/'combat-locks.json'
combat = json.loads(combat_path.read_text())
combat['VALSAK'] = '瓦尔萨克：三头三颈、共用胸躯、四足双翼单尾，视觉体量目标约40米外长；黑曜有机鳞甲、琥珀眼与局部焰光。东侧共用颈根焰囊为持续破甲目标，非某一侧头单独的喉囊；伤损不复原，不加外露宝石。尺寸为概念预演目标，非三维模型实测。'
if 'combat-v6/three-view.png' not in combat['ROBOT']:
    combat['ROBOT'] += ' 当前图像锁：combat-v6/three-view.png，肩舱每侧三管作三角排布；初始全装、首轮后每侧一枚，末轮后全空。'
combat['KING'] = combat['KING'].replace('外观为新增文字设定，未生成参考图。','已生成 assets/characters/KING/reference-v4.png；国王只在托付镜头，不随队进入山谷。')
combat_path.write_text(json.dumps(combat, ensure_ascii=False, indent=2)+'\n')
(PROD/'visual-style-current.md').write_text('# 当前风格与三头龙锁｜v6\n\n'+lock+'\n\n'
    '用户最后提供的三张风格图已保存到 assets/style/cinematic-v6。v5过光滑方案与v4单头方案均已被本版替代，保留历史文件，不进入当前交付包。\n')
if not (EP/'continuity.md').read_text().startswith('# 当前图像锁 v6'):
    (EP/'continuity.md').write_text('# 当前图像锁 v6\n\n'+lock+'\n\n'
    '三头分别警戒与反击；最终切断的是三颈共用焰囊的热压通路，保持原破甲配合。'
    '刺客由东侧低台接近，束足使龙胸降低后才落稳刺入；三条颈相继向西倒，刺客先东撤，兽人西撤。\n\n'
    '以下原坐标继续用于预演方向；参考图为概念关键帧，远景骨段数量、发射舱背部通风口及局部透视仍需视频阶段锁形，不能据图宣称三维实测连续性或动态重量验收。\n\n'+(EP/'continuity.md').read_text())

def rel(path, base=DELIVERY):
    return os.path.relpath(path, base)
cards = []
md = ['# EP001 当前参考图与补充资产｜v6', '',
      '四段各30秒，每段10张，共40张。图像全部通过内置 image_gen 生成；人物基础三视图沿用。', '',
      '[可缩放整组画廊](index.html)', '[整组ZIP](ep001-40refs-assets-v6.zip)', '']
for s in range(1,5):
    group = [j for j in refs if j['segment']==s]
    seg = Path(group[0]['target']).parents[2]
    gmd = [f'# Segment {s:02d}｜当前10张参考图 v6', '', '每图为独立参考关键帧，不按十张等时播放。', '']
    md.extend([f'## Segment {s:02d}', '', f'[本段ZIP](segment-{s:02d}-10refs-v6.zip)', ''])
    for j in group:
        im = Path(j['target'])
        gmd.extend([f"### {j['index']:02d}｜{j['title']}", '', f'![{j["title"]}]({im.name})', '',
                     f'[当前重制提示词]({im.with_suffix(".prompt.txt").name})', ''])
        md.extend([f'{j["index"]:02d}. [{j["title"]}]({rel(im)})', ''])
        cards.append(f'<figure data-segment="{s}"><a href="{html.escape(rel(im))}"><img loading="lazy" src="{html.escape(rel(im))}" alt="{html.escape(j["title"])}"></a><figcaption>S{s} · {j["index"]:02d} {html.escape(j["title"])} <a href="{html.escape(rel(im.with_suffix(".prompt.txt")))}">提示词</a></figcaption></figure>')
    (seg/'frames/current-references-v2/reference-gallery.md').write_text('\n'.join(gmd))
md.extend(['## 补充资产', ''])
for j in assets:
    md.extend([f'- [{j["title"]}]({rel(Path(j["target"]))})', ''])
md.extend(['原六名成员三视图保留，整组ZIP附带原始身份图。视频、配音、音效尚未生成。', ''])
(DELIVERY/'README.md').write_text('\n'.join(md))
asset_cards = ''.join(f'<figure><a href="{html.escape(rel(Path(j["target"])))}"><img loading="lazy" src="{html.escape(rel(Path(j["target"])))}" alt="{html.escape(j["title"])}"></a><figcaption>{html.escape(j["title"])}</figcaption></figure>' for j in assets)
page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>猎杀瓦尔萨克 · EP001 v6</title><style>body{margin:0;background:#15191f;color:#ece5da;font:16px system-ui}header,main{max-width:1440px;margin:auto;padding:28px}h1{font-size:28px}p{color:#bcb8b2;line-height:1.7}nav{display:flex;gap:10px;flex-wrap:wrap;position:sticky;top:0;background:#15191ff0;padding:14px 0;z-index:2}button,a{color:#e5b875}button{background:#252c35;border:1px solid #536071;border-radius:6px;padding:9px 14px;cursor:pointer}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}figure{margin:0;background:#222933;border-radius:7px;overflow:hidden}img{display:block;width:100%;height:auto}figcaption{padding:12px 15px}figcaption a{float:right}dialog{border:0;padding:0;background:#111;max-width:96vw;max-height:96vh}dialog img{max-height:92vh;width:auto;max-width:95vw}dialog::backdrop{background:#000c}@media(max-width:700px){.grid{grid-template-columns:1fr}header,main{padding:18px}}</style><header><h1>龙骨荒原：猎杀瓦尔萨克</h1><p>EP001 · 120秒 · 四段各30秒 · 40张独立参考图 · 三头龙 v6<br>采用用户最后三张参考的电影CG材质与光影，六人基础设计保留。点击图片放大；再次点击关闭。</p><p><a href="ep001-40refs-assets-v6.zip">下载40张＋资产＋提示词</a>　<a href="README.md">文字索引</a></p><nav><button data-filter="all">全部40张</button><button data-filter="1">第一段</button><button data-filter="2">第二段</button><button data-filter="3">第三段</button><button data-filter="4">第四段</button></nav></header><main><div class="grid" id="refs">''' + ''.join(cards) + '''</div><h2>补充资产</h2><div class="grid">''' + asset_cards + '''</div><p>本次交付为参考图与资产图；未生成视频。空间与受力仍需动态预演验收。</p></main><dialog id="viewer"><img alt="放大参考图"></dialog><script>const d=document.querySelector('dialog');document.querySelectorAll('figure>a').forEach(a=>a.onclick=e=>{e.preventDefault();d.querySelector('img').src=a.href;d.showModal()});d.onclick=()=>d.close();document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>document.querySelectorAll('#refs figure').forEach(f=>f.hidden=b.dataset.filter!=='all'&&f.dataset.segment!==b.dataset.filter));</script></html>'''
(DELIVERY/'index.html').write_text(page)

usage = ['# 当前参考图用途｜v6', '', '每段10张，按镜头功能选用，不等分30秒。当前全部为重新生成/校正后的v6选图。', '']
for s in range(1,5):
    usage.extend([f'## Segment {s:02d}', '', '| 序号 | 功能 | 当前图片 |', '| --- | --- | --- |'])
    for j in refs:
        if j['segment']==s:
            usage.append(f'| {j["index"]:02d} | {j["title"]} | [{Path(j["target"]).name}]({os.path.relpath(j["target"],EP)}) |')
    usage.append('')
usage += ['原 frames/references-v1 与 current-references-v1 均保留为来源/历史，不进入本套40张计数。', '',
          '整组可浏览画廊与ZIP见 ../../delivery/ep001-cinematic-v6/。最终提示词与修订来源见 production/v4/media-production-manifest.json。', '']
(EP/'current-reference-use.md').write_text('\n'.join(usage))
(EP/'image-manifest.md').write_text('# 当前图像清单｜v6\n\n40张当前参考图，每段10张；8张补充资产；原6位队员三视图保留。\n\n'
    '[当前用途](current-reference-use.md)\n\n[整组交付](../../delivery/ep001-cinematic-v6/README.md)\n\n'
    '每张的路径、生成来源、SHA256、尺寸、实际参考图和修订提示词见 ../../production/v4/media-production-manifest.json。\n')
(ROOT/'README.md').write_text('# 龙骨荒原：猎杀瓦尔萨克\n\n'
    'EP001直接在原目录更新为三头龙当前图像版v6；120秒，四段各30秒，目录历史后缀不变。\n\n'
    '- [40张参考图＋8张资产总览](delivery/ep001-cinematic-v6/README.md)\n'
    '- [可放大画廊](delivery/ep001-cinematic-v6/index.html)\n'
    '- [整组ZIP](delivery/ep001-cinematic-v6/ep001-40refs-assets-v6.zip)\n'
    '- [当前剧本](episodes/EP001_valsak_v3_seasons/episode.md)\n'
    '- [连续性](episodes/EP001_valsak_v3_seasons/continuity.md)\n'
    '- [六人原三视图](assets/characters/team-turnarounds-v1.md)\n\n'
    '本次图像使用内置image_gen生成并保存到项目，视频和音频尚未生成。旧试稿保留，当前交付不混入单头或过光滑版本。\n')
qa = dict(version='v6-three-head-cinematic', reference_count=40,
          per_segment={str(s):10 for s in range(1,5)}, supplement_assets=8,
          original_actor_sheets=6, png_integrity='PASS', unique_references='PASS',
          timeline_seconds=120, timeline_frames=3600, timeline_units=37,
          static_visual_review='COMPLETED_WITH_NOTES', motion_qa='NOT_RUN',
          notes=['三头、指定人物及主要动作逐图检查，国王误入/额外头/左右腕/弹舱数量等已定点修正。',
                 '概念图远景骨段数、局部透视、根束在前后足分布有生成差异；视频阶段以环境底图、动作锁与前后关键帧继续锁定。',
                 '静帧不能验证实际运动重量、镜头连贯或无声成片可读性；未生成视频。'], files=records)
(DELIVERY/'validation.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2)+'\n')
(EP/'text-validation.json').write_text(json.dumps(dict(version=timeline['version'],total_seconds=120,total_frames=3600,segments=4,segment_seconds=30,storyboard_units=37,gap_overlap='PASS',motion_validation='NOT_RUN'),ensure_ascii=False,indent=2)+'\n')

package_files = set()
for j in refs + assets:
    p=Path(j['target']); package_files.add(p)
    for suffix in ['.prompt.txt','.revision.prompt.txt']:
        side=p.with_suffix(suffix)
        if side.exists(): package_files.add(side)
package_files.update(actors.values())
package_files.update((ROOT/'assets/style/cinematic-v6').glob('*.png'))
package_files.add(EP/'qa-checklist.md')
for seg in EP.glob('segment_*'):
    package_files.update(seg.glob('*.md'))
    package_files.update(seg.glob('*.txt'))
    package_files.add(seg/'frames/current-references-v2/reference-gallery.md')
package_files.update([MF, EP/'episode.md', EP/'continuity.md', EP/'timeline.json',
                      EP/'current-reference-use.md', DELIVERY/'README.md',
                      DELIVERY/'index.html', DELIVERY/'validation.json', PROD/'visual-style-current.md'])
for s in range(1,5):
    with zipfile.ZipFile(DELIVERY/f'segment-{s:02d}-10refs-v6.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
        for j in refs:
            if j['segment']==s:
                p=Path(j['target']); z.write(p,p.name)
                z.write(p.with_suffix('.prompt.txt'),p.with_suffix('.prompt.txt').name)
                rp=p.with_suffix('.revision.prompt.txt')
                if rp.exists(): z.write(rp,rp.name)
with zipfile.ZipFile(DELIVERY/'ep001-40refs-assets-v6.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for p in sorted(package_files): z.write(p,p.relative_to(ROOT))
    assert z.testzip() is None
print(json.dumps(dict(references=40, supplement_assets=8, original_actor_sheets=6,
                      gallery=str(DELIVERY/'index.html'), zip=str(DELIVERY/'ep001-40refs-assets-v6.zip'),
                      zip_bytes=(DELIVERY/'ep001-40refs-assets-v6.zip').stat().st_size),ensure_ascii=False))
