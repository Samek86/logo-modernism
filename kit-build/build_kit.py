#!/usr/bin/env python3
"""LogoModernism kit generator — Effect C (180° interlocking notched slabs, Z-channel).
All geometry is orthogonal; rect unions are traced into clean outline paths (no live text)."""
import os, subprocess
from collections import defaultdict

OUT = "/workspace/logo-modernism/examples/kit"
ACCENT = "#FF4F00"   # International Orange
os.makedirs(OUT, exist_ok=True)

# ---------- rectilinear union -> outline path ----------
def union_path(rects, ndp=3):
    """rects: list of (x, y, w, h). Returns SVG path data of the union outline."""
    xs = sorted({round(v, ndp) for x, y, w, h in rects for v in (x, x + w)})
    ys = sorted({round(v, ndp) for x, y, w, h in rects for v in (y, y + h)})
    xi = {v: i for i, v in enumerate(xs)}; yi = {v: i for i, v in enumerate(ys)}
    filled = set()
    for x, y, w, h in rects:
        for i in range(xi[round(x, ndp)], xi[round(x + w, ndp)]):
            for j in range(yi[round(y, ndp)], yi[round(y + h, ndp)]):
                filled.add((i, j))
    # directed edges, clockwise in screen coords (y down)
    edges = {}
    def add(a, b):
        if (b, a) in edges: del edges[(b, a)]
        else: edges[(a, b)] = True
    for i, j in filled:
        p = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
        for k in range(4): add(p[k], p[(k + 1) % 4])
    nxt = defaultdict(list)
    for a, b in edges: nxt[a].append(b)
    used = set(); loops = []
    for start in list(edges):
        if start in used: continue
        loop = []; e = start
        while e not in used:
            used.add(e); loop.append(e[0])
            cands = [b for b in nxt[e[1]] if (e[1], b) not in used]
            if not cands: break
            # prefer a right turn at pinch points so loops stay simple
            dx, dy = e[1][0] - e[0][0], e[1][1] - e[0][1]
            def turn(b):
                ex, ey = b[0] - e[1][0], b[1] - e[1][1]
                return -(dx * ey - dy * ex)
            b = sorted(cands, key=turn)[0]
            e = (e[1], b)
        loops.append(loop)
    d = []
    for loop in loops:
        pts = [(xs[i], ys[j]) for i, j in loop]
        # drop collinear points
        simp = []
        n = len(pts)
        for k in range(n):
            a, b, c = pts[k - 1], pts[k], pts[(k + 1) % n]
            if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]): continue
            simp.append(b)
        f = lambda v: ("%g" % round(v, 2))
        d.append("M" + " L".join(f"{f(x)} {f(y)}" for x, y in simp) + " Z")
    return " ".join(d)

# ---------- mark geometry ----------
def mark_rects(a, b, c, h):
    """Square [a,b]; channel c; top bar height h. Two L-slabs, 180° about centre."""
    s = a + b
    Y1 = a + h; Y2 = s - c - Y1; X2 = (s - c) / 2
    top = [(a, a, b - a, h), (a, Y1, X2 - a, Y2 - Y1)]
    rot = lambda r: (s - r[0] - r[2], s - r[1] - r[3], r[2], r[3])
    return top, [rot(r) for r in top]

def mark_path(a, b, c, h):
    t, btm = mark_rects(a, b, c, h)
    return union_path(t) + " " + union_path(btm)

# master: 8-unit grid (crisp at 32/64/128 px). span 32..224, channel 16, bar 56, leg 64
MASTER = dict(a=32, b=224, c=16, h=56)
# reversed tile: 7-unit grid, 65.6% of tile, same proportions (24u span: bar 7u, leg 8u, channel 2u)
REV = dict(a=44, b=212, c=14, h=49)
# 16px cut: 16-unit grid = 1px; span 1..15 px, channel 2px, bar 4px, leg 4px
SMALL = dict(a=16, b=240, c=32, h=64)

P_MASTER = mark_path(**MASTER)
P_REV = mark_path(**REV)
P_SMALL = mark_path(**SMALL)
TILE = "M56 0 H200 A56 56 0 0 1 256 56 V200 A56 56 0 0 1 200 256 H56 A56 56 0 0 1 0 200 V56 A56 56 0 0 1 56 0 Z"

# ---------- wordmark: hand-built orthogonal sans ----------
# units: cap 100, x-height top y=28, baseline y=100, descender y=128
# optical compensation: verticals TV heavier than horizontals TH
TV, TH = 17, 14
T = TV
XT, BL, DS = 28, 100, 128
MID = (XT + BL - TH) / 2          # centred mid-bar for e / s
def bowl(w, right_top=XT, right_bot=BL):
    return [(0, XT, w, TH), (0, BL - TH, w, TH), (0, XT, TV, BL - XT), (w - TV, right_top, TV, right_bot - right_top)]
G = {}
G['L'] = (58, lambda: [(0, 0, TV, 100), (0, 100 - TH, 58, TH)])
G['o'] = (66, lambda: bowl(66))
G['g'] = (66, lambda: bowl(66, XT, DS) + [(0, DS - TH, 66, TH)])
G['M'] = (100, lambda: [(0, 0, 100, TH), (0, 0, TV, 100), (100 - TV, 0, TV, 100), ((100 - TV) / 2, 0, TV, 62)])
G['d'] = (66, lambda: bowl(66, 0, BL))
G['e'] = (66, lambda: [(0, XT, 66, TH), (0, XT, TV, BL - XT), (0, BL - TH, 66, TH), (0, MID, 66, TH), (66 - TV, XT, TV, MID + TH - XT)])
G['r'] = (48, lambda: [(0, XT, TV, BL - XT), (0, XT, 48, TH)])
G['n'] = (66, lambda: [(0, XT, TV, BL - XT), (0, XT, 66, TH), (66 - TV, XT, TV, BL - XT)])
G['i'] = (TV, lambda: [(0, XT, TV, BL - XT), (0, 0, TV, TH + 2)])
G['s'] = (62, lambda: [(0, XT, 62, TH), (0, XT, TV, MID + TH - XT), (0, MID, 62, TH), (62 - TV, MID, TV, BL - MID), (0, BL - TH, 62, TH)])
G['m'] = (104, lambda: [(0, XT, TV, BL - XT), (0, XT, 104, TH), ((104 - TV) / 2, XT, TV, BL - XT), (104 - TV, XT, TV, BL - XT)])
TRACK = 18
KERN = {('L', 'o'): -8}

def wordmark_rects(word="LogoModernism"):
    x = 0; out = []; prev = None
    for ch in word:
        if prev: x += TRACK + KERN.get((prev, ch), 0)
        w, fn = G[ch]
        for (rx, ry, rw, rh) in fn(): out.append((x + rx, ry, rw, rh))
        x += w; prev = ch
    return out, x   # rects, total width

WM_RECTS, WM_W = wordmark_rects()

def xform(rects, s, dx, dy):
    return [(dx + x * s, dy + y * s, w * s, h * s) for x, y, w, h in rects]

def glyph_paths(rects_by_glyph):
    return " ".join(union_path(r) for r in rects_by_glyph)

def wordmark_path(s, dx, dy):
    # union per glyph keeps paths readable/editable
    x = 0; prev = None; parts = []
    for ch in "LogoModernism":
        if prev: x += TRACK + KERN.get((prev, ch), 0)
        w, fn = G[ch]
        parts.append(union_path(xform([(x + rx, ry, rw, rh) for rx, ry, rw, rh in fn()], s, dx, dy)))
        x += w; prev = ch
    return " ".join(parts)

def mark_at(size, ox, oy, geom=MASTER):
    """master/small geometry scaled from 256 box to `size`, origin (ox,oy)."""
    s = size / 256
    t, b = mark_rects(**geom)
    return union_path(xform(t, s, ox, oy)) + " " + union_path(xform(b, s, ox, oy))

# ---------- write SVGs ----------
def svg(vb, body, title, comment):
    return (f'<!-- {comment} -->\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="t">\n'
            f'  <title id="t">{title}</title>\n{body}\n</svg>\n')

files = {}
files['mark.svg'] = svg("0 0 256 256", f'  <path fill="currentColor" d="{P_MASTER}"/>', "LogoModernism mark",
    "LogoModernism master — two identical L-slabs, 180° about centre, split by a uniform Z-channel. 8-unit grid: span 32–224, channel 16, bar 56, leg 64")
files['mark-reversed.svg'] = svg("0 0 256 256",
    f'  <path fill="#000" d="{TILE}"/>\n  <path fill="#fff" d="{P_REV}"/>', "LogoModernism mark reversed",
    "Reversed — white mark on black rounded-square field (r56). Mark 168/256, 7-unit grid, same 7:8:2 proportions")
files['mark-16.svg'] = svg("0 0 256 256", f'  <path fill="currentColor" d="{P_SMALL}"/>', "LogoModernism mark 16px",
    "16px cut — 16-unit grid (1 unit = 1px @16). Span 1–15px, channel 2px, bar 4px, leg 4px. Use at ≤24px")
files['favicon.svg'] = svg("0 0 256 256",
    f'  <path fill="#000" d="{TILE}"/>\n  <path fill="#fff" d="{P_MASTER}"/>', "LogoModernism favicon",
    "Favicon tile — master geometry (8-unit grid → whole pixels at 32px) on black field")

# horizontal lockup. X (clear-space unit) = bar height of mark = 56/256 of mark box.
MK = 192                       # drawn mark height (master span)
X = MK * 56 / 192              # = 56  -> clear-space unit
cap = MK * 0.5                 # wordmark cap height = half mark height
s = cap / 100
gap = X
mark_box = MK * 256 / 192      # 256-box size that yields 192 drawn
off = (mark_box - MK) / 2      # 32
W = X + MK + gap + WM_W * s + X
H = X + MK + X
mk = mark_at(mark_box, X - off, X - off)
wm = wordmark_path(s, X + MK + gap, X + (MK - cap) / 2)
files['lockup-horizontal.svg'] = svg(f"0 0 {W:g} {H:g}",
    f'  <path fill="currentColor" d="{mk}"/>\n  <path fill="currentColor" d="{wm}"/>', "LogoModernism horizontal lockup",
    "Horizontal lockup — cap height = ½ mark, gap = X (X = slab bar = 56 @ 192 mark), viewBox includes X clear-space")
# stacked lockup
cap2 = MK * 0.30
s2 = cap2 / 100
wmw2 = WM_W * s2
W2 = X + max(MK, wmw2) + X
H2 = X + MK + gap + DS * s2 + X
mk2 = mark_at(mark_box, (W2 - MK) / 2 - off, X - off)
wm2 = wordmark_path(s2, (W2 - wmw2) / 2, X + MK + gap)
files['lockup-stacked.svg'] = svg(f"0 0 {W2:g} {H2:g}",
    f'  <path fill="currentColor" d="{mk2}"/>\n  <path fill="currentColor" d="{wm2}"/>', "LogoModernism stacked lockup",
    "Stacked lockup — mark centred over wordmark, cap height = 0.3 × mark, gap = X, X clear-space")

for name, data in files.items():
    open(os.path.join(OUT, name), "w").write(data)

def r(src, dst, w, h=None):
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h or w), src, "-o", dst], check=True)
r(f"{OUT}/favicon.svg", f"{OUT}/favicon.png", 32)
r(f"{OUT}/mark-reversed.svg", f"{OUT}/app-icon.png", 512)

# ---------- kit sheet ----------
SW = 1600
def P(d, fill): return f'<path fill="{fill}" d="{d}"/>'
def label(x, y, t, fill="#000", size=15, anchor="start", weight="normal"):
    return (f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="0.5">{t}</text>')
el = []
M = 80
# header: wordmark paths + subtitle
el.append(P(wordmark_path(0.40, M, 64), "#000"))
el.append(label(SW - M, 96, "IDENTITY KIT · EFFECT C · v1", anchor="end", size=15, weight="bold"))
el.append(f'<rect x="{M}" y="130" width="{SW-2*M}" height="3" fill="#000"/>')
# row 1: master large | reversed | clear-space diagram  (panels 460 tall)
y1 = 170; ph = 460; pw = (SW - 2 * M - 2 * 30) / 3
xA, xB, xC = M, M + pw + 30, M + 2 * (pw + 30)
el.append(f'<rect x="{xA}" y="{y1}" width="{pw}" height="{ph}" fill="#fff" stroke="#000" stroke-width="2"/>')
el.append(P(mark_at(360, xA + (pw - 360) / 2, y1 + 40), "#000"))
el.append(label(xA + 16, y1 + ph - 16, "01  MASTER — mark.svg"))
el.append(f'<rect x="{xB}" y="{y1}" width="{pw}" height="{ph}" fill="#E4E4E0"/>')
s_t = 320 / 256; tx, ty = xB + (pw - 320) / 2, y1 + 50
el.append(f'<g transform="translate({tx} {ty}) scale({s_t})">{P(TILE, "#000")}{P(P_REV, "#fff")}</g>')
el.append(label(xB + 16, y1 + ph - 16, "02  REVERSED / APP ICON — mark-reversed.svg"))
# clear-space
el.append(f'<rect x="{xC}" y="{y1}" width="{pw}" height="{ph}" fill="#F2F2F2"/>')
cs_m = 220; cs_s = cs_m / 192; cx0 = xC + (pw - cs_m) / 2; cy0 = y1 + 110
Xp = 56 * cs_s
el.append(f'<rect x="{cx0-Xp}" y="{cy0-Xp}" width="{cs_m+2*Xp}" height="{cs_m+2*Xp}" fill="{ACCENT}" fill-opacity="0.16" stroke="{ACCENT}" stroke-width="2" stroke-dasharray="8 6"/>')
el.append(f'<rect x="{cx0}" y="{cy0}" width="{cs_m}" height="{cs_m}" fill="#fff"/>')
el.append(P(mark_at(cs_m * 256 / 192, cx0 - 32 * cs_s, cy0 - 32 * cs_s), "#000"))
# X markers: show bar height = X
el.append(f'<rect x="{cx0+cs_m+Xp+8}" y="{cy0}" width="8" height="{Xp}" fill="{ACCENT}"/>')
el.append(label(cx0 + cs_m + Xp + 22, cy0 + Xp / 2 + 5, "X", fill=ACCENT, weight="bold", size=17))
for (bx, by) in [(cx0 - Xp, cy0 + cs_m / 2 - 4), (cx0 + cs_m, cy0 + cs_m / 2 - 4)]:
    el.append(f'<rect x="{bx}" y="{by}" width="{Xp}" height="8" fill="{ACCENT}"/>')
el.append(f'<rect x="{cx0+cs_m/2-4}" y="{cy0-Xp}" width="8" height="{Xp}" fill="{ACCENT}"/>')
el.append(label(xC + 16, y1 + ph - 40, "03  CLEAR SPACE = X on all sides"))
el.append(label(xC + 16, y1 + ph - 16, "X = slab bar height (7/24 of mark)", size=13, fill="#555"))

# row 2: size ladder on white and black
y2 = y1 + ph + 40; rh = 170; half = (SW - 2 * M - 30) / 2
for k, (bg, fg) in enumerate([("#fff", "#000"), ("#000", "#fff")]):
    x0 = M + k * (half + 30)
    el.append(f'<rect x="{x0}" y="{y2}" width="{half}" height="{rh}" fill="{bg}" stroke="#000" stroke-width="2"/>')
    cx = x0 + 60
    for sz in (64, 32, 24, 16):
        geom = SMALL if sz <= 16 else MASTER
        oy = round(y2 + 30 + (64 - sz))
        el.append(P(mark_at(sz, round(cx), oy, geom), fg))
        el.append(label(cx + sz / 2, y2 + 130, f"{sz}px", fill=fg, anchor="middle", size=14))
        cx += max(sz, 40) + 90
    el.append(label(x0 + half - 16, y2 + 158, "16px uses mark-16.svg", fill="#888", anchor="end", size=12))
el.append(label(M, y2 + rh + 26, "04  SIZE LADDER — 64 / 32 / 24 / 16 px, rendered at 1:1", size=14))

# row 3: horizontal lockup on white, on black
y3 = y2 + rh + 60; lh = 190
for k, (bg, fg) in enumerate([("#fff", "#000"), ("#000", "#fff")]):
    x0 = M + k * (half + 30)
    el.append(f'<rect x="{x0}" y="{y3}" width="{half}" height="{lh}" fill="{bg}" stroke="#000" stroke-width="2"/>')
    sc = (half - 60) / W
    el.append(f'<g transform="translate({x0+30} {y3+(lh-H*sc)/2}) scale({sc})">{P(mk, fg)}{P(wm, fg)}</g>')
el.append(label(M, y3 + lh + 26, "05  HORIZONTAL LOCKUP — lockup-horizontal.svg", size=14))

# row 4: stacked lockup | colour
y4 = y3 + lh + 60; sh = 360
el.append(f'<rect x="{M}" y="{y4}" width="{half}" height="{sh}" fill="#fff" stroke="#000" stroke-width="2"/>')
sc2 = min((half - 80) / W2, (sh - 40) / H2)
el.append(f'<g transform="translate({M+(half-W2*sc2)/2} {y4+(sh-H2*sc2)/2}) scale({sc2})">{P(mk2, "#000")}{P(wm2, "#000")}</g>')
el.append(label(M, y4 + sh + 26, "06  STACKED LOCKUP — lockup-stacked.svg", size=14))
x0 = M + half + 30
sw_w = (half - 2 * 20) / 3
for i, (hexv, name, tc) in enumerate([("#000000", "BLACK", "#fff"), ("#FFFFFF", "WHITE", "#000"), (ACCENT, "INTERNATIONAL ORANGE", "#000")]):
    sx = x0 + i * (sw_w + 20)
    el.append(f'<rect x="{sx}" y="{y4}" width="{sw_w}" height="230" fill="{hexv}" stroke="#000" stroke-width="2"/>')
    el.append(label(sx + 14, y4 + 200, name, fill=tc, size=13, weight="bold"))
    el.append(label(sx + 14, y4 + 220, hexv, fill=tc, size=13))
# accent in use: mark on accent field
ax = x0; ay = y4 + 250
el.append(f'<rect x="{ax}" y="{ay}" width="{half}" height="110" fill="{ACCENT}"/>')
el.append(P(mark_at(96, ax + 24, ay + 7), "#000"))
el.append(label(ax + 140, ay + 50, "Accent = field only. Mark stays black or white.", size=14, weight="bold"))
el.append(label(ax + 140, ay + 74, "Never set the mark itself in orange on white.", size=13))
el.append(label(x0, y4 + sh + 26, "07  COLOUR — 1 accent + black/white", size=14))

SH = y4 + sh + 70
sheet = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">'
         f'<rect width="{SW}" height="{SH}" fill="#FAFAF7"/>' + "".join(el) + "</svg>")
open("/workspace/logo-modernism/kit-build/kit-sheet.src.svg", "w").write(sheet)
subprocess.run(["rsvg-convert", "-w", str(SW), "/workspace/logo-modernism/kit-build/kit-sheet.src.svg",
                "-o", f"{OUT}/kit-sheet.png"], check=True)
print("wordmark width", WM_W, "lockup", W, H, "stacked", W2, H2, "sheet", SW, SH)
