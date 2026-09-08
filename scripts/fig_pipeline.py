# -*- coding: utf-8 -*-
"""GraphRAG pipeline sequence diagram (replaces the mermaid block in the doc)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "graphrag-pipeline.svg")

W, H = 1360, 660
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
SLATE = dict(fill="#E9EFF5", stroke="#3E5C76", text="#22374A", tint="#3E5C76")
OCHRE = dict(fill="#FBEEE2", stroke="#B0703A", text="#6B4320", tint="#B0703A")
GREEN = dict(fill="#E6EFEA", stroke="#47795F", text="#294A39", tint="#47795F")
EDGE_C, EDGE_LBL, LIFE_C = "#8A9199", "#4E565E", "#CDD3D9"

PARTS = [
    ("user",      105,  116, "User",              OCHRE, "ACTOR"),
    ("processor", 330,  140, "Processor",         SLATE, "STAGE"),
    ("retriever", 555,  140, "Retriever",         SLATE, "STAGE"),
    ("graph",     800,  178, "Graph Data Source", GREEN, "SOURCE"),
    ("organizer", 1045, 140, "Organizer",         SLATE, "STAGE"),
    ("generator", 1270, 140, "Generator",         SLATE, "STAGE"),
]
PX = {p[0]: p[1] for p in PARTS}
BOX_Y, BOX_H, LIFE_BOT = 46, 58, 606

MSGS = [
    ("user", "processor",      "Query",                         182, False),
    ("processor", "retriever", "Pre-processed query",           298, False),
    ("retriever", "graph",     "Retrieve content",              344, False),
    ("graph", "retriever",     "Content",                       390, True),
    ("retriever", "organizer", "Content",                       436, False),
    ("organizer", "generator", "Arranged and refined content",  482, False),
    ("processor", "generator", "Pre-processed query",           528, False),
    ("generator", "user",      "Generated answer",              574, False),
]

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
o.append(f'<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto" '
         f'markerUnits="userSpaceOnUse"><path d="M0,0.6 L8.4,4.5 L0,8.4 z" fill="{EDGE_C}"/></marker></defs>')
o.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')

# lifelines
for _, x, _, _, _, _ in PARTS:
    o.append(f'<line x1="{x}" y1="{BOX_Y+BOX_H}" x2="{x}" y2="{LIFE_BOT}" stroke="{LIFE_C}" '
             f'stroke-width="1.4" stroke-dasharray="5 5"/>')

def label(mx, my, text, span, size=11.5):
    """Draw a message label fully above the arrow so the line is never broken."""
    while size > 9.4 and len(text) * size * 0.62 + 14 > span - 12:
        size -= 0.5
    tw = len(text) * size * 0.62 + 14
    o.append(f'<rect x="{mx-tw/2:.1f}" y="{my-22:.1f}" width="{tw:.1f}" height="17" rx="3" fill="#FFFFFF"/>')
    o.append(f'<text x="{mx:.1f}" y="{my-9:.1f}" text-anchor="middle" font-size="{size}" fill="{EDGE_LBL}">{text}</text>')

# messages
for a, b, text, y, dashed in MSGS:
    x1, x2 = PX[a], PX[b]
    d = 6 if x2 > x1 else -6
    dash = ' stroke-dasharray="6 4"' if dashed else ''
    o.append(f'<line x1="{x1+d}" y1="{y}" x2="{x2-d}" y2="{y}" stroke="{EDGE_C}" stroke-width="1.5"{dash} marker-end="url(#ar)"/>')
    label((x1 + x2) / 2, y, text, abs(x2 - x1))

# self-loop on Processor
sx = PX["processor"]
o.append(f'<path d="M{sx+6},216 L{sx+54},216 L{sx+54},250 L{sx+10},250" fill="none" stroke="{EDGE_C}" '
         f'stroke-width="1.5" marker-end="url(#ar)"/>')
o.append(f'<text x="{sx+66}" y="{237}" font-size="11.5" fill="{EDGE_LBL}">Process query</text>')

# participant boxes
for _, x, w, name, c, kind in PARTS:
    o.append(f'<rect x="{x-w/2}" y="{BOX_Y}" width="{w}" height="{BOX_H}" rx="8" fill="{c["fill"]}" '
             f'stroke="{c["stroke"]}" stroke-width="1.7"/>')
    o.append(f'<text x="{x}" y="{BOX_Y+21}" text-anchor="middle" font-size="9" letter-spacing="1.1" fill="{c["tint"]}">{kind}</text>')
    o.append(f'<text x="{x}" y="{BOX_Y+42}" text-anchor="middle" font-size="14.5" font-weight="600" fill="{c["text"]}">{name}</text>')

o.append(f'<text x="46" y="640" font-size="12.5" font-style="italic" fill="#9AA0A8">'
         'The query reaches the generator twice: once retrieved and organised as content, and once as the processed query itself.</text>')
o.append('</svg>')
open(OUT, "w").write("\n".join(o))
print("wrote", OUT)
