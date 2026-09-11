#!/usr/bin/env python3
"""
视频开幕标题生成器
给已有视频添加高端杂志风开幕标题：中文主标题 + 英文副标题 + 装饰细线 + 作者署名，
白色字体，渐显→保持→渐隐。

用法:
  python3 add_opening_title.py \
    --input input.mp4 --output output.mp4 \
    --title-cn "荒轨" --title-en "WASTELINE" \
    --subtitle "A POST-APOCALYPTIC TALE" --author "西瓜终结者"
"""

import argparse
import os
import subprocess
import sys
import tempfile

# ─── macOS 默认字体路径 ───────────────────────────────────────────
DEFAULT_FONT_CN = "/System/Library/Fonts/Supplemental/Songti.ttc"
DEFAULT_FONT_EN = "/System/Library/Fonts/Supplemental/Didot.ttc"
DEFAULT_FONT_SUB = "/System/Library/Fonts/Supplemental/Futura.ttc"

# 备选字体（当默认字体不存在时尝试）
FALLBACK_FONTS_CN = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
]
FALLBACK_FONTS_EN = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Times.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]


def parse_args():
    p = argparse.ArgumentParser(description="给视频添加高端杂志风开幕标题")
    p.add_argument("--input", required=True, help="输入视频路径")
    p.add_argument("--output", required=True, help="输出视频路径")
    p.add_argument("--title-cn", required=True, help="中文主标题")
    p.add_argument("--title-en", default="", help="英文主标题（Didot衬线体）")
    p.add_argument("--subtitle", default="", help="英文副标题（Futura）")
    p.add_argument("--author", default="", help="作者名（显示为 CREATED BY 作者名）")
    p.add_argument("--show-duration", type=float, default=6.0, help="标题总显示时长（秒），默认6")
    p.add_argument("--fade-in", type=float, default=1.2, help="渐显时长（秒），默认1.2")
    p.add_argument("--fade-out", type=float, default=1.2, help="渐隐时长（秒），默认1.2")
    p.add_argument("--font-cn", default=None, help="中文字体路径")
    p.add_argument("--font-en", default=None, help="英文主标题字体路径")
    p.add_argument("--font-sub", default=None, help="英文副标题字体路径")
    p.add_argument("--title-size", type=int, default=168, help="中文主标题字号，默认168")
    p.add_argument("--en-size", type=int, default=52, help="英文主标题字号，默认52")
    p.add_argument("--tracking", type=int, default=14, help="英文主标题字间距（px），默认14")
    p.add_argument("--crf", type=int, default=18, help="x264 CRF，默认18")
    p.add_argument("--preset", default="fast", help="x264 preset，默认fast")
    p.add_argument("--dry-run", action="store_true", help="只生成标题PNG，不执行ffmpeg")
    return p.parse_args()


def resolve_font(preferred, fallbacks):
    """解析可用字体路径"""
    if preferred and os.path.exists(preferred):
        return preferred
    for f in fallbacks:
        if os.path.exists(f):
            return f
    return None


def get_video_size(video_path):
    """用 ffprobe 获取视频宽高"""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0:s=x",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] ffprobe 失败: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    w, h = result.stdout.strip().split("x")
    return int(w), int(h)


def draw_text_centered(draw, text, font, y, fill, tracking=0, canvas_w=1280):
    """绘制居中文本，支持字间距"""
    if tracking == 0:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (canvas_w - tw) // 2 - bbox[0]
        draw.text((x, y), text, font=font, fill=fill)
    else:
        widths = []
        for ch in text:
            bbox = draw.textbbox((0, 0), ch, font=font)
            widths.append(bbox[2] - bbox[0])
        total_w = sum(widths) + tracking * (len(text) - 1)
        x = (canvas_w - total_w) // 2
        for i, ch in enumerate(text):
            bbox = draw.textbbox((0, 0), ch, font=font)
            draw.text((x - bbox[0], y), ch, font=font, fill=fill)
            x += widths[i] + tracking


def draw_hline(draw, y, width, color, canvas_w=1280):
    """绘制居中水平线"""
    x1 = (canvas_w - width) // 2
    draw.line([(x1, y), (x1 + width, y)], fill=color, width=1)


def generate_title_png(args, width, height, output_path):
    """生成透明背景标题 PNG"""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 颜色
    WHITE = (255, 255, 255, 255)
    WHITE_85 = (255, 255, 255, 217)
    WHITE_60 = (255, 255, 255, 153)
    WHITE_40 = (255, 255, 255, 102)

    # 字体
    font_cn_path = resolve_font(args.font_cn, [DEFAULT_FONT_CN] + FALLBACK_FONTS_CN)
    font_en_path = resolve_font(args.font_en, [DEFAULT_FONT_EN] + FALLBACK_FONTS_EN)
    font_sub_path = resolve_font(args.font_sub, [DEFAULT_FONT_SUB] + FALLBACK_FONTS_EN)

    if not font_cn_path:
        print("[ERROR] 未找到可用中文字体，请用 --font-cn 指定", file=sys.stderr)
        sys.exit(1)

    # 按视频分辨率缩放字号（基准 1280x720）
    scale = width / 1280.0
    title_size = int(args.title_size * scale)
    en_size = int(args.en_size * scale)
    sub_size = int(20 * scale)
    author_en_size = int(18 * scale)
    author_cn_size = int(24 * scale)
    tracking = int(args.tracking * scale)

    f_title = ImageFont.truetype(font_cn_path, title_size)
    f_en = ImageFont.truetype(font_en_path or font_cn_path, en_size) if args.title_en else None
    f_sub = ImageFont.truetype(font_sub_path or font_en_path or font_cn_path, sub_size) if args.subtitle else None
    f_author_en = ImageFont.truetype(font_sub_path or font_en_path or font_cn_path, author_en_size) if args.author else None
    f_author_cn = ImageFont.truetype(font_cn_path, author_cn_size) if args.author else None

    # 垂直布局（按 720 基准，再缩放）
    def sy(v): return int(v * height / 720.0)

    current_y = sy(180)

    # 顶部装饰线
    draw_hline(draw, current_y, int(120 * scale), WHITE_40, width)
    current_y += sy(25)

    # 中文主标题
    draw_text_centered(draw, args.title_cn, f_title, current_y, WHITE, canvas_w=width)
    current_y += int(title_size * 1.15)

    # 英文主标题
    if f_en and args.title_en:
        draw_text_centered(draw, args.title_en.upper(), f_en, current_y, WHITE_85, tracking=tracking, canvas_w=width)
        current_y += int(en_size * 1.3)

    # 中间装饰线
    draw_hline(draw, current_y, int(200 * scale), WHITE_40, width)
    current_y += sy(25)

    # 副标题
    if f_sub and args.subtitle:
        draw_text_centered(draw, args.subtitle.upper(), f_sub, current_y, WHITE_60, tracking=int(4 * scale), canvas_w=width)
        current_y += sy(45)

    # 作者
    if args.author and f_author_en and f_author_cn:
        text_en = "CREATED BY"
        text_cn = args.author
        bbox_en = draw.textbbox((0, 0), text_en, font=f_author_en)
        bbox_cn = draw.textbbox((0, 0), text_cn, font=f_author_cn)
        w_en = bbox_en[2] - bbox_en[0]
        w_cn = bbox_cn[2] - bbox_cn[0]
        gap = int(16 * scale)
        total = w_en + gap + w_cn
        x_start = (width - total) // 2
        draw.text((x_start - bbox_en[0], current_y), text_en, font=f_author_en, fill=WHITE_60)
        draw.text((x_start + w_en + gap - bbox_cn[0], current_y - int(2 * scale)), text_cn, font=f_author_cn, fill=WHITE_85)

    img.save(output_path)
    print(f"[OK] 标题 PNG 已生成: {output_path} ({width}x{height})")
    return output_path


def run_ffmpeg(args, title_png):
    """执行 ffmpeg 叠加标题"""
    fade_out_start = args.show_duration - args.fade_out
    if fade_out_start <= args.fade_in:
        print("[WARN] fade-in + fade-out 超过显示时长，已自动调整", file=sys.stderr)
        fade_out_start = args.fade_in + 0.1

    filter_complex = (
        f"[1:v]format=rgba,"
        f"fade=t=in:st=0:d={args.fade_in}:alpha=1,"
        f"fade=t=out:st={fade_out_start}:d={args.fade_out}:alpha=1,"
        f"trim=0:{args.show_duration},setpts=PTS-STARTPTS[title];"
        f"[0:v][title]overlay=0:0:eof_action=pass[vout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", args.input,
        "-loop", "1", "-i", title_png,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-preset", args.preset,
        "-crf", str(args.crf),
        "-c:a", "copy",
        args.output,
    ]

    print(f"[RUN] ffmpeg 编码中...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] ffmpeg 失败:\n{result.stderr[-2000:]}", file=sys.stderr)
        sys.exit(1)

    size_mb = os.path.getsize(args.output) / 1024 / 1024
    print(f"[OK] 输出视频: {args.output} ({size_mb:.1f} MB)")


def main():
    args = parse_args()

    if not os.path.exists(args.input):
        print(f"[ERROR] 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 确保输出目录存在
    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)

    # 获取视频分辨率
    width, height = get_video_size(args.input)
    print(f"[INFO] 视频分辨率: {width}x{height}")

    # 生成标题 PNG
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        title_png = tmp.name
    try:
        generate_title_png(args, width, height, title_png)

        if args.dry_run:
            print(f"[DRY-RUN] 标题 PNG 已保存到: {title_png}")
            print(f"[DRY-RUN] 跳过 ffmpeg 编码")
        else:
            run_ffmpeg(args, title_png)
    finally:
        if not args.dry_run:
            os.unlink(title_png)

    print("[DONE] 完成")


if __name__ == "__main__":
    main()
