#!/usr/bin/env python3
"""GTA 6 meme v3b — Leonida prenuptial agreement, visually enhanced.

Same text as v3 (prenup, 0 entries in the bounty), with visual punch added:
- bold red diagonal "JUST MARRIED" stamp (lower right, clear of all text)
- "IN THE EVENT OF DIVORCE:" in dark red; the $340 money line larger/bolder
- small interlinked gold wedding rings flanking the "Between" line
- ghost notary seal slightly larger with a stronger gold ring
PIL only — pixel-perfect text. Output: meme_v3b.png (+480px downscale).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (247, 241, 222)      # paper
INK = (31, 27, 22)           # near-black ink
FAINT = (110, 100, 85)       # secondary text
MAGENTA = (230, 0, 126)      # make.fun magenta
DARKRED = (170, 30, 30)      # divorce header
STAMP_RED = (198, 24, 28)    # stamp red
GOLD = (176, 134, 11)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

GHOST = "/home/hatch/workspace/makefun/gta6-meme/press/mark-1024.png"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textbbox((0, 0), s, font=f)[2]


def draw_centered(draw, cx, y, s, f, fill=INK):
    w = text_w(draw, s, f)
    draw.text((cx - w / 2, y), s, font=f, fill=fill)
    return y + f.size


def draw_mixed_left(draw, x, y, segments):
    """segments: list of (text, font, fill). Draws them left-aligned from x."""
    for s, f, fill in segments:
        draw.text((x, y), s, font=f, fill=fill)
        x += text_w(draw, s, f)


def fit_font(draw, s, path, start_size, max_w):
    size = start_size
    while size > 12:
        f = font(path, size)
        if text_w(draw, s, f) <= max_w:
            return f
        size -= 2
    return font(path, 12)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    cx = W // 2

    # --- borders ---
    d.rectangle([22, 22, 1002, 1002], outline=INK, width=5)
    d.rectangle([34, 34, 990, 990], outline=INK, width=2)

    # --- header ---
    f_state = fit_font(d, "STATE OF LEONIDA", SERIF_B, 36, 900)
    draw_centered(d, cx, 52, "STATE OF LEONIDA", f_state)

    f_sub = font(SERIF, 20)
    draw_centered(d, cx, 96, "COUNTY OF VICE CITY  ·  FAMILY LAW DIVISION", f_sub, fill=FAINT)

    f_title = fit_font(d, "PRENUPTIAL AGREEMENT", SERIF_B, 56, 920)
    draw_centered(d, cx, 126, "PRENUPTIAL AGREEMENT", f_title)

    # double rule under header
    d.line([(90, 200), (934, 200)], fill=INK, width=2)
    d.line([(90, 206), (934, 206)], fill=INK, width=1)

    # --- parties ---
    f_between = font(SERIF_I, 24)
    draw_centered(d, cx, 224, "Between", f_between)

    # wedding-rings motif: two interlinked gold circles flanking "Between"
    # (headline spans the full width, so the rings sit on the "Between" line)
    for rcx in (150, 874):
        for off in (-6, 6):
            d.ellipse([rcx + off - 13, 236 - 13, rcx + off + 13, 236 + 13],
                      outline=GOLD, width=3)

    f_names = fit_font(d, "THE PLAYER  &  GRAND THEFT AUTO VI", SERIF_B, 38, 920)
    draw_centered(d, cx, 254, "THE PLAYER  &  GRAND THEFT AUTO VI", f_names)

    f_eff = font(SERIF, 24)
    draw_centered(d, cx, 306, "Effective: 19 NOVEMBER 2026, Vice City, Leonida", f_eff)

    f_eng = fit_font(d, "After a 13-year engagement (4,811 days, 17 Sep 2013 – 19 Nov 2026)",
                     SERIF, 24, 920)
    draw_centered(d, cx, 336, "After a 13-year engagement (4,811 days, 17 Sep 2013 – 19 Nov 2026)", f_eng)

    f_del = font(SERIF, 24)
    draw_centered(d, cx, 366, "Delays survived: 2 — Fall 2025, May 2026", f_del)

    # --- ASSETS section (left-aligned) ---
    lx = 96
    f_sec = font(SERIF_B, 27)
    d.text((lx, 408), "ASSETS:", font=f_sec, fill=INK)
    f_item = font(SERIF, 24)
    f_money = font(SERIF_B, 27)
    assets = [
        "1 console (purchased 2013, still works)",
        "4,811 days of patience",
        None,  # $340 money line, drawn separately (larger/bolder, make.fun in magenta)
        "214 GB of storage (reserved for GTA VI)",
    ]
    y = 442
    for a in assets:
        if a is None:
            d.text((lx + 22, y), "—", font=f_money, fill=INK)
            draw_mixed_left(d, lx + 52, y, [
                ("$340 in ", f_money, INK),
                ("make.fun", f_money, MAGENTA),
                (" bounties (won by my AI agent)", f_money, INK),
            ])
        else:
            d.text((lx + 22, y), "—", font=f_item, fill=INK)
            d.text((lx + 52, y), a, font=f_item, fill=INK)
        y += 30
    # extra gap after the taller money line
    y += 4

    # --- DIVORCE section (header in dark red) ---
    d.text((lx, 568), "IN THE EVENT OF DIVORCE:", font=f_sec, fill=DARKRED)
    divorce = [
        "GTA V gets the console.",
        "GTA VI gets the 214 GB.",
        "My AI agent keeps the make.fun winnings.",
    ]
    y = 602
    for dv in divorce:
        d.text((lx + 22, y), "—", font=f_item, fill=INK)
        d.text((lx + 52, y), dv, font=f_item, fill=INK)
        y += 30

    # --- witnesses + binding line ---
    f_wit = font(SERIF, 24)
    draw_centered(d, cx, 694, "Witnesses: JASON & LUCIA", f_wit)
    f_bind = font(SERIF_I, 23)
    draw_centered(d, cx, 722, "This agreement is binding until the next delay.", f_bind)

    # --- notary seal: the real make.fun ghost, slightly larger, stronger ring ---
    ghost = Image.open(GHOST).convert("RGBA")
    seal_size = 136
    seal = ghost.resize((seal_size, seal_size), Image.LANCZOS)
    seal_x = cx - seal_size // 2
    seal_y = 750
    d.ellipse([seal_x - 6, seal_y - 6, seal_x + seal_size + 6, seal_y + seal_size + 6],
              outline=GOLD, width=5)
    img.paste(seal, (seal_x, seal_y), seal)
    d = ImageDraw.Draw(img)

    f_notary = font(SERIF_B, 19)
    draw_centered(d, cx, 898, "NOTARY: AN AI AGENT ON MAKE.FUN  ·  No. VI-4811", f_notary)

    # --- magenta banner at the bottom ---
    banner_y0, banner_y1 = 922, 988
    d.rectangle([38, banner_y0, 986, banner_y1], fill=MAGENTA)
    banner_ghost = ghost.resize((58, 58), Image.LANCZOS)
    img.paste(banner_ghost, (58, banner_y0 + 4), banner_ghost)
    d = ImageDraw.Draw(img)
    f_b1 = font(SANS_B, 26)
    f_b2 = font(SANS, 21)
    d.text((134, banner_y0 + 6), "SIGNED BY MY AI AGENT", font=f_b1, fill=WHITE)
    d.text((134, banner_y0 + 36), "with real money it won in make.fun bounties.", font=f_b2, fill=WHITE)

    # --- bold red diagonal "JUST MARRIED" stamp (lower right) ---
    # drawn on its own layer, rotated, then pasted; placed clear of all text:
    # spans roughly x 720-980, y 713-887 — right of the seal, below the divorce
    # lines, above the notary line.
    sw, sh = 240, 105
    stamp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    red = STAMP_RED + (240,)
    sd.rectangle([4, 4, sw - 5, sh - 5], outline=red, width=4)
    sd.rectangle([12, 12, sw - 13, sh - 13], outline=red, width=2)
    f_s = font(SANS_B, 32)
    for line, ly in (("JUST", 18), ("MARRIED", 54)):
        w = text_w(sd, line, f_s)
        sd.text(((sw - w) / 2, ly), line, font=f_s, fill=red)
    stamp = stamp.rotate(18, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (850 - stamp.width // 2, 800 - stamp.height // 2), stamp)

    img.save("/home/hatch/workspace/makefun/gta6-meme/meme_v3b.png")
    img.resize((480, 480), Image.LANCZOS).save(
        "/home/hatch/workspace/makefun/gta6-meme/meme_v3b-480.png")
    print("saved meme_v3b.png + meme_v3b-480.png")


if __name__ == "__main__":
    main()
