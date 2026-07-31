import swisseph as swe
from datetime import datetime, timedelta
LAT, LON, TZ = 30.2110, 74.9455, 5.5
swe.set_sid_mode(swe.SIDM_LAHIRI,0,0)
F = swe.FLG_SWIEPH|swe.FLG_SIDEREAL
NAK=["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
"Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
"Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada",
"Uttara Bhadrapada","Revati"]
TN=["Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami",
"Dashami","Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima/Amavasya"]
# Nakshatras classically approved for Namkaran (naming) samskara
GOOD_NAK={"Ashwini","Rohini","Mrigashira","Punarvasu","Pushya","Uttara Phalguni","Hasta","Chitra",
"Swati","Anuradha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Uttara Bhadrapada","Revati","Mula"}
RIKTA={4,9,14}          # Rikta tithis - avoided for samskaras
BAD_DAY={"Tuesday","Saturday"}   # classically avoided for Namkaran

print("Birth: 28 Jul 2026 10:15 IST, Bathinda.  11th day = 07 Aug, 12th day = 08 Aug\n")
print(f"{'Date':<14}{'Day':<11}{'Tithi':<26}{'Nakshatra':<20}{'Verdict'}")
print("-"*95)
d0=datetime(2026,8,3)
for i in range(21):
    d=d0+timedelta(days=i)
    j=swe.julday(d.year,d.month,d.day,10.0-TZ,swe.GREG_CAL)   # judged at ~10:00 IST
    sun=swe.calc_ut(j,swe.SUN,F)[0][0]; moon=swe.calc_ut(j,swe.MOON,F)[0][0]
    diff=(moon-sun)%360; t=int(diff//12)
    tname=("Shukla " if t<15 else "Krishna ")+TN[t%15]
    nk=NAK[int(moon//(360/27))]
    wd=d.strftime("%A")
    tnum=(t%15)+1
    bad=[]
    if wd in BAD_DAY: bad.append(wd)
    if tnum in RIKTA: bad.append("Rikta tithi")
    if t==29: bad.append("Amavasya")
    if t==14: bad.append("Purnima")
    if nk not in GOOD_NAK: bad.append("nakshatra not classical for Namkaran")
    v="** AUSPICIOUS **" if not bad else "avoid: "+", ".join(bad)
    star=" <-- 11th day" if d.day==7 else (" <-- 12th day" if d.day==8 else "")
    print(f"{d:%d %b %Y}  {wd:<11}{tname:<26}{nk:<20}{v}{star}")
