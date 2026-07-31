#!/usr/bin/env python3
"""Everything I did NOT compute the first time. Navamsa, doshas, nakshatra attributes, Lo Shu."""
import swisseph as swe
LAT,LON,TZ=30.2110,74.9455,5.5
swe.set_sid_mode(swe.SIDM_LAHIRI,0,0)
F=swe.FLG_SWIEPH|swe.FLG_SIDEREAL|swe.FLG_SPEED
J=swe.julday(2026,7,28,10+15/60.-TZ,swe.GREG_CAL)
SIGNS=["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
NAK=["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha",
"P.Phalguni","U.Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha",
"U.Ashadha","Shravana","Dhanishta","Shatabhisha","P.Bhadrapada","U.Bhadrapada","Revati"]
B=[("Sun",swe.SUN),("Moon",swe.MOON),("Mars",swe.MARS),("Mercury",swe.MERCURY),
   ("Jupiter",swe.JUPITER),("Venus",swe.VENUS),("Saturn",swe.SATURN)]
pos={n:swe.calc_ut(J,p,F)[0][0] for n,p in B}
rahu=swe.calc_ut(J,swe.MEAN_NODE,F)[0][0]; pos["Rahu"]=rahu; pos["Ketu"]=(rahu+180)%360
asc=swe.houses_ex(J,LAT,LON,b'P',swe.FLG_SIDEREAL)[1][0]; pos["Lagna"]=asc

print("="*78); print("1. NAVAMSA (D9) — the divisional chart I never computed"); print("="*78)
def nav(l): return int(l/(10/3.))%12
for k,v in pos.items():
    print(f"  {k:<8} D1 {SIGNS[int(v//30)]:<12} {v%30:5.2f}°   ->   D9 {SIGNS[nav(v)]}")
mn=nav(pos["Moon"]); ln=nav(pos["Lagna"])
print(f"\n  Moon's navamsa sign  = {SIGNS[mn]}")
print(f"  Navamsa lagna        = {SIGNS[ln]}")
print(f"  Note: the naming syllable comes from the Moon's RASHI nakshatra pada, not the D9.")
print(f"  Cross-check: pada 4 of a nakshatra ALWAYS maps to the 4th navamsa of its span,")
print(f"  so pada and navamsa are two views of the same 3°20' arc — they cannot disagree.")

print("\n"+"="*78); print("2. DOSHAS — none of which I checked before"); print("="*78)
# Gandanta: last 3°20' of a water sign / first 3°20' of a fire sign
def gandanta(l):
    s=int(l//30); d=l%30
    water=[3,7,11]; fire=[0,4,8]
    return (s in water and d>=26+40/60.) or (s in fire and d<=3+20/60.)
print(f"  Moon gandanta?        {'YES' if gandanta(pos['Moon']) else 'NO'}  (Moon at {SIGNS[int(pos['Moon']//30)]} {pos['Moon']%30:.2f}°)")
print(f"  Lagna gandanta?       {'YES' if gandanta(pos['Lagna']) else 'NO'}")
# Kaal Sarp: every planet inside one Rahu-Ketu hemisphere
R,K=pos["Rahu"],pos["Ketu"]
def between(a,b,x): 
    a%=360;b%=360;x%=360
    return (a<=x<=b) if a<b else (x>=a or x<=b)
side1=[n for n,_ in B if between(K,R,pos[n])]; side2=[n for n,_ in B if not between(K,R,pos[n])]
print(f"  Kaal Sarp yoga?       {'YES' if not side1 or not side2 else 'NO'}  (Ketu->Rahu arc: {side1 or 'none'} | other arc: {side2 or 'none'})")
# Mangal dosha: Mars in 1,2,4,7,8,12 from lagna / Moon / Venus
def house(frm,x): return int(((x-frm)%360)//30)+1
for ref in ("Lagna","Moon","Venus"):
    h=house(pos[ref]- (pos[ref]%30), pos["Mars"])
    print(f"  Mars house from {ref:<6} {h:>2}   {'MANGAL DOSHA' if h in (1,2,4,7,8,12) else 'clear'}")
# Sade Sati: Saturn in 12/1/2 from natal Moon
hs=house(pos["Moon"]-(pos["Moon"]%30), pos["Saturn"])
print(f"  Saturn house from Moon {hs:>2}   {'SADE SATI' if hs in (12,1,2) else 'not Sade Sati'}")
# Moon strength (paksha bala proxy): distance from Sun
d=(pos["Moon"]-pos["Sun"])%360
print(f"  Moon-Sun elongation  {d:.1f}°  -> {'bright/strong (Shukla, near full)' if 90<d<270 else 'waning/weak'}")

print("\n"+"="*78); print("3. PURVA ASHADHA'S OWN ATTRIBUTES — never stated"); print("="*78)
print("""  Deity      Apah (the Waters)          Ruling planet  Venus / Shukra
  Symbol     elephant tusk; winnowing fan  Gana          Manushya (human)
  Varna      Brahmin                       Nadi          Madhya
  Yoni       Vanara (monkey), male         Guna          Sattva
  Meaning    'the former invincible one' — undefeated, unsubdued""")

print("\n"+"="*78); print("4. LO SHU GRID — which digits his birth date is MISSING"); print("="*78)
dob="28072026"; from collections import Counter
c=Counter(d for d in dob if d!="0")
present=sorted(int(k) for k in c); missing=[n for n in range(1,10) if str(n) not in dob]
print(f"  digits present: {dict(sorted((int(k),v) for k,v in c.items()))}")
print(f"  digits MISSING: {missing}")
print(f"  Note: his Moolank (1) and Bhagyank (9) are BOTH absent from the date itself.")
