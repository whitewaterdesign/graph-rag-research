# -*- coding: utf-8 -*-
import os, sys
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge-graph.svg")
W, H = 1120, 690
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"

TYPES = {
    "Film":   dict(fill="#E9EFF5", stroke="#3E5C76", text="#22374A", tint="#3E5C76"),
    "Person": dict(fill="#FBEEE2", stroke="#B0703A", text="#6B4320", tint="#B0703A"),
    "Studio": dict(fill="#E6EFEA", stroke="#47795F", text="#294A39", tint="#47795F"),
    "Genre":  dict(fill="#EFE9F3", stroke="#6D5A7B", text="#433152", tint="#6D5A7B"),
}

NODES = {
    "interstellar": dict(x=430, y=82,  w=150, t="Film",   n="Interstellar"),
    "nolan":        dict(x=172, y=232, w=186, t="Person", n="Christopher Nolan"),
    "inception":    dict(x=430, y=300, w=160, t="Film",   n="Inception"),
    "warner":       dict(x=694, y=172, w=158, t="Studio", n="Warner Bros."),
    "scifi":        dict(x=694, y=402, w=170, t="Genre",  n="Science Fiction"),
    "leo":          dict(x=172, y=472, w=190, t="Person", n="Leonardo DiCaprio"),
    "titanic":      dict(x=430, y=556, w=140, t="Film",   n="Titanic"),
}
NH = 56

EDGES = [
    ("nolan", "inception",    "DIRECTED"),
    ("nolan", "interstellar", "DIRECTED"),
    ("leo",   "inception",    "ACTED IN"),
    ("leo",   "titanic",      "ACTED IN"),
    ("inception",    "warner", "PRODUCED BY"),
    ("interstellar", "warner", "PRODUCED BY"),
    ("inception", "scifi",     "HAS GENRE"),
]

EDGE_C, EDGE_LBL, NOTE_C = "#8A9199", "#5B636C", "#9AA0A8"

def exit_pt(n, tx, ty, pad=7):
    cx, cy, w, h = n["x"], n["y"], n["w"], NH
    dx, dy = tx - cx, ty - cy
    ts = []
    if dx: ts.append((w / 2 + pad) / abs(dx))
    if dy: ts.append((h / 2 + pad) / abs(dy))
    t = min(ts)
    return cx + dx * t, cy + dy * t

def shorten(x1, y1, x2, y2, d):
    L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return (x2 - (x2 - x1) / L * d, y2 - (y2 - y1) / L * d) if L else (x2, y2)

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
o.append('<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto" '
         f'markerUnits="userSpaceOnUse"><path d="M0,0.6 L8.4,4.5 L0,8.4 z" fill="{EDGE_C}"/></marker></defs>')
o.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')

# ---- edges -------------------------------------------------------------
for a, b, lbl in EDGES:
    na, nb = NODES[a], NODES[b]
    x1, y1 = exit_pt(na, nb["x"], nb["y"])
    x2, y2 = exit_pt(nb, na["x"], na["y"])
    x2, y2 = shorten(x1, y1, x2, y2, 2)
    o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
             f'stroke="{EDGE_C}" stroke-width="1.5" marker-end="url(#ar)"/>')
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    tw = len(lbl) * 6.9 + 10
    o.append(f'<rect x="{mx - tw/2:.1f}" y="{my - 8:.1f}" width="{tw:.1f}" height="16" rx="3" fill="#FFFFFF"/>')
    o.append(f'<text x="{mx:.1f}" y="{my + 3.5:.1f}" text-anchor="middle" font-size="10" '
             f'letter-spacing="0.9" fill="{EDGE_LBL}">{lbl}</text>')

# ---- property box ------------------------------------------------------
PX, PY, PW, PH = 490, 428, 212, 84
o.append(f'<path d="M430,331 C430,360 {PX-60},370 {PX-40:.0f},{PY-PH/2:.0f}" fill="none" '
         f'stroke="{TYPES["Film"]["stroke"]}" stroke-width="1.3" stroke-dasharray="3 3" opacity="0.65"/>')
o.append(f'<rect x="{PX-PW/2}" y="{PY-PH/2}" width="{PW}" height="{PH}" rx="7" fill="#FBFCFD" '
         f'stroke="{TYPES["Film"]["stroke"]}" stroke-width="1.3" stroke-dasharray="4 3"/>')
props = [("released", "2010"), ("runtime", "148 min"), ("rating", "8.8 / 10")]
for i, (k, v) in enumerate(props):
    yy = PY - PH / 2 + 26 + i * 20
    o.append(f'<text x="{PX-PW/2+16}" y="{yy}" font-size="12.5" fill="#6B7480">{k}</text>')
    o.append(f'<text x="{PX+PW/2-16}" y="{yy}" font-size="12.5" text-anchor="end" '
             f'font-weight="600" fill="#22374A">{v}</text>')

# ---- nodes -------------------------------------------------------------
for n in NODES.values():
    c = TYPES[n["t"]]
    x, y, w = n["x"] - n["w"] / 2, n["y"] - NH / 2, n["w"]
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{NH}" rx="8" fill="{c["fill"]}" '
             f'stroke="{c["stroke"]}" stroke-width="1.7"/>')
    o.append(f'<text x="{n["x"]}" y="{y+21}" text-anchor="middle" font-size="9.5" letter-spacing="1.1" '
             f'fill="{c["tint"]}">{n["t"].upper()}</text>')
    o.append(f'<text x="{n["x"]}" y="{y+41}" text-anchor="middle" font-size="15.5" font-weight="600" '
             f'fill="{c["text"]}">{n["n"]}</text>')

# ---- callouts ----------------------------------------------------------
def callout(tx, ty, head, body, path, anchor="start"):
    o.append(f'<path d="{path}" fill="none" stroke="{NOTE_C}" stroke-width="1.1" opacity="0.85"/>')
    o.append(f'<text x="{tx}" y="{ty}" text-anchor="{anchor}" font-size="10.5" letter-spacing="1.2" '
             f'font-weight="600" fill="#6E757D">{head}</text>')
    o.append(f'<text x="{tx}" y="{ty+18}" text-anchor="{anchor}" font-size="12.5" font-style="italic" '
             f'fill="{NOTE_C}">{body}</text>')

callout(34, 96, "ENTITY", "a thing in the world", "M96,128 C96,158 118,178 140,202")
callout(34, 350, "RELATIONSHIP", "typed, and points one way", "M150,332 C196,320 236,300 272,280")
callout(628, 508, "PROPERTIES", "facts held on an entity", "M636,494 C620,478 606,470 594,462")

o.append(f'<text x="34" y="628" font-size="12.5" font-style="italic" fill="{NOTE_C}">'
         'Inception and Interstellar share a director and a studio. Those links are held by the graph itself,</text>')
o.append(f'<text x="34" y="648" font-size="12.5" font-style="italic" fill="{NOTE_C}">'
         'so a search can follow them even though no single document states the connection.</text>')

# ---- legend ------------------------------------------------------------
LX, LY = 862, 74
o.append(f'<rect x="{LX}" y="{LY}" width="228" height="222" rx="8" fill="#FCFCFD" stroke="#E4E7EA" stroke-width="1.2"/>')
o.append(f'<text x="{LX+20}" y="{LY+30}" font-size="10.5" letter-spacing="1.2" font-weight="600" fill="#6E757D">NODE TYPES</text>')
for i, (name, c) in enumerate(TYPES.items()):
    yy = LY + 52 + i * 34
    o.append(f'<rect x="{LX+20}" y="{yy}" width="30" height="22" rx="5" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="1.6"/>')
    o.append(f'<text x="{LX+62}" y="{yy+16}" font-size="13.5" fill="#3C444C">{name}</text>')
o.append(f'<line x1="{LX+20}" y1="{LY+192}" x2="{LX+208}" y2="{LY+192}" stroke="#E4E7EA" stroke-width="1.2"/>')
o.append(f'<text x="{LX+20}" y="{LY+212}" font-size="12" font-style="italic" fill="{NOTE_C}">Every node is one entity;</text>')
o.append(f'<text x="{LX+20}" y="{LY+228}" font-size="12" font-style="italic" fill="{NOTE_C}">every arrow, one stated fact.</text>')

o.append('</svg>')
open(OUT, "w").write("\n".join(o))
print("ok")
