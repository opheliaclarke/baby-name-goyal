#!/usr/bin/env python3
"""North Indian kundli (D1 + D9) + full chart data with Hindi labels."""
import swisseph as swe, json, math
LAT,LON,TZ=30.2110,74.9455,5.5
swe.set_sid_mode(swe.SIDM_LAHIRI,0,0)
F=swe.FLG_SWIEPH|swe.FLG_SIDEREAL|swe.FLG_SPEED
J=swe.julday(2026,7,28,10+15/60.-TZ,swe.GREG_CAL)

RASHI_HI=["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
NAK_HI=["अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशिरा","आर्द्रा","पुनर्वसु","पुष्य","आश्लेषा","मघा",
"पूर्वा फाल्गुनी","उत्तरा फाल्गुनी","हस्त","चित्रा","स्वाति","विशाखा","अनुराधा","ज्येष्ठा","मूल",
"पूर्वाषाढ़ा","उत्तराषाढ़ा","श्रवण","धनिष्ठा","शतभिषा","पूर्वा भाद्रपद","उत्तरा भाद्रपद","रेवती"]
GRAHA=[("सू","सूर्य",swe.SUN),("चं","चंद्र",swe.MOON),("मं","मंगल",swe.MARS),("बु","बुध",swe.MERCURY),
       ("गु","गुरु",swe.JUPITER),("शु","शुक्र",swe.VENUS),("श","शनि",swe.SATURN)]
# exaltation / debilitation signs (0-indexed) per classical texts
UCHCHA={"सूर्य":0,"चंद्र":1,"मंगल":9,"बुध":5,"गुरु":3,"शुक्र":11,"शनि":6}
NEECHA={k:(v+6)%12 for k,v in UCHCHA.items()}
SWA={"सूर्य":[4],"चंद्र":[3],"मंगल":[0,7],"बुध":[2,5],"गुरु":[8,11],"शुक्र":[1,6],"शनि":[9,10]}

pos={}
for ab,hi,pl in GRAHA:
    p=swe.calc_ut(J,pl,F)[0]
    pos[hi]=dict(ab=ab,lon=p[0],retro=p[3]<0)
r=swe.calc_ut(J,swe.MEAN_NODE,F)[0]
pos["राहु"]=dict(ab="रा",lon=r[0],retro=True)
pos["केतु"]=dict(ab="के",lon=(r[0]+180)%360,retro=True)
asc=swe.houses_ex(J,LAT,LON,b'P',swe.FLG_SIDEREAL)[1][0]
LAGNA_SIGN=int(asc//30)

def nav(l): return int(l/(10/3.))%12
def house_of(sign): return ((sign-LAGNA_SIGN)%12)+1

rows=[]
for hi,d in pos.items():
    s=int(d["lon"]//30); deg=d["lon"]%30
    n=int(d["lon"]//(360/27)); pada=int((d["lon"]%(360/27))//(360/108))+1
    st=""
    if hi in UCHCHA:
        if s==UCHCHA[hi]: st="उच्च"
        elif s==NEECHA[hi]: st="नीच"
        elif s in SWA.get(hi,[]): st="स्वगृही"
    rows.append(dict(graha=hi,ab=d["ab"],sign=s,rashi=RASHI_HI[s],
                     deg=f"{int(deg)}°{int((deg%1)*60):02d}'",
                     nak=NAK_HI[n],pada=pada,house=house_of(s),
                     navamsa=RASHI_HI[nav(d["lon"])],retro=d["retro"],status=st))
data=dict(lagna=dict(rashi=RASHI_HI[LAGNA_SIGN],sign=LAGNA_SIGN,
                     deg=f"{int(asc%30)}°{int(((asc%30)%1)*60):02d}'",
                     nak=NAK_HI[int(asc//(360/27))],pada=int((asc%(360/27))//(360/108))+1,
                     navamsa=RASHI_HI[nav(asc)]),
          grahas=rows)
json.dump(data,open('chartdata.json','w'),ensure_ascii=False,indent=1)

print(f"लग्न: {data['lagna']['rashi']} {data['lagna']['deg']}  (नवमांश {data['lagna']['navamsa']})\n")
print(f"{'ग्रह':<8}{'राशि':<10}{'अंश':<9}{'भाव':>4}  {'नक्षत्र':<18}{'पाद':>3}  {'नवमांश':<9}{'स्थिति'}")
print("-"*82)
for r_ in rows:
    print(f"{r_['graha']:<8}{r_['rashi']:<10}{r_['deg']:<9}{r_['house']:>4}  {r_['nak']:<18}{r_['pada']:>3}  "
          f"{r_['navamsa']:<9}{r_['status']}{' वक्री' if r_['retro'] else ''}")
