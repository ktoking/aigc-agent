#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 1920x1080 transparent OP title card PNG.
Main: 裂界行者 (bold white fill, electric-blue outline + glow)
Sub:  RIFT BREAKERS (letterspaced, white with blue glow)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FONT_PATH = "/System/Library/Fonts/PingFang.ttc"
FONT_IDX = 8  # PingFang SC Semibold

main_text = "裂界行者"
sub_text = "RIFT BREAKERS"

# Electric blue
E_BLUE = (40, 170, 255, 255)
E_BLUE_HI = (120, 210, 255, 255)
WHITE = (255, 255, 255, 255)

# ---- Layer 1: glow layer (blue blurred) ----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)

main_size = 300
sub_size = 66
f_main = ImageFont.truetype(FONT_PATH, main_size, index=FONT_IDX)
f_sub = ImageFont.truetype(FONT_PATH, sub_size, index=FONT_IDX)

# measure main text
bbox = gd.textbbox((0, 0), main_text, font=f_main, stroke_width=16)
mw = bbox[2] - bbox[0]
mh = bbox[3] - bbox[1]
mx = (W - mw) // 2 - bbox[0]
my = (H - mh) // 2 - 60 - bbox[1]  # shift up a touch

# letter-spaced sub text
def text_width_spaced(draw, txt, font, spacing):
    w = 0
    for ch in txt:
        b = draw.textbbox((0, 0), ch, font=font)
        w += (b[2] - b[0]) + spacing
    return w - spacing

sp = 14
sw = text_width_spaced(gd, sub_text, f_sub, sp)
sx = (W - sw) // 2
sy = my + mh + 70

def draw_spaced(draw, xy, txt, font, fill, spacing, stroke_width=0, stroke_fill=None):
    x, y = xy
    for ch in txt:
        draw.text((x, y), ch, font=font, fill=fill,
                  stroke_width=stroke_width, stroke_fill=stroke_fill)
        b = draw.textbbox((0, 0), ch, font=font)
        x += (b[2] - b[0]) + spacing

# glow: draw main + sub in blue, multiple passes, then blur
for _ in range(3):
    gd.text((mx, my), main_text, font=f_main, fill=E_BLUE, stroke_width=18, stroke_fill=E_BLUE)
draw_spaced(gd, (sx, sy), sub_text, f_sub, E_BLUE, sp, stroke_width=6, stroke_fill=E_BLUE)
glow = glow.filter(ImageFilter.GaussianBlur(18))

# ---- Layer 2: main crisp text ----
card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(card)
# main: white fill, blue stroke
d.text((mx, my), main_text, font=f_main, fill=WHITE, stroke_width=14, stroke_fill=E_BLUE)
# add a thinner bright-blue inner stroke for punch
d.text((mx, my), main_text, font=f_main, fill=None, stroke_width=3, stroke_fill=E_BLUE_HI)
# sub: white fill, blue stroke
draw_spaced(d, (sx, sy), sub_text, f_sub, WHITE, sp, stroke_width=4, stroke_fill=E_BLUE)

# composite glow behind card
out = Image.alpha_composite(glow, card)
out.save("episodes/OP00_opening/output/title_card.png")
print("title_card.png saved", out.size)
