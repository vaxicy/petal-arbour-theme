#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Petal Arbour Theme — vector logo candidates (SVG rendered by headless Chromium).

The reference art is an arch (arbour) with a cream sun inside, soft wavy bands and
a drooping frond. The marks distil that one composition instead of drawing yet
another flower, which keeps this pastel theme distinct from the pink set already
in the store.

Every palette colour is extremely light, so each mark pairs a pale fill with a
deep plum outline: without the outline the shapes disappear on a white page.

Playwright screenshots each SVG cell with omit_background=True (true
transparency); PIL only composes the contact sheets, the inline strip and the
official logo/logo.png exported from SELECTED.

Colours come from manifest.json. Change SELECTED and re-run; never hand-copy PNGs.
"""
import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128
CELL = 512
PREVIEW = 256
SELECTED = "01"
CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]


def hx(vals):
    return "#%02X%02X%02X" % tuple(vals)


PINK = hx(_C["frame"])                             # #F4C2EA
PALE = hx(_C["toolbar"])                           # #FDDBF5
CREAM = hx(_C["ntp_background"])                   # #FEFDDC
MINT = hx(_C["button_background"])                 # #D8F9D2
VIOLET = hx(_C["button_background_secondary"])     # #DAC6F1
LINK = hx(_C["ntp_link"])                          # #9C5AA8
INK = hx(_C["ntp_text"])                           # #3E2A44

SHADOW = """
  <filter id="ds" x="-35%%" y="-35%%" width="170%%" height="170%%">
    <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="%s" flood-opacity=".18"/>
  </filter>""" % INK


def svg_open(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s%s</svg>' % (CELL, CELL, defs, body))


def frond(x0, y0, x1, y1, leaves, size, fill, vein, curve=26):
    """A drooping frond: quadratic stem with paired leaflets set along the tangent.

    Leaflets are ellipses rotated to follow the stem and pushed out perpendicular to
    it, each with a thin vein-coloured rim so a pale leaf still reads on a pale page.
    """
    cx, cy = (x0 + x1) / 2 + curve, (y0 + y1) / 2 - abs(curve) * 0.5

    def point(t):
        u = 1 - t
        return (u * u * x0 + 2 * u * t * cx + t * t * x1,
                u * u * y0 + 2 * u * t * cy + t * t * y1)

    out = ['<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" '
           'stroke-width="3.5" stroke-linecap="round" stroke-opacity=".75"/>'
           % (x0, y0, cx, cy, x1, y1, vein)]
    for i in range(leaves):
        t = 0.16 + 0.74 * i / max(1, leaves - 1)
        px, py = point(t)
        qx, qy = point(min(1.0, t + 0.02))
        ang = math.degrees(math.atan2(qy - py, qx - px))
        rx = size * (1.0 - 0.42 * t)
        ry = rx * 0.46
        for side in (-1, 1):
            ox = px - math.sin(math.radians(ang)) * rx * side * 0.95
            oy = py + math.cos(math.radians(ang)) * rx * side * 0.95
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" '
                       'stroke="%s" stroke-width="1.6" stroke-opacity=".55" '
                       'transform="rotate(%.1f %.1f %.1f)"/>'
                       % (ox, oy, rx, ry, fill, vein, ang + side * 52, ox, oy))
    return "".join(out)


# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
<defs>
  <linearGradient id="ar1" x1="0" y1="0" x2="0.4" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  <path d="M62 224 V116 a66 66 0 0 1 132 0 V224 Z" fill="url(#ar1)" stroke="%s" stroke-width="4"/>
  <path d="M74 224 V118 a54 54 0 0 1 108 0 V224 Z" fill="%s"/>
  <circle cx="128" cy="126" r="30" fill="%s"/>
  <path d="M74 182 q27 -18 54 0 q27 18 54 0 V224 H74 Z" fill="%s"/>
</g>
%s
""" % (MINT, PALE, SHADOW, INK, CREAM, CREAM, MINT,
       frond(60, 70, 128, 96, 4, 15, PINK, INK)))

SVG_02 = svg_open("""
<defs>%s</defs>
<g filter="url(#ds)">
  <circle cx="128" cy="128" r="100" fill="%s"/>
  <path d="M70 196 V120 a58 58 0 0 1 116 0 V196 Z" fill="%s" stroke="%s" stroke-width="4"/>
  <circle cx="128" cy="124" r="26" fill="%s"/>
  <path d="M70 162 q29 -16 58 0 q29 16 58 0 V196 H70 Z" fill="%s"/>
</g>
%s
""" % (SHADOW, PINK, MINT, INK, CREAM, MINT,
       frond(168, 150, 96, 186, 3, 13, CREAM, INK)))

SVG_03 = svg_open("""
<defs>%s</defs>
<g fill="none" stroke-linecap="round" filter="url(#ds)">
  <!-- three nested arches: the arbour read as a rainbow -->
  <path d="M52 214 V128 a76 76 0 0 1 152 0 V214" stroke="%s" stroke-width="16"/>
  <path d="M74 214 V128 a54 54 0 0 1 108 0 V214" stroke="%s" stroke-width="16"/>
  <path d="M96 214 V128 a32 32 0 0 1 64 0 V214" stroke="%s" stroke-width="16"/>
</g>
<circle cx="128" cy="196" r="16" fill="%s"/>
""" % (SHADOW, VIOLET, CREAM, MINT, PINK))

SVG_04 = svg_open("""
<defs>%s</defs>
<circle cx="128" cy="128" r="100" fill="%s" filter="url(#ds)"/>
<circle cx="128" cy="128" r="100" fill="none" stroke="%s" stroke-width="4"/>
<path d="M80 190 V128 a48 48 0 0 1 96 0 V190 Z" fill="%s"/>
<circle cx="128" cy="130" r="20" fill="%s"/>
<path d="M80 168 q24 -13 48 0 q24 13 48 0 V190 H80 Z" fill="%s"/>
%s
""" % (SHADOW, VIOLET, INK, MINT, CREAM, MINT,
       frond(96, 92, 176, 118, 3, 11, CREAM, INK)))

SVG_05 = svg_open("""
<defs>
  <linearGradient id="sk5" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  <circle cx="128" cy="128" r="100" fill="url(#sk5)" stroke="%s" stroke-width="4"/>
  <circle cx="148" cy="86" r="30" fill="%s"/>
  <path d="M28 168 q30 -22 60 0 q30 22 60 0 q30 -22 60 0 V228 H28 Z" fill="%s"/>
  <path d="M28 196 q30 -18 60 0 q30 18 60 0 q30 -18 60 0 V228 H28 Z" fill="%s"/>
</g>
%s
""" % (PALE, MINT, SHADOW, INK, CREAM, PINK, MINT,
       frond(60, 74, 132, 108, 4, 14, VIOLET, INK)))

SVG_06 = svg_open("""
<defs>
  <linearGradient id="lw6" x1="0" y1="0" x2="0.5" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  <path d="M56 220 V114 a72 72 0 0 1 144 0 V220 Z" fill="url(#lw6)" stroke="%s" stroke-width="4"/>
  <circle cx="128" cy="104" r="24" fill="%s"/>
  <path d="M56 186 q36 -20 72 0 q36 20 72 0 V220 H56 Z" fill="%s"/>
</g>
%s
%s
""" % ("#C4E8F4", MINT, SHADOW, INK, CREAM, MINT,
       frond(70, 76, 168, 128, 4, 15, CREAM, INK, curve=30),
       frond(186, 196, 88, 152, 4, 15, PINK, INK, curve=-30)))

CANDIDATES = [
    ("01", "arch-sun", "Arbour with a cream sun and a frond — the reference scene", SVG_01),
    ("02", "pink-gate", "Mint gate on a pink disc — softest mark", SVG_02),
    ("03", "rainbow-arch", "Three nested arches with a pink sun — most graphic", SVG_03),
    ("04", "garden-badge", "Lilac badge with a mint gate — strongest at 32px", SVG_04),
    ("05", "sunrise-bands", "Sun over layered waves — closest to the illustration", SVG_05),
    ("06", "leaf-gate", "Leaf-shaped gate with two fronds — most graphic", SVG_06),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render_cells():
    cells = "".join('<div id="cell%s" style="width:%dpx;height:%dpx">%s</div>' % (num, CELL, CELL, svg)
                    for num, _n, _d, svg in CANDIDATES)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;background:transparent}'
            '#grid{display:flex;flex-wrap:wrap;width:%dpx}div[id^=cell]{display:block}'
            '</style></head><body><div id="grid">%s</div></body></html>' % (CELL * 3, cells))
    out = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception:
            # bundled headless shell may be missing after a Playwright update
            b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": CELL * 3, "height": CELL * 2})
        pg.set_content(html)
        for num, name, _d, _svg in CANDIDATES:
            path = CAND_DIR / ("%s-%s.png" % (num, name))
            pg.locator("#cell" + num).screenshot(path=str(path), omit_background=True)
            img = Image.open(path).convert("RGBA").resize((PREVIEW, PREVIEW), Image.LANCZOS)
            img.save(path)
            bbox = img.split()[3].getbbox()
            assert bbox, "candidate %s rendered empty" % name
            assert bbox[0] > 6 and bbox[1] > 6 and bbox[2] < PREVIEW - 6 and bbox[3] < PREVIEW - 6, \
                "candidate %s touches the canvas edge: %s" % (name, bbox)
            out[num] = img
            print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))
        b.close()
    return out


def contact_sheet(rendered, bg, txt, sub, path, title):
    cols, rows = 3, 2
    cw, ch = 384, 374
    gap, margin = 28, 40
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = margin * 2 + 34 + rows * ch + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f_title, f_name, f_desc, f_file = font(24, True), font(21, True), font(15), font(14)
    d.text((margin, margin), title, font=f_title, fill=txt)
    y0 = margin + 34
    for i, (num, name, desc, _svg) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        big = rendered[num].resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = rendered[num].resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 300 <= y + 322, "text block collides with the thumbnail row"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), (254, 253, 220))
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _n, _d, _s) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=(62, 42, 68))
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = render_cells()
    contact_sheet(rendered, (254, 253, 220), (62, 42, 68), (150, 128, 156),
                  CAND_DIR / "contact-light.png", "Petal Arbour — vector logo candidates (light)")
    contact_sheet(rendered, (52, 36, 56), (253, 219, 245), (188, 156, 190),
                  CAND_DIR / "contact-dark.png", "Petal Arbour — vector logo candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
