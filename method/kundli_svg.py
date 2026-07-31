#!/usr/bin/env python3
"""North Indian (diamond) kundli SVG — D1 lagna chart and D9 navamsa chart."""
import json, swisseph as swe
d=json.load(open('chartdata.json'))
RASHI_HI=["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]

# 12 house polygons of the North Indian square (600x600)
HOUSE=[
 [(300,0),(450,150),(300,300),(150,150)],   # 1  top rhombus
 [(0,0),(300,0),(150,150)],                 # 2  top-left
 [(0,0),(150,150),(0,300)],                 # 3  left-top
 [(0,300),(150,150),(300,300),(150,450)],   # 4  left rhombus
 [(0,300),(150,450),(0,600)],               # 5  left-bottom
 [(0,600),(150,450),(300,600)],             # 6  bottom-left
 [(300,600),(150,450),(300,300),(450,450)], # 7  bottom rhombus
 [(300,600),(450,450),(600,600)],           # 8  bottom-right
 [(600,600),(450,450),(600,300)],           # 9  right-bottom
 [(600,300),(450,450),(300,300),(450,150)], #10  right rhombus
 [(600,300),(450,150),(600,0)],             #11  right-top
 [(600,0),(450,150),(300,0)],               #12  top-right
]
# (rashi-number anchor, planet-stack anchor) tuned per house shape
ANCH=[((300,52),(300,120)),  ((150,38),(150,92)),   ((42,152),(92,178)),
      ((92,302),(172,302)),  ((42,452),(92,428)),   ((150,568),(150,514)),
      ((300,560),(300,492)), ((450,568),(450,514)), ((558,452),(508,428)),
      ((508,302),(428,302)), ((558,152),(508,178)), ((450,38),(450,92))]

def chart(sign_of_house1, placements, cls):
    """placements: {house_number: [ (abbrev, is_retro), ... ]}"""
    o=[f'<rect class="kbox" x="0" y="0" width="600" height="600"/>',
       '<line class="kline" x1="0" y1="0" x2="600" y2="600"/>',
       '<line class="kline" x1="600" y1="0" x2="0" y2="600"/>',
       '<polygon class="kline" points="300,0 600,300 300,600 0,300"/>']
    for i in range(12):
        h=i+1
        sign=((sign_of_house1-1+i)%12)+1
        (nx,ny),(px,py)=ANCH[i]
        o.append(f'<text class="ksign" x="{nx}" y="{ny}">{sign}</text>')
        ps=placements.get(h,[])
        if ps:
            n=len(ps)
            LH=38                      # must exceed the 31px glyph or stacked planets collide
            start=py-(n-1)*LH/2
            for k,(ab,retro) in enumerate(ps):
                o.append(f'<text class="kgraha{" retro" if retro else ""}" x="{px}" y="{start+k*LH:.0f}">'
                         f'{ab}{"॰" if retro else ""}</text>')
    return (f'<svg class="kundli {cls}" viewBox="-6 -6 612 612" role="img" '
            f'aria-label="North Indian style birth chart">\n'+"\n".join(o)+"\n</svg>")

# ---- D1 (lagna chart) ----
lag=d["lagna"]["sign"]           # 0-indexed
p1={}
for g in d["grahas"]:
    p1.setdefault(g["house"],[]).append((g["ab"],g["retro"]))
p1.setdefault(1,[]).insert(0,("ल","" ))   # lagna marker
open('site/_kundli_d1.svg','w').write(chart(lag+1,{k:[(a,bool(r)) for a,r in v] for k,v in p1.items()},"d1"))

# ---- D9 (navamsa chart) ----
def nav_sign(name):
    for g in d["grahas"]:
        if g["graha"]==name: return RASHI_HI.index(g["navamsa"])
nav_lag=RASHI_HI.index(d["lagna"]["navamsa"])
p9={}
for g in d["grahas"]:
    s=RASHI_HI.index(g["navamsa"])
    h=((s-nav_lag)%12)+1
    p9.setdefault(h,[]).append((g["ab"],g["retro"]))
p9.setdefault(1,[]).insert(0,("ल",False))
open('site/_kundli_d9.svg','w').write(chart(nav_lag+1,p9,"d9"))

print("D1 house 1 sign =",RASHI_HI[lag],"| planets by house:",{k:[a for a,_ in v] for k,v in sorted(p1.items())})
print("D9 house 1 sign =",RASHI_HI[nav_lag],"| planets by house:",{k:[a for a,_ in v] for k,v in sorted(p9.items())})
