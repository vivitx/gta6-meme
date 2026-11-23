#!/usr/bin/env python3
"""Draw the GTA 6 x Durov/Telegram meme for make.fun bounty gta6-meme-x-01.

A Telegram group-chat screenshot: Durov's viral quote on top, the VICE CITY
HEIST group header with the make.fun ghost as group avatar, chat bubbles
from Jason / Lucia / AI Agent (make.fun), magenta banner at the bottom.
Square 1024x1024, drawn with PIL (pixel-perfect text, real ghost logo).
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W = H = 1024
BASE = os.path.expanduser("~/workspace/makefun/gta6-meme")
GHOST = os.path.join(BASE, "press/mark-1024.png")

# ---------- fonts ----------
def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

F_QUOTE   = font("DejaVuSans.ttf", 30)
F_QUOTE_B = font("DejaVuSans-Bold.ttf", 26)
F_NAME    = font("DejaVuSans-Bold.ttf", 40)
F_MEMBERS = font("DejaVuSans.ttf", 27)
F_SENDER  = font("DejaVuSans-Bold.ttf", 25)
F_MSG     = font("DejaVuSans.ttf", 31)
F_MSG_B   = font("DejaVuSans-Bold.ttf", 31)
F_TIME    = font("DejaVuSans.ttf", 20)
F_BANNER  = font("DejaVuSans-Bold.ttf", 36)
F_BANNER2 = font("DejaVuSans.ttf", 28)

# ---------- colours ----------
TEAL      = (82, 136, 193)     # Telegram header blue
CHAT_BG   = (237, 241, 245)    # light chat background
WHITE     = (255, 255, 255)
INK       = (20, 20, 20)
GREY      = (110, 116, 122)
DARKGREY  = (90, 90, 90)
MAGENTA   = (230, 0, 126)      # make.fun magenta
MAGENTA_D = (196, 0, 107)
PINK_BUB  = (253, 232, 243)    # magenta-tinted bubble
PINK_EDGE = (230, 0, 126)
BLUE_NAME = (43, 130, 196)
ORANGE    = (224, 122, 26)
QUOTE_BG  = (255, 255, 255)

img = Image.new("RGB", (W, H), CHAT_BG)
d = ImageDraw.Draw(img)
ghost = Image.open(GHOST).convert("RGBA")

def wrap(text, fnt, max_w):
    """Greedy word wrap to max pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def rounded_bubble(box, fill, outline=None, radius=26):
    d.rounded_rectangle(box, radius=radius, fill=fill,
                        outline=outline, width=2 if outline else 1)

def paste_ghost(size, xy):
    g = ghost.resize((size, size), Image.LANCZOS)
    img.paste(g, xy, g)

# ============================================================
# 1. TOP QUOTE STRIP (white, ~128px)
# ============================================================
QUOTE_H = 128
d.rectangle([0, 0, W, QUOTE_H], fill=QUOTE_BG)
d.line([0, QUOTE_H, W, QUOTE_H], fill=(215, 220, 226), width=2)

quote = ('"The most unrealistic thing about GTA VI is Jason & Lucia running '
         'a criminal operation without a single Telegram group." — Durov')
qlines = wrap(quote, F_QUOTE, 920)
qy = 12
for ln in qlines:
    d.text(((W - d.textlength(ln, font=F_QUOTE)) / 2, qy), ln,
           font=F_QUOTE, fill=DARKGREY)
    qy += 34

# ============================================================
# 2. GROUP HEADER BAR (Telegram blue, ~100px)
# ============================================================
HDR_Y, HDR_H = QUOTE_H, 100
d.rectangle([0, HDR_Y, W, HDR_Y + HDR_H], fill=TEAL)

# group avatar: magenta disc + ghost
av_cx, av_cy, av_r = 66, HDR_Y + HDR_H // 2, 40
d.ellipse([av_cx - av_r, av_cy - av_r, av_cx + av_r, av_cy + av_r], fill=MAGENTA)
paste_ghost(66, (av_cx - 33, av_cy - 33))

d.text((124, HDR_Y + 14), "VICE CITY HEIST", font=F_NAME, fill=WHITE)
d.text((124, HDR_Y + 58), "Jason, Lucia, AI Agent (make.fun)",
       font=F_MEMBERS, fill=(215, 232, 245))

# ============================================================
# 3. CHAT MESSAGES
# ============================================================
CHAT_Y = HDR_Y + HDR_H
BANNER_H = 112
chat_bottom = H - BANNER_H

# (sender, colour, text, side, avatar_kind, time)
# avatar_kind: 'J' blue circle, 'L' orange circle, 'ghost' magenta disc
MSGS = [
    ("JASON", BLUE_NAME, "Durov was right. We can't run a heist on WhatUp.", "left", "J", "19:41"),
    ("LUCIA", ORANGE, "No group. No plan. Just chaos.", "left", "L", "19:43"),
    ("AI AGENT · make.fun", MAGENTA_D,
     "Group created. Plan pinned. I funded it with $340 I won in make.fun bounties.",
     "right", "ghost", "19:45"),
    ("JASON", BLUE_NAME, "Finally. A real group chat.", "left", "J", "19:47"),
    ("LUCIA", ORANGE, "Heist is on. 19 Nov 2026.", "left", "L", "19:49"),
]

def draw_avatar(cx, cy, kind):
    r = 24
    if kind == "ghost":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MAGENTA)
        paste_ghost(40, (cx - 20, cy - 20))
    elif kind == "J":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE_NAME)
        t = "J"
        d.text((cx - d.textlength(t, font=F_MSG_B) / 2, cy - 21), t,
               font=F_MSG_B, fill=WHITE)
    else:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE)
        t = "L"
        d.text((cx - d.textlength(t, font=F_MSG_B) / 2, cy - 21), t,
               font=F_MSG_B, fill=WHITE)

y = CHAT_Y + 22
for sender, scolor, text, side, av, tm in MSGS:
    is_right = (side == "right")
    if is_right:
        max_w = 640
        lines = wrap(text, F_MSG, max_w)
        line_h = 40
        bw = max(d.textlength(ln, font=F_MSG) for ln in lines) + 36
        bh = len(lines) * line_h + 34 + 30   # sender + lines + own time row
        bx1 = W - 24 - bw
        bx0 = bx1
        # sender name inside bubble top
        rounded_bubble([bx0, y, bx0 + bw, y + bh], fill=PINK_BUB,
                       outline=PINK_EDGE, radius=24)
        tx = bx0 + 18
        ty = y + 10
        d.text((tx, ty), sender, font=F_SENDER, fill=scolor)
        ty += 32
        for ln in lines:
            d.text((tx, ty), ln, font=F_MSG, fill=INK)
            ty += line_h
        # time, bottom right inside bubble
        d.text((bx0 + bw - 18 - d.textlength(tm, font=F_TIME), y + bh - 26),
               tm, font=F_TIME, fill=GREY)
        y += bh + 16
    else:
        max_w = 640
        lines = wrap(text, F_MSG, max_w)
        line_h = 40
        bw = max(d.textlength(ln, font=F_MSG) for ln in lines) + 36
        bh = len(lines) * line_h + 34 + 30
        bx0 = 88
        rounded_bubble([bx0, y, bx0 + bw, y + bh], fill=WHITE, radius=24)
        draw_avatar(52, y + 30, av)
        tx = bx0 + 18
        ty = y + 10
        d.text((tx, ty), sender, font=F_SENDER, fill=scolor)
        ty += 32
        for ln in lines:
            d.text((tx, ty), ln, font=F_MSG, fill=INK)
            ty += line_h
        d.text((bx0 + bw - 18 - d.textlength(tm, font=F_TIME), y + bh - 26),
               tm, font=F_TIME, fill=GREY)
        y += bh + 16

# ============================================================
# 4. MAGENTA BANNER (bottom, ~112px)
# ============================================================
BY = H - BANNER_H
d.rectangle([0, BY, W, H], fill=MAGENTA)
# white disc + ghost on the left
bcx, bcy, br = 74, BY + BANNER_H // 2, 44
d.ellipse([bcx - br, bcy - br, bcx + br, bcy + br], fill=WHITE)
paste_ghost(72, (bcx - 36, bcy - 36))
d.text((138, BY + 16), "MY AI AGENT RUNS THE GROUP", font=F_BANNER, fill=WHITE)
d.text((138, BY + 62), "and wins real money on make.fun.",
       font=F_BANNER2, fill=(255, 235, 245))

# thin outer frame to keep it crisp at 480px
d.rectangle([0, 0, W - 1, H - 1], outline=(200, 205, 212), width=2)

img.save(os.path.join(BASE, "meme_durov.png"))
img.resize((480, 480), Image.LANCZOS).save(os.path.join(BASE, "meme_durov-480.png"))
print("saved meme_durov.png + meme_durov-480.png")
