"""单张中文封面：不同版式的离线 HTML/CSS，不请求外部图片或字体。"""
from __future__ import annotations

import hashlib
import html
import os
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
COVER_STYLES = ('bold', 'sticky', 'editorial', 'receipt', 'split', 'ink')
LEGACY = {'minimal': 'ink', 'magazine': 'editorial', 'technology': 'split', 'data': 'editorial',
          'travel': 'sticky', 'comparison': 'split', 'guide': 'receipt', 'opinion': 'bold', 'lifestyle': 'sticky'}


def cover_style(template, article_id, title):
    if template == 'auto':
        seed = int(hashlib.sha256((article_id + title).encode()).hexdigest()[:8], 16)
        return COVER_STYLES[seed % len(COVER_STYLES)]
    return LEGACY.get(template, template) if template in LEGACY or template in COVER_STYLES else 'ink'


def _html(title: str, subtitle: str, style: str) -> str:
    headline, hook = html.escape(title[:90]).replace('，', '<br>'), html.escape(subtitle[:30])
    widths = {'bold':900,'sticky':692,'editorial':910,'receipt':748,'split':916,'ink':900}
    sizes = {'bold':136,'sticky':105,'editorial':120,'receipt':99,'split':124,'ink':118}
    size = sizes[style]
    if '，' in title:
        longest=max(len(part) for part in title.split('，'))
        size=min(size,int(widths[style]/max(longest,1)*.96))
    heading=f'<h1 style="font-size:{size}px">{headline}</h1>'
    layouts = {
        'bold': '''body{background:#e34b30;color:#fff8e9}main{padding:110px 90px;justify-content:center}
            .label{font-size:30px;letter-spacing:8px;margin-bottom:65px}h1{font-size:136px;line-height:1.15;letter-spacing:-7px}
            .hook{font-size:40px;margin-top:70px;max-width:730px;border-top:4px solid currentColor;padding-top:30px}
            .accent{position:absolute;width:200px;height:200px;border:4px solid #fff8e9;right:-65px;top:60px;border-radius:50%}''',
        'sticky': '''body{background:#30413b;color:#26251f}main{padding:145px 88px;justify-content:center}
            .sheet{background:#f7df79;padding:100px 66px 85px;transform:rotate(-2deg);box-shadow:18px 24px 0 #18282244;position:relative}
            .sheet:before{content:"";position:absolute;width:240px;height:58px;background:#efeee4bb;top:-29px;left:calc(50% - 120px);transform:rotate(6deg)}
            .label{font-size:28px;margin-bottom:65px}h1{font-size:105px;line-height:1.24;letter-spacing:-4px}
            .hook{font-size:37px;margin-top:50px;border-top:3px solid #26251f;padding-top:30px}''',
        'editorial': '''body{background:#f2efe6;color:#252a28}main{padding:95px 85px;justify-content:space-between}
            .label{font-size:27px;letter-spacing:8px;border-top:9px solid #252a28;border-bottom:2px solid #252a28;padding:28px 0}
            .sheet{margin-top:auto;margin-bottom:auto}h1{font-family:"Songti SC","STSong",serif;font-size:120px;line-height:1.21;letter-spacing:-5px}
            .hook{font-size:37px;line-height:1.6;border-top:2px solid #252a28;padding-top:30px;margin-top:70px}
            .accent{width:135px;height:16px;background:#b74732;position:absolute;bottom:110px;right:90px}''',
        'receipt': '''body{background:#cec6b8;color:#2d2924}main{padding:95px 110px;justify-content:center}
            .sheet{background:#faf8f0;padding:72px 56px 95px;box-shadow:8px 13px 0 #00000016;border-bottom:14px dashed #cec6b8;transform:rotate(1deg)}
            .label{font-size:30px;text-align:center;letter-spacing:6px;border-bottom:3px dashed #91887c;padding-bottom:40px;margin-bottom:65px}
            h1{font-size:99px;line-height:1.28;letter-spacing:-4px}.hook{font-size:36px;border-top:3px dashed #91887c;margin-top:65px;padding-top:36px}''',
        'split': '''body{background:#eee8d9;color:#243e45}main{padding:95px 82px;justify-content:center}
            main:before{content:"";position:absolute;background:#243e45;width:100%;height:40%;bottom:0;left:0;z-index:-1}
            .label{font-size:28px;background:#e3a0ad;align-self:flex-start;padding:14px 24px;transform:rotate(-5deg);margin-bottom:65px}
            .sheet{margin-bottom:180px}h1{font-size:124px;line-height:1.18;letter-spacing:-5px;position:relative}
            .hook{font-size:39px;background:#f2cc58;display:inline-block;padding:28px 32px;margin-top:70px;transform:rotate(2deg);max-width:820px}''',
        'ink': '''body{background:#f8f7f1;color:#292c29}main{padding:130px 90px;justify-content:center}
            .label{font-size:29px;color:#777c72;margin-bottom:90px}h1{font-size:118px;line-height:1.3;letter-spacing:-4px;transform:rotate(-1deg)}
            h1:after{content:"";display:block;height:16px;background:#eacc56;transform:rotate(-3deg);margin-top:26px;width:82%;border-radius:45%}
            .hook{font-size:39px;margin-top:65px;max-width:780px}.accent{width:70px;height:70px;border:3px solid #b64635;border-radius:50%;position:absolute;bottom:120px;right:110px}''',
    }
    label = {'bold': '我有话说', 'sticky': '随手写两句', 'editorial': '说说这件事',
             'receipt': '今天想吐槽', 'split': '说句实话', 'ink': '一点个人看法'}[style]
    # Each layout is structurally distinct. No paragraph cards, fake photographs,
    # page counters or repeated product badges are baked into the cover.
    if style in {'sticky', 'receipt', 'editorial', 'split'}:
        content = f'<div class="sheet"><div class="label">{label}</div>{heading}<p class="hook">{hook}</p></div>'
    else:
        content = f'<div class="label">{label}</div>{heading}<p class="hook">{hook}</p>'
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><style>
    *{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1440px;overflow:hidden;font-family:"PingFang SC","Heiti SC",sans-serif}}
    main{{position:relative;isolation:isolate;height:100%;display:flex;flex-direction:column}}
    h1{{margin:0;font-weight:800;overflow-wrap:anywhere;text-wrap:balance}}.hook{{margin-bottom:0;line-height:1.55;font-weight:500}}
    {layouts[style]}</style><main>{content}<div class="accent"></div></main></html>'''


def render_article(article_id: str, title: str, cards: list, template: str = 'auto') -> list[dict]:
    from playwright.sync_api import sync_playwright
    from PIL import Image

    safe_id = ''.join(c for c in article_id if c.isalnum() or c in '-_')
    if not safe_id or safe_id != article_id:
        raise ValueError('非法文章标识')
    data_root = Path(os.getenv('XHS_DATA_DIR', str(ROOT / 'data'))).resolve()
    destination = data_root / 'media' / safe_id / uuid4().hex[:12]
    destination.mkdir(parents=True, exist_ok=True)
    style = cover_style(template, article_id, title)
    first = next((item for item in cards if isinstance(item, dict)), {})
    subtitle = str(first.get('cover_subtitle') or first.get('body') or '')
    # Legacy drafts may have paragraphs in cards; use only a short hook on their cover.
    subtitle = subtitle.split('\n')[0][:30]
    file = destination / '01.png'
    markup = _html(title, subtitle, style)
    chrome = os.getenv('XHS_RENDER_BROWSER', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome if Path(chrome).exists() else None, headless=True)
        page = browser.new_page(viewport={'width':1080, 'height':1440}, device_scale_factor=1)
        try:
            page.set_content(markup, wait_until='load')
            page.evaluate('document.fonts.ready')
            overflow = '''() => [...document.querySelectorAll('h1,.hook,.sheet')].some(e=>{const r=e.getBoundingClientRect();return r.top<20||r.bottom>1420||r.left<15||r.right>1065})'''
            if page.evaluate(overflow):
                page.add_style_tag(content='h1{font-size:82px!important;line-height:1.2!important}.hook{font-size:32px!important;margin-top:36px!important}.label{margin-bottom:36px!important}')
            if page.evaluate(overflow):
                raise ValueError('封面文字超出画布，请缩短标题或钩子')
            page.screenshot(path=str(file), animations='disabled')
            (destination / '01.html').write_text(markup, encoding='utf-8')
            with Image.open(file) as image:
                if image.size != (1080, 1440):
                    raise ValueError('图片尺寸错误')
        finally:
            browser.close()
    digest = hashlib.sha256(file.read_bytes()).hexdigest()
    return [{'id':uuid4().hex, 'url':'/media/' + str(file.relative_to(data_root / 'media')), 'path':str(file), 'sha256':digest,
             'source':'本地原创 HTML/CSS 封面', 'license':'原创；仅使用本机中文字体渲染', 'template':style, 'width':1080, 'height':1440}]
