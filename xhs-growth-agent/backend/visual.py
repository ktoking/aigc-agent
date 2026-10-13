"""原创中文信息卡：离线 HTML/CSS 渲染，无外部图片与字体请求。"""
from __future__ import annotations

import hashlib
import html
import os
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'minimal': ('#f4f1e9', '#162922', '#b9d979'),
    'magazine': ('#f3ece3', '#29251f', '#ef7c4c'),
    'technology': ('#16242c', '#f8f2e7', '#a8dfb0'),
    'data': ('#eaf0f4', '#142b45', '#ffc56b'),
    'travel': ('#f6f0e6', '#314d43', '#dca271'),
    'comparison': ('#ecece9', '#1f313a', '#7bb6b0'),
    'guide': ('#f8f0df', '#423b29', '#d7aa66'),
    'opinion': ('#efebe5', '#352826', '#d48373'),
    'lifestyle': ('#f4e9e5', '#3b3430', '#c5afa4'),
}


def _html(title: str, text: str, index: int, total: int, palette: tuple[str, str, str]) -> str:
    bg, ink, accent = palette
    headline = html.escape(title[:90])
    blocks = [html.escape(p.strip()) for p in text.split('\n') if p.strip()]
    body = ''.join(f'<p>{p}</p>' for p in blocks[:8])
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><style>
    *{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1440px;overflow:hidden;background:{bg};color:{ink};font-family:"PingFang SC","Heiti SC",sans-serif}}
    main{{padding:82px;position:relative;height:100%;display:flex;flex-direction:column}}
    header{{display:flex;justify-content:space-between;align-items:center;font-size:25px;font-weight:600;letter-spacing:3px;border-bottom:2px solid {ink}33;padding-bottom:26px}}
    .pill{{font-size:23px;letter-spacing:1px;background:{accent};color:#182a24;padding:13px 22px;border-radius:30px}}
    .issue{{margin:55px 0 25px;font-size:23px;letter-spacing:4px;opacity:.65}}
    h1{{font-size:{86 if index == 0 else 69}px;line-height:1.3;letter-spacing:-3px;margin:0 0 35px;font-weight:700;max-width:900px;word-break:break-all}}
    .rule{{width:105px;height:12px;background:{accent};margin:0 0 38px}}
    article{{font-size:{35 if index == 0 else 34}px;line-height:1.68;letter-spacing:.4px;flex:1;overflow:hidden}}
    p{{margin:0 0 26px;white-space:pre-wrap}}
    footer{{font-size:22px;line-height:1.55;display:flex;justify-content:space-between;border-top:2px solid {ink}33;padding-top:22px;opacity:.68}}
    </style><main><header><span>NOTEBOOK</span><span class="pill">分享随手记</span></header>
    <div class="issue">{'NOTES · 今天分享' if index == 0 else 'NOTES · 接着看'}</div>
    <h1>{headline}</h1><div class="rule"></div><article>{body}</article>
    <footer><span>分享随手记</span><span>{index + 1:02d} / {total:02d}</span></footer></main></html>'''


def render_article(article_id: str, title: str, cards: list, template: str = 'minimal') -> list[dict]:
    from playwright.sync_api import sync_playwright
    from PIL import Image

    safe_id = ''.join(c for c in article_id if c.isalnum() or c in '-_')
    if not safe_id or safe_id != article_id:
        raise ValueError('非法文章标识')
    data_root = Path(os.getenv('XHS_DATA_DIR', str(ROOT / 'data'))).resolve()
    destination = data_root / 'media' / safe_id / uuid4().hex[:12]
    destination.mkdir(parents=True, exist_ok=True)
    palette = PALETTES.get(template, PALETTES['minimal'])
    normalized = []
    for item in cards[:5]:
        if isinstance(item, dict):
            normalized.append((str(item.get('title', item.get('heading', '操作要点'))), str(item.get('body', item.get('text', item.get('content', ''))))))
        else:
            normalized.append(('操作要点', str(item)))
    if not normalized:
        normalized = [('先定义任务边界', '先给输入和验收标准，再开始执行。'), ('检查实际结果', '把成功日志与真正完成的结果分别核实。')]
    cover_subtitle = next((str(item['cover_subtitle']) for item in cards if isinstance(item, dict) and item.get('cover_subtitle')), '从一个具体场景开始\n把想说的事讲清楚')
    slides = [(title, cover_subtitle)] + normalized
    assets = []
    chrome = os.getenv('XHS_RENDER_BROWSER', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome if Path(chrome).exists() else None, headless=True)
        page = browser.new_page(viewport={'width':1080, 'height':1440}, device_scale_factor=1)
        try:
            for index, (heading, body) in enumerate(slides):
                markup = _html(heading, body, index, len(slides), palette)
                file = destination / f'{index + 1:02d}.png'
                page.set_content(markup, wait_until='load')
                page.evaluate('document.fonts.ready')
                overflow = page.evaluate('document.querySelector("article").scrollHeight > document.querySelector("article").clientHeight || document.querySelector("h1").getBoundingClientRect().bottom > 1100')
                if overflow:
                    page.add_style_tag(content='h1{font-size:58px!important}article{font-size:29px!important;line-height:1.55!important}p{margin-bottom:16px!important}')
                if page.evaluate('document.querySelector("article").scrollHeight > document.querySelector("article").clientHeight'):
                    raise ValueError('信息卡文字超出画布，请缩短内容或增加卡片')
                page.screenshot(path=str(file), animations='disabled')
                (destination / f'{index + 1:02d}.html').write_text(markup, encoding='utf-8')
                with Image.open(file) as image:
                    if image.size != (1080, 1440):
                        raise ValueError('图片尺寸错误')
                digest = hashlib.sha256(file.read_bytes()).hexdigest()
                assets.append({'id':uuid4().hex, 'url':'/media/' + str(file.relative_to(data_root / 'media')), 'path':str(file), 'sha256':digest,
                               'source':'本地原创 HTML/CSS 信息卡', 'license':'原创；仅使用本机中文字体渲染', 'template':template, 'width':1080, 'height':1440})
        finally:
            browser.close()
    return assets
