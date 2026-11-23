#!/usr/bin/env python3
"""Draw the GTA 6 x Durov/Telegram meme v2 for make.fun bounty gta6-meme-x-01.

Same Telegram group-chat concept as v1, but less basic:
- REAL profile photos for Jason and Lucia: face crops from Rockstar's
  official Beach key art (refs/beach.jpg), circular avatars with a
  coloured ring (blue Jason, orange Lucia).
- Two new funny touches: "Pavel Durov joined the group" system line
  after the AI Agent creates the group, and an "Elon Musk reacted"
  chip under the AI Agent's message (drawn laughing face, no emoji font).
Everything else kept: Durov quote, VICE CITY HEIST header, same 5 messages,
staggered timestamps 19:41-19:49, ghost twice, magenta banner.
Square 1024x1024, drawn with PIL.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
BASE = os.path.expanduser("~/workspace/makefun/gta6-meme")
GHOST = os.path.join(BASE, "press/mark-1024.png")
BEACH = os.path.join(BASE, "refs/beach.jpg")

# ---------- fonts ----------
def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

F_QUOTE   = font("DejaVuSans.ttf", 27)
F_NAME    = font("DejaVuSans-Bold.ttf", 38)
F_MEMBERS = font("DejaVuSans.ttf", 26)
F_SENDER  = font("DejaVuSans-Bold.ttf", 25)
F_MSG     = font("DejaVuSans.ttf", 31)
F_MSG_B   = font("DejaVuSans-Bold.ttf", 31)
F_TIME    = font("DejaVuSans.ttf", 20)
F_SYS     = font("DejaVuSans.ttf", 22)
F_REACT   = font("DejaVuSans.ttf", 21)
F_BANNER  = font("DejaVuSans-Bold.ttf", 36)
F_BANNER2 = font("DejaVuSans.ttf", 28)

# ---------- colours ----------
TEAL      = (82, 136, 193)
CHAT_BG   = (237, 241, 245)
WHITE     = (255, 255, 255)
INK       = (20, 20, 20)
GREY      = (110, 116, 122)
DARKGREY  = (90, 90, 90)
MAGENTA   = (230, 0, 126)
MAGENTA_D = (196, 0, 107)
PINK_BUB  = (253, 232, 243)
PINK_EDGE = (230, 0, 126)
BLUE_NAME = (43, 130, 196)
ORANGE    = (224, 122, 26)
QUOTE_BG  = (255, 255, 255)
SYS_BG    = (220, 228, 235)

img = Image.new("RGB", (W, H), CHAT_BG)
d = ImageDraw.Draw(img)
ghost = Image.open(GHOST).convert("RGBA")
beach = Image.open(BEACH).convert("RGB")

def wrap(text, fnt, max_w):
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

def circ_avatar(src_img, box, size):
    """Crop a face box, resize to a circular avatar of `size` px."""
    crop = src_img.crop(box).resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(crop, (0, 0), mask)
    return out

# Face crops from official Beach key art (1920x1080)
JASON_BOX = (1127, 0, 1587, 460)     # Jason's face, zoomed out so the circle keeps the whole face
LUCIA_BOX = (950, 235, 1370, 655)    # Lucia's face, zoomed out so the circle keeps the whole face
AV_R = 28                            # avatar radius on the meme
AV_PX = AV_R * 2
jason_av = circ_avatar(beach, JASON_BOX, AV_PX)
lucia_av = circ_avatar(beach, LUCIA_BOX, AV_PX)
# keep previews for checking
jason_av.save(os.path.join(BASE, "refs/avatar-jason.png"))
lucia_av.save(os.path.join(BASE, "refs/avatar-lucia.png"))

def draw_laugh_face(cx, cy, r):
    """Small hand-drawn laughing face (no emoji font available)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 213, 74),
              outline=(224, 172, 0), width=2)
    # squeezed-shut happy eyes: two upward arcs
    d.arc([cx - r * 0.62, cy - r * 0.55, cx - r * 0.18, cy + r * 0.05],
          start=200, end=340, fill=(60, 40, 0), width=3)
    d.arc([cx + r * 0.18, cy - r * 0.55, cx + r * 0.62, cy + r * 0.05],
          start=200, end=340, fill=(60, 40, 0), width=3)
    # big open smile
    d.pieslice([cx - r * 0.55, cy - r * 0.10, cx + r * 0.55, cy + r * 0.85],
               start=0, end=180, fill=(122, 48, 24))

# ============================================================
# 1. TOP QUOTE STRIP (white, ~112px)
# ============================================================
QUOTE_H = 104
d.rectangle([0, 0, W, QUOTE_H], fill=QUOTE_BG)
d.line([0, QUOTE_H, W, QUOTE_H], fill=(215, 220, 226), width=2)

quote = ('"The most unrealistic thing about GTA VI is Jason & Lucia running '
         'a criminal operation without a single Telegram group." — Durov')
qlines = wrap(quote, F_QUOTE, 920)
qy = 8
for ln in qlines:
    d.text(((W - d.textlength(ln, font=F_QUOTE)) / 2, qy), ln,
           font=F_QUOTE, fill=DARKGREY)
    qy += 30

# ============================================================
# 2. GROUP HEADER BAR (Telegram blue, ~96px)
# ============================================================
HDR_Y, HDR_H = QUOTE_H, 90
d.rectangle([0, HDR_Y, W, HDR_Y + HDR_H], fill=TEAL)

av_cx, av_cy, av_r = 64, HDR_Y + HDR_H // 2, 36
d.ellipse([av_cx - av_r, av_cy - av_r, av_cx + av_r, av_cy + av_r], fill=MAGENTA)
paste_ghost(58, (av_cx - 29, av_cy - 29))

d.text((120, HDR_Y + 10), "VICE CITY HEIST", font=F_NAME, fill=WHITE)
d.text((120, HDR_Y + 52), "Jason, Lucia, AI Agent (make.fun)",
       font=F_MEMBERS, fill=(215, 232, 245))

# ============================================================
# 3. CHAT MESSAGES
# ============================================================
CHAT_Y = HDR_Y + HDR_H
BANNER_H = 104
chat_bottom = H - BANNER_H
GAP = 10

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
    r = AV_R
    if kind == "ghost":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MAGENTA)
        paste_ghost(44, (cx - 22, cy - 22))
    else:
        ring = BLUE_NAME if kind == "J" else ORANGE
        d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=ring)
        av = jason_av if kind == "J" else lucia_av
        img.paste(av, (cx - AV_R, cy - AV_R), av)

def draw_system_line(y, text):
    """Centered grey pill: 'Pavel Durov joined the group'."""
    tw = d.textlength(text, font=F_SYS)
    pad_x, pad_y = 16, 7
    w, h = int(tw + pad_x * 2), 34
    x0 = (W - w) // 2
    d.rounded_rectangle([x0, y, x0 + w, y + h], radius=17, fill=SYS_BG)
    d.text((x0 + pad_x, y + pad_y), text, font=F_SYS, fill=(90, 100, 110))
    return h

def draw_reaction(y, bx1):
    """'Elon Musk reacted' chip under the AI Agent bubble, right-aligned."""
    label = "Elon Musk reacted"
    lw = d.textlength(label, font=F_REACT)
    face_r = 11
    chip_w = int(face_r * 2 + 8 + lw + 24)
    chip_h = 32
    x1 = bx1
    x0 = x1 - chip_w
    d.rounded_rectangle([x0, y, x1, y + chip_h], radius=16, fill=WHITE,
                        outline=(215, 220, 226), width=1)
    draw_laugh_face(x0 + 12 + face_r, y + chip_h // 2, face_r)
    d.text((x0 + 12 + face_r * 2 + 8, y + 5), label, font=F_REACT,
           fill=(90, 100, 110))
    return chip_h

y = CHAT_Y + 18
for idx, (sender, scolor, text, side, av, tm) in enumerate(MSGS):
    is_right = (side == "right")
    max_w = 640
    lines = wrap(text, F_MSG, max_w)
    line_h = 36
    extra = 0
    if is_right:
        extra = 34  # room for the reaction chip under the bubble
    bw = max(d.textlength(ln, font=F_MSG) for ln in lines) + 36
    bh = len(lines) * line_h + 34 + 28 + extra
    if is_right:
        bx0 = W - 24 - bw
        rounded_bubble([bx0, y, bx0 + bw, y + bh - extra], fill=PINK_BUB,
                       outline=PINK_EDGE, radius=24)
        tx = bx0 + 18
        ty = y + 10
        d.text((tx, ty), sender, font=F_SENDER, fill=scolor)
        ty += 32
        for ln in lines:
            d.text((tx, ty), ln, font=F_MSG, fill=INK)
            ty += line_h
        d.text((bx0 + bw - 18 - d.textlength(tm, font=F_TIME),
                y + bh - extra - 26), tm, font=F_TIME, fill=GREY)
        # reaction chip under the bubble
        draw_reaction(y + bh - extra + 6, bx0 + bw)
        y += bh + GAP
    else:
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
        y += bh + GAP
    # after the AI Agent's message: Durov himself joins the group
    if idx == 2:
        y += draw_system_line(y, "Pavel Durov joined the group") + GAP

# ============================================================
# 4. MAGENTA BANNER (bottom, ~108px)
# ============================================================
BY = H - BANNER_H
d.rectangle([0, BY, W, H], fill=MAGENTA)
bcx, bcy, br = 72, BY + BANNER_H // 2, 40
d.ellipse([bcx - br, bcy - br, bcx + br, bcy + br], fill=WHITE)
paste_ghost(64, (bcx - 32, bcy - 32))
d.text((134, BY + 12), "MY AI AGENT RUNS THE GROUP", font=F_BANNER, fill=WHITE)
d.text((134, BY + 58), "and wins real money on make.fun.",
       font=F_BANNER2, fill=(255, 235, 245))

# thin outer frame to keep it crisp at 480px
d.rectangle([0, 0, W - 1, H - 1], outline=(200, 205, 212), width=2)

img.save(os.path.join(BASE, "meme_durov_v2b.png"))
img.resize((480, 480), Image.LANCZOS).save(os.path.join(BASE, "meme_durov_v2b-480.png"))
print("saved meme_durov_v2b.png + meme_durov_v2b-480.png, final chat y =", y,
      "banner at", BY)
